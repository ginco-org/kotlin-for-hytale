pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}

plugins {
    // Puts hygradle (versionless, via the settings plugin) on the build
    // classpath.
    id("gg.ginco.hygradle.settings") version "0.5.1"
}

rootProject.name = "kotlin-for-hytale"
