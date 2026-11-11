# Changelog

## 1.0.1

**Blender 5.3 support.** 5.3 turns the compositor into a stack of effects (the new Compositor & Effects tab in Properties). 1.0.0 only looked at whichever effect was active, so as soon as you added a second one, like the new Bloom, the Parameters stopped reaching the lines and the setup and removal buttons worked on the wrong effect. Renders were still fine, but nothing told you the controls had gone dead. The addon now finds the line art in whichever effect holds it.

On 5.3, **Add Compositor Nodes** gives the lines their own **AVR Lines** effect at the bottom of the stack instead of splicing into an existing tree. Anything above it in the stack feeds into it, so Bloom and the rest keep working. **Batch Cleanup** takes the effect out again. Files you've already set up keep their lines where they are, and nothing changes in 5.2.

**The compositor reads the camera itself.** Until now the addon pushed the scene camera's FOV, focal length and clip end into the compositor group, so the lines needed the addon running to stay right. The group now reads them with Blender's Active Camera and Camera Info nodes. So lens, clip end and resolution changes come through with the addon off, or on a render farm without it. The one exception is **Sensor Fit**: set it to Horizontal or Vertical and the addon still has to be running, since Blender doesn't expose that setting to the compositor. Files set up with 1.0.0 keep the pushed values until you run **Update Nodes**.

**Faster line expansion.** The Jump Flood part of the compositor is reorganized so Blender can merge more of it into fewer GPU passes. In my tests it's about 5 to 8% faster in the viewport and while tuning lines in the Image Editor, with identical output. Run **Update Nodes** in files set up with 1.0.0 to get it. New setups get it automatically.

**Old node groups get flagged.** The addon reads the version frame in each node group, and the Warnings section tells you when the file's groups are older than the ones it ships with. The Update Nodes dialog shows which version each group is. Run **Update Nodes** to clear it. The bundled groups are now **v1.0.1**.

**Attribute limit corrected.** I had EEVEE's per-material limit at 15. It's 14, and going over doesn't quietly drop one attribute like I said. It breaks the whole material, and every attribute in it reads 0. The warning now starts at 12 and says "over the 14 limit" past that. The count itself is now worked out the way EEVEE does it, so it matches what Blender actually compiles: nodes that don't reach an output cost nothing (even inside groups, so disconnecting is enough), and the hidden costs of UV Map, Texture Coordinate, Normal Map and procedural texture nodes are included. See [Material attribute limit](troubleshooting.md#material-attribute-limit).

---

**Related:** [Future Plans](future-plans.md) · [Known Issues](known-issues.md)
