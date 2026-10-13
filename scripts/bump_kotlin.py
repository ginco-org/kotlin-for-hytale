#!/usr/bin/env python3
"""Bump the carrier to the latest stable Kotlin / coroutines releases.

Stable = X.Y.Z without a pre-release suffix (Beta/RC/EAP are filtered out).
Rewrites build.gradle.kts (kotlin("jvm"), kotlin-reflect, kotlinx-coroutines,
the `+kotlin.` version suffix) and the Plugin.kt log literals so the halves
stay in lockstep. Prints GitHub Actions key=value outputs (changed/kotlin/
coroutines) on stdout; human-readable summary goes to stderr.
"""
import re
import sys
import urllib.request
from pathlib import Path

CENTRAL = "https://repo1.maven.org/maven2"
STABLE = re.compile(r"^\d+\.\d+\.\d+$")
ROOT = Path(__file__).resolve().parent.parent
GRADLE = ROOT / "build.gradle.kts"
PLUGIN = ROOT / "src/main/kotlin/gg/ginco/kotlinforhytale/Plugin.kt"


def latest_stable(artifact: str) -> str:
    url = f"{CENTRAL}/{artifact}/maven-metadata.xml"
    with urllib.request.urlopen(url, timeout=30) as r:
        versions = re.findall(r"<version>([^<]+)</version>", r.read().decode())
    stable = [v for v in versions if STABLE.match(v)]
    if not stable:
        sys.exit(f"no stable release found in {url}")
    latest = max(stable, key=lambda v: tuple(map(int, v.split("."))))
    print(f"{artifact}: latest stable {latest}", file=sys.stderr)
    return latest


def main() -> None:
    kotlin = latest_stable("org/jetbrains/kotlin/kotlin-stdlib")
    coroutines = latest_stable("org/jetbrains/kotlinx/kotlinx-coroutines-core")

    gradle = GRADLE.read_text()
    plugin = PLUGIN.read_text()
    ko = re.search(r'kotlin\("jvm"\) version "([^"]+)"', gradle)
    refl = re.search(r"kotlin-reflect:([\w.]+)", gradle)
    co = re.search(r"kotlinx-coroutines-core:([\w.]+)", gradle)
    if not (ko and refl and co):
        sys.exit("could not find current Kotlin/coroutines pins in build.gradle.kts")
    ko_old, refl_old, co_old = ko.group(1), refl.group(1), co.group(1)

    gradle = gradle.replace(
        f'kotlin("jvm") version "{ko_old}"', f'kotlin("jvm") version "{kotlin}"'
    )
    gradle = gradle.replace(f"kotlin-reflect:{refl_old}", f"kotlin-reflect:{kotlin}")
    gradle = gradle.replace(
        f"kotlinx-coroutines-core:{co_old}", f"kotlinx-coroutines-core:{coroutines}"
    )
    gradle = re.sub(r"(\d+\.\d+\.\d+)\+kotlin\.[\w.]+", rf"\1+kotlin.{kotlin}", gradle)
    plugin = plugin.replace(f'"{ko_old}"', f'"{kotlin}"').replace(
        f'"{co_old}"', f'"{coroutines}"'
    )

    changed = False
    if gradle != GRADLE.read_text():
        GRADLE.write_text(gradle)
        changed = True
    if plugin != PLUGIN.read_text():
        PLUGIN.write_text(plugin)
        changed = True

    print(f"changed={'true' if changed else 'false'}")
    print(f"kotlin={kotlin}")
    print(f"coroutines={coroutines}")
    if changed:
        print(
            f"bumped Kotlin {ko_old} -> {kotlin}, coroutines {co_old} -> {coroutines}",
            file=sys.stderr,
        )
    else:
        print("already up to date", file=sys.stderr)


if __name__ == "__main__":
    main()
