# Known Issues and Limitations

What the tool can't currently do, and why. Some of these are technical limitations of the tool itself, some are limitations of the method (Screen Space Extraction), and some are limitations of doiing line art in 3D at all.

For *setup* problems (no lines at all, doubled lines, and so on) see [Troubleshooting](troubleshooting.md) instead.

## Requirements and hard limits

!!! warning "EEVEE only in the viewport"
    The line data is carried by **AOVs**, and AOVs are only written in the viewport by EEVEE. In a Cycles viewport the AOVs stay empty, so you get no lines. Full renders should work properly in Cycles, but it has not been put through practical testing yet. This has been an EEVEE focused tool for the first version, and Cycles will get more attention going forward.

- **Blender 5.2 or newer is required:** The addon uses compositor and geometry nodes that don't exist earlier.
- **EEVEE only binds 15 attributes per material, and silently drops the rest:** No error, nothing in the console. The dropped attribute just reads blank or wrong, which usually turns up as one line set failing on one material while working fine everywhere else. `Shader_Data` uses 6 slots, leaving you roughly 8 for your own texturing. Plenty for most materials, tight for heavily layered ones. The addon warns you at 13. See [Material attribute limit](troubleshooting.md#material-attribute-limit) for ways to get slots back.
- **Anti-aliasing has to be off:** Detection compares neighboring pixels, and AA blurs values across pixel boundaries, so a single edge detects as several. Film Filter Size must be 0. The compositor re-anti-aliases the render with the AA node before overlaying the lines. That isn't as good as native AA. For toon styles this generally doesn't matter for your full image. But if it does, supersample (render large and scale down at the end of the compositor), or render lines separately. See [Technical Notes](technical-notes.md) and [Downscaling a supersampled render](width-and-scaling.md#downscaling-a-supersampled-render).
- **Only one** `Shader_Data` **group per material:** Two in the same material fight over the same AOVs.
- `Geo_Data` **must come after any mesh-altering modifiers** so it reads the final geometry.
- **The OBJ ID channel is doing two jobs at once:** it defines the Object ID line set, and it is what the Jump Flood Expansion uses to tell whether two pixels are on the same surface. That means only mesh-based data belongs in it. Combining texture or shader data into the OBJ ID makes a surface sort against itself and can remove whole chunks of a line pass. Put that data in a Custom ID. Separating line regions from surface sorting properly needs a second ID channel and is planned for a later version. See [The OBJ ID channel does a second job](custom-ids.md#the-obj-id-channel-does-a-second-job) and [Whole chunks are missing from a line pass](troubleshooting.md#whole-chunks-are-missing-from-a-line-pass).

!!! warning "Disconnecting a node doesn't free its slot"
    Inside a node group, EEVEE runs every node whether its output goes anywhere or not, and its unused-node cleanup only looks at the top level of a material. So an Attribute node sitting unconnected inside `Shader_Data` still costs you its slot. You have to remove it, or clear its attribute name.

## Screen-space constraints

The tool detects lines from what the camera rendered, and most of the limits below fall straight out of that. None of them are going away.

- **Only visible geometry gets lines:** Nothing off-screen or occluded is detected, and no line carries on behind an object. There's no hidden line data to work from.
- **Detection resolution is render resolution:** Anything finer than a pixel can't be detected, so fine features come and go as you change resolution. Adaptive [Threshold Scaling](width-and-scaling.md) keeps one threshold value behaving the same across resolutions, but it can't bring back detail the render never resolved.
- **The output is a raster image, not strokes:** No line objects, so no per-stroke control, no tapering along a stroke's length, and no textured or brush-like strokes. Width varies per pixel through the width scales, not along a stroke.
- **Lines on coplanar surfaces have a 2 pixel floor:** Detection keeps the neighbor pixel when it is in front, or when the depth difference is too small to tell which side is in front. In that second case both sides get marked and the line can't render thinner than 2, so asking for 1 gives 2. Where depth does resolve a front surface the mark is 1 pixel and any width is exact. In practice this mostly affects ID and Marked Edge lines, since those are the ones you draw across flat and coplanar surfaces. See [Technical Notes](technical-notes.md#line-thickness-and-the-2-pixel-floor-for-coplanar-lines).
- **Orthographic cameras aren't properly supported:** FOV, pixel size, and depth thresholds would all need different handling under an orthographic projection, and that isn't implemented. **Disable on Orthographic Camera** is on by default, so you get no lines instead of wrong ones. Turning it off is at your own risk.



## Camera and viewport

- **Everything is measured from the Active Camera:** Width scaling uses its FOV, and the camera-based distance scaling modes use its position. In the viewport that's only correct inside the camera frame, which is why the addon defaults the viewport compositor to *Camera Only*.
- **Camera-relative distance scaling is geometry nodes only:** Getting *any* camera position into a shader, by Python or by driver, recompiles the material every time the camera moves. So the material `Distance_Scale` group has no mode that reads the camera's position, and the camera-relative sources live in `Distance_Scale_GN`. Proper Z Depth can be computed in geometry nodes too and will probably be added later, but doing it there is extra computation when its already computed for the shader. Z Depth is generally the better choice over camera-relative anyway, but it may suit some styles. See [Distance Scaling](distance-scaling.md#z-depth-vs-distance-to-the-camera).
- **The viewport compositor works at the size of the camera frame on screen**, not at render resolution. Adaptive threshold scaling matches detection to a render, but the viewport still can't preview detail below its own pixel scale.

!!! note "Why the viewport camera isn't used"
    The viewport navigation camera lives on the editor Space rather than a datablock, so no driver can reach it, and fetching its position with Python means writing shader node values every frame. That throws away every compiled material using the group, which you see as surfaces flashing grey while you orbit. Using the Active Camera also avoids confusion caused by different lens or FOV settings as it is the same as in full renders.

## Transparency

Transparency causes complications, but most of them can be worked around. Which problem you get depends on the material's **Render Method**.

- **Blended materials are left out of the AOVs entirely:** EEVEE renders them on a separate transparent pass that never writes render passes, so they carry no depth, normal, or ID data and get no lines. This applies to the **whole material**, not just the parts you actually made transparent, and they don't occlude for detection either. So don't set a material to Blended and then mask the transparency down to a small area, because you lose lines across all of it.
- **Blended is therefore a useful hack:** If you want a material exempt from the line system completely, setting it to Blended is the quickest way to do it. But there are more proper ways to exempt something from lines (0 thickness, same value for the whole area in IDs passes, etc.)
- **Dithered materials write AOVs properly**, so they detect normally. If a surface is fully transparent or fully solid there's nothing to worry about, and you can leave a whole material on Dithered and mask it in only where you need it.
- **Partial transparency on Dithered causes overdetection:** Dithered resolves alpha stochastically over many samples, so a partly transparent surface blends with whatever is behind it as noise. If the thing behind carries data that would detect, every speck of that noise detects as a line, and the area usually fills in solid.
- **The fix is to remove the difference:** Give the transparent mesh and whatever is behind it the same value, or set the width scales to 0 in that area.

**Lines on a surface seen through transparency**

If you want lines on a character standing behind coloured glass, use **Blended** for the glass. It gets ignored by the line system, so the character behind detects normally. Dithered will not do this well.

**Lines on the transparent surface *and* what's behind it is harder**

- Easiest is to make whatever needs lines **opaque and split onto its own material**, since those areas get covered anyway. If you wanted a marked edge to catch scratches on glass, give the scratch edge a slight thickness and assign it a non-Blended material. Watch out for it casting opaque shadows instead of transparent ones, which you can fix with Light Path.
- With Blended you can also pick the surface up through the **Transparency pass**. If you can build an ID mask from it in that pass, you can mix that into the existing AOVs and still get lines on it.
- If you have to use Dithered and need lines on both, there's no seamless viewport answer currently. You will need to use multiple render layers and composite them together to get full control.

!!! warning "I have not tested transparency in Cycles"
    It will probably end up like Dithered in Eevee. Hopefully I can improve all this in the next version.

## ID and marked edge limits

- **ID values can't be gradients:** Which rules out vertex data, since it interpolates across each face. Use Face data stored as Face or Face Corner attributes, or ramp shader-driven IDs into flat regions. See [Object & Custom IDs](custom-ids.md).
- **Marked edges can't be open boundary edges:** The comparison needs a face on both sides, and an open edge has nothing on the other side to differ from.
- **Marked edge data is saved, not live:** **Set Marked Edge Boundaries** writes a region map onto the mesh, so it goes stale as soon as you change which edges are marked. Run it again after editing your marks.
- **A marked chain that doesn't close can't be told apart from its completion edges:** So those lines can't be drawn correctly. The tool lists unresolved boundaries in the console rather than guessing. Extend the chain to a mesh boundary or to another marked chain. See [Marked Edges](marked-edges.md#splitting-mixed-boundaries).
- **Each region only carries three line group tags:** Dense marking can go over that, and the lines that don't fit are silently dropped. The console reports *slots per region* on each run.
- **Trace Completions will fail in some situations:** The option does its best, but it can't yet handle certain low poly situations or edge flows. It only traces from the ends of floating marked edge segments currently, so it will fail in certain situations, such as needing a cut at the back of a cylinder. For now these will need to be added manually.



## Line quality

These affect how the line art looks, rather than whether it works.

- **Depth and Normal lines are less reliable than ID lines:** The data underneath them varies pixel to pixel, so they shift with small camera moves, detect areas only a few pixels across, and flicker and crawl in animation. Using both together covers most of each other's gaps, but build the majority of your lines from IDs and only use Depth and Normal where there's no ID boundary to use. The Advanced Line Set options to include Depth and Normal lines into Custom IDs (or mask with them) gives the control to address these issues. See [Line Types](line-types.md).
- **Depth lines fragment into dashes on gradual contours:** Edge strength varies along the contour, and a single hard threshold cuts that into on/off segments. Aliasing and per-pixel noise then make the dashes crawl frame to frame. This is a known hard problem in NPR line art, not something specific to this tool. Geometry based lines often handle it a bit better, and the ability to inject geo lines into the screen space system is planned.
- **Depth detection can't tell a real depth discontinuity from steep curvature:** Depth Grazing Correction uses the normals to estimate how much of a difference is just a surface angling away from you, but it often doesn't quite do enough, or it overcorrects. The proper solution would be to use Curvature detected in Geometry Nodes instead, which is planned for future versions (but will cost computation power per mesh.)
- **Grazing Correction sits outside the threshold resolution compensation:** It attenuates the detection signal rather than the threshold, so surfaces near a grazing angle can still detect a bit differently between resolutions, even with Adaptive threshold scaling on. Surfaces facing the camera aren't affected.
- **Short perpendicular fragments:** 1-2 pixel stubs sticking off a stroke. No fix in 1.0. A high quality smoothing pass is planned for the future.
- **The Anti-Aliasing node can blur the outermost pixels of the image:** Its samples run off the edge of frame and get clamped back onto the border pixel, so the outer edge blends from duplicated values. Render a little larger and crop if a clean border matters.



## Performance and precision

- **Cost of the compositor is flat per pixel**, no matter how complex the scene is. Every pixel gets evaluated whatever is in it, so heavy geometry costs no more than low poly, except for the Geometry Nodes. But they are just storing data and won't become a problem unless meshes are very large, in which case you can bake or apply most of their data and only rerun them when changes are made.
- **Max Width is the main cost:** Every pixel pays for the full expansion range even where lines are thin, so set it to the smallest preset that covers your thickest line. See [Width & Scaling](width-and-scaling.md).
- **Adding the Line_Art group more than once re-runs the whole setup:** This isn't a VRAM concern, as the copies execute in series rather than all at once. But each copy adds its full execution time again, so it can get slow. Mix your input values into a single instance if you need the speed. Taking several outputs off one instance is free.
- **Avoid intersecting meshes:** Where two meshes pass through each other the surfaces genuinely meet at the same depth, so there is nothing to sort them by and no amount of precision fixes it. The expansion can't decide which line is in front, so it flickers between them, and the same confusion affects other line types along the intersection. Model the join properly, or keep a small gap, rather than letting meshes clip. This is most visible in **Varying Color** mode, where the competing lines are different colors, but it isn't limited to it. Intersections cause issues in all 3D line detection that can see them (not Freestyle), but it is particularly noticable with colored Screen Space Lines due to the noise it creates being pixel level.
- **Half precision widens that problem to lines that are merely close:** At half precision the compositor can't reliably separate depths that are near each other, not just identical, so the same flickering appears in places that aren't actual intersections. This part only affects the **viewport**, since final renders already composite at full precision. Set compositor precision to **Full** to match the render while you work, at the cost of doubling the memory of every intermediate buffer.
- **It is slower than Malt:**  [Malt](https://malt3d.com/) is a dedicated NPR render engine and can do things the compositor can't. This should improve as the compositor gains features, but won't catch up to Malt without a dedicated Jump Flood node in the compositor.

---

**Related:** [Troubleshooting](troubleshooting.md) · [Technical Notes](technical-notes.md) · [Future Plans](future-plans.md)