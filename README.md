# kotlin-for-hytale

Hytale's [`fabric-language-kotlin`](https://github.com/FabricMC/fabric-language-kotlin):
**one shared Kotlin runtime for every plugin on a server**, instead of one
bundled copy per plugin.

A plugin jar that carries `kotlin-stdlib`, `kotlin-reflect` and
`kotlinx-coroutines` (and exists for no other reason). Because each plugin
jar gets its own `PluginClassLoader`, plugin APIs that exchange Kotlin types
(`List`, lambdas, suspend calls) only work safely when all participants bind
the **same** stdlib classes — which means one carrier per server. This is
that carrier.

## For server operators

Drop the release jar into `mods/` next to your plugins. Nothing to configure.

## For plugin authors

```kotlin
hytale {
    // hard dependency: the server refuses to load your plugin when the
    // runtime plugin is missing, and guarantees it loads before yours
    depends("gg.ginco:KotlinForHytale", ">=0.1.2")
    // never bundle the Kotlin runtime — it arrives through the bridge
    bundleDependencies = false   // or exclude it selectively (hygradle)
}
```

At compile time you just use Kotlin normally (stdlib/reflect/coroutines from
Maven Central); at runtime your loader resolves them from this plugin's
classloader via the server's plugin bridge (`PluginBridgeClassLoader`
searches declared hard dependencies first — see `PluginManager.java` in the
shared source).

### Rules that make this work

1. **Exactly one carrier.** Any plugin that *also* bundles stdlib forks the
   runtime identity per classloader — `IncompatibleClassChangeError`s across
   plugin APIs are the symptom.
2. **Declare the dependency.** Without the hard dep, stdlib resolution is
   best-effort across whatever other plugins happen to be installed.
3. **Watch the server classpath.** Resolution order is own URLs → server
   classpath → bridge. If a future Hytale server build ships Kotlin on its
   classpath, every plugin binds that copy first; version-skew issues would
   then apply server-wide.

## Versioning

`<carrier-version>+kotlin.<kotlin-version>` (e.g. `0.1.2+kotlin.2.3.21`),
like FLK. The suffix documents exactly which Kotlin runtime the jar carries;
Kotlin bumps produce new carrier releases.

## Inspiration

Obviously modeled after [fabric-language-kotlin](https://github.com/FabricMC/fabric-language-kotlin),
adapted to the Hytale plugin-loader model. No Kotlin *language adapter*
here — Hytale has no datapack-style scripting seam (yet) to adapt to.
