pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}

plugins {
    // kotlin-for-hytale builds with the JDK 25 toolchain hygradle defaults to; on
    // hosts without a local JDK 25 the foojay resolver provisions one. (The
    // resolver bundled into hygradle.settings ≤0.6.0 did not make it into the
    // published jar, so declare it here too.)
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
    // Puts hygradle (versionless, via the settings plugin) on the build
    // classpath.
    id("gg.ginco.hygradle.settings") version "0.6.0"
}

rootProject.name = "kotlin-for-hytale"
