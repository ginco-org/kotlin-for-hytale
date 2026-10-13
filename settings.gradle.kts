pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}

plugins {
    // Puts hygradle (versionless, via the settings plugin) on the build
    // classpath. 0.7.0+ bundles and registers the foojay toolchain resolver
    // itself, so the JDK 25 toolchain auto-provisions without a local JDK.
    id("gg.ginco.hygradle.settings") version "0.7.0"
}

rootProject.name = "kotlin-for-hytale"
