package gg.ginco.kotlinforhytale

import com.hypixel.hytale.server.core.plugin.JavaPlugin
import com.hypixel.hytale.server.core.plugin.JavaPluginInit
import java.util.logging.Level

/**
 * Loader-only plugin: it exists so the server instantiates *something* whose
 * classloader carries the Kotlin runtime. There is nothing to set up —
 * consumers reach kotlin classes through the plugin bridge (hard manifest
 * dependencies are searched first), and this plugin's presence is enforced
 * by their `depends("gg.ginco:KotlinForHytale")` manifest entries.
 */
class Plugin(init: JavaPluginInit) : JavaPlugin(init) {
    override fun start() {
        logger.at(Level.INFO).log(
            "Kotlin runtime active (bundled stdlib %s, reflect %s, coroutines %s)",
            KotlinVersion.CURRENT.toString(), "2.4.21", "1.11.0")
    }
}
