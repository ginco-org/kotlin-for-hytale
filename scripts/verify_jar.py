#!/usr/bin/env python3
"""Verify the built carrier jar actually bundles the Kotlin runtime.

Exits 1 if any check fails; prints one OK/FAIL line per check. Shared by
ci.yml and the kotlin-bump workflow.
"""
import glob
import json
import re
import sys
import zipfile
from pathlib import Path

# the jar for the version currently declared in build.gradle.kts — never an
# older artifact left over from a previous build
ver = re.search(r'^version = "([^"]+)"', Path("build.gradle.kts").read_text(), re.M)
if not ver:
    sys.exit("could not read project version from build.gradle.kts")
jar = f"build/libs/kotlin-for-hytale-{ver.group(1)}.jar"
if not glob.glob(jar):
    sys.exit(f"missing {jar} for version {ver.group(1)} — run ./gradlew jar first")
z = zipfile.ZipFile(jar)
names = z.namelist()

checks = {
    "kotlin-stdlib classes": sum(1 for n in names if n.startswith("kotlin/") and n.endswith(".class")) > 100,
    "kotlin-reflect classes": any(n.startswith("kotlin/reflect/jvm/internal/") for n in names),
    "coroutines classes": any(n.startswith("kotlinx/coroutines/") for n in names),
    "plugin main class": "gg/ginco/kotlinforhytale/Plugin.class" in names,
    "manifest": "manifest.json" in names,
}
m = json.loads(z.read("manifest.json"))
checks["manifest names this plugin"] = m.get("Name") == "KotlinForHytale" and (m.get("Main") or "").endswith("kotlinforhytale.Plugin")
checks["server version pinned"] = m.get("ServerVersion", "").startswith("=0.7")

for k, v in checks.items():
    print(("OK  " if v else "FAIL"), k)
if not all(checks.values()):
    sys.exit(1)
print(jar, len(names), "entries — all checks passed")
