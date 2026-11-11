# Changelog

## 1.0.1

- **Blender 5.3 support.** The Line nodes will be added as their own entry at the bottom of the effect stack. You may need to adjust the order depending on any other effects in use.

- **The compositor uses camera data nodes.** The Active Camera and Camera info nodes are now used, meaning less python setting node values.

- **Slight performance improvement.** The Jump Flood part of the compositor is reorganized so Blender can merge more of it into fewer GPU passes. Should be a few % faster, but not huge.

- **Old node groups warning.** The addon reads the version frame in each node group, and the Warnings section tells you when the file's groups are older than the ones it ships with.

- **Attribute limit corrected.** It is 14 not 15.

---

**Related:** [Future Plans](future-plans.md) · [Known Issues](known-issues.md)
