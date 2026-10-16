import org.gradle.api.file.DuplicatesStrategy

plugins {
    // hygradle comes onto the classpath via gg.ginco.hygradle.settings (0.7.0)
    // in settings.gradle.kts, so no version is declared here.
    id("gg.ginco.hygradle")
    kotlin("jvm") version "2.3.21"
}

group = "gg.ginco"
// FLK-style dual version: carrier release + the Kotlin version carried.
// Bump the second half whenever the pinned Kotlin modules below change.
version = "0.1.2+kotlin.2.3.21"

dependencies {
    // The carried Kotlin runtime. Everything here is bundled into the plugin
    // jar (bundleDependencies) and thus exists EXACTLY ONCE per server, in
    // this plugin's classloader; every consumer resolves it through the
    // plugin bridge (hard manifest dependencies are searched first, see
    // PluginManager.java). Do NOT add libraries that any consumer also
    // compiles against without intending them to be singletons server-wide.
    api("org.jetbrains.kotlin:kotlin-reflect:2.3.21")
    api("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.11.0")
    // kotlin-stdlib needs no declaration: the Kotlin Gradle plugin pins it
    // onto every source set and it flows into runtimeClasspath.
}

hytale {
    group = "gg.ginco"
    name = "KotlinForHytale"
    description = "Shared Kotlin runtime for Hytale plugins (stdlib, reflect, coroutines)"
    serverVersion = "0.7.2"
    mainClass = "gg.ginco.kotlinforhytale.Plugin"
    // The whole point: this jar IS the carrier — bundle the Kotlin runtime
    // and ship one self-contained plugin jar per release.
    bundleDependencies = true
}

// kotlin-stdlib and coroutines are multi-release jars: duplicate
// module-info/class entries are expected and must be excluded.
tasks.named<org.gradle.api.tasks.bundling.Jar>("jar") {
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
}
