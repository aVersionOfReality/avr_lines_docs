# Troubleshooting

Start here if something looks wrong. The **Warnings** section of the add-on panel catches most setup problems automatically, so check it first.

## Common problems

### No lines at all

- **Are you in a Cycles viewport?** AOVs are only written in the viewport by EEVEE, so a Cycles viewport has no line data to detect from. See [Engine support](#engine-support).
- Was **Add Compositor Nodes** run? The Line_Art group has to be wired into the compositor.
- Is the **Depth pass** enabled and are the **AOVs** created? (Run **Set Render Settings**.)
- Are you in a context that shows the compositor, such as camera view or a **Rendered viewport** with the viewport compositor set to Always?
- Check the **Warnings** section, which names most of these directly.



### Lines are doubled, blurry, or too thick

- **Anti-aliasing is probably still on.** Set Render → Film → **Filter Size = 0**. AA makes single edges detect multiple times. See [Technical Notes](technical-notes.md).
- **Lines look soft or the AA isn't good enough?** Supersample. Render at double resolution and scale down to 50% (0.5) the end of the compositor. See [Downscaling a supersampled render](width-and-scaling.md#downscaling-a-supersampled-render).
- **Is it only along the edge of frame?** The compositor's Anti-Aliasing node blurs the outermost pixels, since its samples clamp back onto the border pixel. Render a little larger and crop. See [Known Issues](known-issues.md).
- **A 1 px line renders 2 px.** That's the floor, not a bug. See [Line thickness and the 2 pixel floor](technical-notes.md#line-thickness-and-the-2-pixel-floor-for-coplanar-lines).



### Line width looks wrong in the viewport

- Width scaling and distance scaling use a camera's FOV. In **Auto/Active** camera source, that's the *scene* camera, so viewport width is only correct when looking through it, filling the screen. See [Known Issues](known-issues.md).



### Z-fighting / flickering on colored lines

- **Are the meshes intersecting there?** If two meshes pass through each other, the surfaces meet at the same depth and nothing can sort them, so the line that draws on top flickers. Precision won't help. Model the join or leave a gap instead of letting them interpenetrate. It disturbs other line types along that seam too.
- **Is it happening away from any intersection?** Then it is half precision failing to separate depths that are merely close. Enable **Full compositor precision** (it doubles intermediate buffer memory).
- **Is it only in the viewport?** For the precision case, that is expected: final renders already composite at full precision, so it is a preview artifact. Real intersections will still show up in the render.
- Switching to **Uniform Color** hides all of this, since every line resolves to the same color. It is also faster, so it's a good option if your lines are one color anyway.



### VRAM spikes / slowdowns

- You may not have enough VRAM and System RAM is being used too, which is slower. Could happen at very high resolutions on lower end cards.
- **Max Width is too high.** Every pixel pays for the full expansion range. Drop it to the smallest preset that covers your thickest line. See [Width & Scaling](width-and-scaling.md).
- **Running the Line_Art group more than once won't be the cause here.** The copies execute in series, so they don't add up in memory. They do each cost their full execution time again though, so check there if things are slow rather than spiking. See [Technical Notes](technical-notes.md).



### Marked edges don't show up

- **Did you run Set Marked Edge Boundaries?** The region data marked edges read is saved onto the mesh. Mark your edges, then run the tool. Run it again whenever you change which edges are marked.
- **Is Use Marked Edges enabled?** It defaults to off, since it costs an attribute slot and some performance.
- **Are some of the lines missing rather than all of them?** Check the console after running the tool. If it reports unresolved boundaries, those chains don't close properly and can't be told apart from their completion edges. See [Marked Edges](marked-edges.md#splitting-mixed-boundaries).
- **Are they showing up but noisy, and only in the viewport?** Check whether any part of the camera frame is cut off by the edge of the viewport. That breaks the dimensions the compositor works from, which puts noise on marked edge lines. Frame the whole camera and it clears. See [Known Issues](known-issues.md#camera-and-viewport).



### Lines appear along edges you didn't mark

- The most likely cause is a marked chain that doesn't close. The tool reports these in the console by region pair. Extend the chain to a mesh boundary or to another marked chain and run it again.
- This can happen with any ID pass as all will detect the background as a different ID. Generally it doesn't matter as you want silhoutte lines anyway. But you can change the Background's IDs in the World Material if needed.



### Custom ID lines are fuzzy, missing, or the whole area detects as lines

- ID data can't be a gradient, and **vertex data interpolates**. Use Face/Face Corner attributes, or ramp shader-driven IDs into flat regions. A variety of problems can occur depending on what data is interpolated wrong and where. See [Line Types](line-types.md).



### Engine support

The line data is carried by **AOVs**, and in the viewport those are only written by EEVEE. Under Cycles the AOVs come back empty, so there is nothing for the compositor to detect and you get no lines at all.

Everything else should work in Cycles, but it has not been through practical testing yet. This has been an EEVEE first tool. Cycles will get more attention going forward, so if you are relying on it, say so.

### Material attribute limit

EEVEE can bind at most **15 attributes per material**. Using more doesn't necessarily show any error. Often data just gets dropped and you may not notice right away.

"Attributes" means anything from the mesh: Attribute nodes, UV maps, color attributes, an Image Texture with nothing plugged into its Vector input (as that implicitly uses a UV map), Normal Map and Tangent nodes. Two nodes reading the *same* attribute only cost one slot.

`AVR_Lines: Shader_Data` **uses 6 of them** (`AVR_lines_color`, `AVR_lines_scale`, `AVR_lines_thresholds`, `AVR_lines_ID_mesh`, `AVR_lines_ID_scales`, `AVR_lines_marked`), plus one built-in. So on a material with the group added you have roughly **8 slots left** for your own setup. That is plenty for most work, but may get tight for some styles.

The add-on warns when a Shader_Data material reaches 13 or more.

**What to do if you hit the limit**

- **Reuse UV maps.** Several Image Textures sharing one UV map cost one slot; each extra UV map costs another.
- **Consolidate Attribute nodes.** Reading the same attribute in several places is free; reading many different ones is not.
- **Pack data into unused channels.** A color attribute carries four values; three separate float attributes cost three slots.
- **Turn off line features you are not using.** Disabling **Use Marked Edges** clears the `AVR_lines_marked` attribute from the group, giving that slot back across every material. It also stops the two marked AOVs being written.
- **Delete unused Attribute nodes from the group by hand, or unset their attribute.** Make a new copy of the group for that specific material first, or expand the group. Note that *disconnecting* them is not enough. See below.
- **Bake your attributes to textures.** Unless they need to update every frame (such as an attribute calculated by geometry nodes), then they can just be an image texture.

**Why disconnecting a node isn't enough**

Inside a node group, EEVEE runs every node whether or not its output goes anywhere, and its unused-node cleanup only ever looks at the top level of a material. So an Attribute node sitting unconnected inside `Shader_Data` still claims its slot. To actually free it, the node has to be removed, or its attribute name cleared. Per-material control over this is planned for a later version. If you expand the Shader_Data group so that the Attribute node is at the top level in the material, then it will cull properly if disconnected.

**A note on the count**

The reported number is a close estimate that leans slightly low: it counts the named attributes you control, but not every built-in that other nodes request behind the scenes. A material can therefore sit a little above the number shown.

---

**Related:** [Known Issues](known-issues.md) · [Technical Notes](technical-notes.md)