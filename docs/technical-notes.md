# Temporary Technical Notes

!!! info "This page is a holding place"
    These are working notes, not a finished page. What's here is accurate, but belongs somewhere
    else and will move. Read it for deeper technical info.

## Performance

- The cost of the compositor is **flat per pixel**. Every pixel gets evaluated whatever is in it, so heavy geometry costs no more than low poly.
- The **Geo_Data modifier** is the exception, since that does scale with mesh size. It's only storing data, so it won't bite unless your meshes are very large. If it does, you can bake or apply most of what it stores and only re-run it when you change something.
- It is **slower than Malt**, which the compositor is the reason for, but still fast compared to most ways of getting advanced lines in Blender. [Malt](https://malt3d.com/) is the deeper tool if you want more quality and options and don't mind a custom render engine.
- This should **improve as the Compositor gains features**, but it won't catch Malt without a dedicated Jump Flood node in the compositor.
- **Max Width is what dominates the cost.** Only use what you need. The high values are mainly for high resolution renders you intend to scale down. See [Width & Scaling](width-and-scaling.md).
- **Adding the Line_Art group more than once costs time, not VRAM.** The copies execute in series, so they don't stack up memory the way you might expect. But each one is a full copy of the whole heavy setup, so each adds the same execution time again. Two instances take about twice as long. If that's too slow, mix the input values into a single instance instead of running two with different inputs.
- Taking **several outputs off one instance is fine.** The compositor evaluates each node once however many things read it, so using the outputs multiple times costs nothing extra.



## Anti-aliasing

This is the tool's main friction with normal workflows, though more options are coming.

- Edge detection compares neighboring pixel values, so it **breaks on anti-aliased data**. The blurring makes one edge detect as several, which adds thickness and wrecks threshold detection (worst on normals). So film AA has to be **off**.
- The compositor's **Anti-Aliasing node** puts AA back on the render before the lines are overlaid. It's **not as good as native AA**. Threshold defaults to 0.1 (lower than Blender's 0.2), because Filter Size 0 aliases more than SMAA's default cutoff catches. Setting it to 0 often fixes some areas and hurts others, but low values like 0.01 can work well. Contrast Limit around 2–3 is also worth trying (2.5 helped on a cel shaded model). Do not run it on the combined image: SMAA throws away weaker edges next to much stronger ones, and the lines would steal AA from nearby shading. Depending on the project you may still lose some quality, and if that matters you can treat this as a viewport preview and render your lines separately without AA for finals. See [Tuning the AA node](setup-tools.md#add-compositor-nodes).
- Anti-Aliasing can **blur the outermost pixels of the image**. It samples a small neighborhood around each pixel, and at the border those samples fall off the edge of frame and get clamped back onto the border pixel, so that outer edge ends up blended from duplicated values. Render a little larger and crop if you need a clean border, or just keep anything important away from the very edge.
- The AA node works best on high contrast data, but some line thicknesses will have feathering on diagonals. The setup actually uses multiple AA nodes with settings optimized for both situations and the two are *almost* indistinguishable, but you may still notice that Odd thickness lines look slightly better, and tapering lines can show very small issues in some situations. These issues are mostly at lower resolutions.
- Lines **thinner than 1px** won't AA well by any method and can't reach full alpha, since you can't partially fill a pixel. **Minimum Width** (1 or 2) helps, and **Width Cutoff** throws the thinnest values away rather than letting them render as grey.
- **Supersampling is the best workaround for all of this.** Render at double size and scale down by exactly 50% (0.5) at the end of the compositor with a Scale node. Detection runs at the bigger resolution so it resolves finer detail, and the downscale gives you real anti-aliasing instead of the AA node's approximation. It costs render time, but it sidesteps most of the quality loss above. See [Width & Scaling](width-and-scaling.md#downscaling-a-supersampled-render).

!!! note "Potential fixes are coming"
    A proposal to run the compositor **before** AA instead of after (which is what Malt does) would resolve most of this. The Raycast node may also allow detection before AA. Both are being watched for future versions, with no timeline.

## Line thickness and the 2 pixel floor for coplanar lines

Detection compares each pixel against its neighbors. Where two regions meet, the boundary runs *between* two pixels rather than through one, so both sides are candidates for the mark. Depth is what decides between them. The neighbor is kept if it's in front, and where the depth difference is too small to tell, both sides get kept and the mark comes out 2 pixels wide instead of 1 (well, technically, it is two single pixel lines next to each other).

Keeping both sides is deliberate. Picking one of them arbitrarily would put the line half a pixel off the real boundary, and which side won would come down to internal values you have no control over, so lines would sit slightly left of some boundaries and slightly right of others. Marking both keeps the line centered on the edge it belongs to.

The compositor then subtracts that extra pixel from the width before expanding, so the width you author is the width you get as long as its at least 2.

- **Where both sides are marked, the thinnest line is 2 pixels.** Ask for 1 and you get 2, because a 2 pixel mark can't render thinner than itself. Widths of 2 and above are exact. Where depth does resolve which side is in front the mark is 1 pixel, and any width is exact.
- **Setting a width to 0 still turns the line off.** The correction is skipped where there's no line to correct, so masking by driving a width to 0 works the way you'd expect.

The test is a tolerance rather than exact equality. The two sides count as ambiguous when their depth difference falls under a small fraction of the distance to the camera, so it covers flat surfaces, coplanar regions, and anything close enough to coplanar. Where one side is genuinely nearer, depth picks it and the mark is 1 pixel. The width correction only applies in the ambiguous case.

The tolerance is a **ratio rather than a fixed distance**, so it scales with how far away the surface is. That keeps it consistent whatever scale you model at, and it tracks depth precision as well, since the depth buffer also gets coarser with distance. A fixed value would be too tight far from the camera and too loose up close.

This applies to Marked Edge lines the same as any other. A marked chain drawn across a single flat surface is coplanar along its whole length, so in practice it is usually corrected. But where a marked edge runs along a silhouette, with something nearer in front of it, depth resolves the order and the near surface wins.

## Transparency and the AOVs

A material's **Render Method** decides whether it reaches the line system at all. This info here is all for **EEVEE**. I haven't tested transparency in Cycles, but it will most likely behave like Dithered does here.

**Blended mode materials never reach the AOVs.** EEVEE puts a material into the forward transparent pipeline when its Render Method is Blended and the shader actually produces transparency. That pipeline gets drawn separately and doesn't bind the render pass outputs at all.

It's the *material* that gets excluded and not just the transparent pixels, so masking the transparency down to a small region doesn't help. And those surfaces don't occlude for detection either, so lines on geometry behind them come through as if the transparent surface wasn't there.

Which makes Blended a handy way to exempt a material from lines completely, and the right choice when you want lines on something seen *through* a transparent surface.

**Dithered materials go through the normal deferred path**, so their AOVs get written and they detect like any other surface. The catch is that dithered alpha is stochastic. Partial transparency is resolved by taking a different surface at each sample, so a partly transparent region ends up as noise mixing the near and far surfaces together. Detection compares neighboring pixels, so if those two surfaces differ in anything being detected, every flip in that noise reads as an edge and the whole region fills in with lines. Give both surfaces the same values or scale to 0 to disable them in those areas. There is no actual fix for Partial Transparency and Dithered.

## Depth sorting and intersecting meshes

Expansion works out which line is in front by comparing depth between pixels with different Object IDs. Matching IDs count as one surface and skip that sort. Where two surfaces sit at the same depth there's nothing to compare, so the result is arbitrary and flickers as the camera moves.

**Mesh intersections are the case that can't be fixed.** Where two meshes pass through each other the surfaces genuinely do meet at the same depth along that seam, so no amount of precision resolves it, and it disturbs other line types along there too. The fix is modelling. Join the meshes properly or leave a small gap rather than letting them clip through each other. Intersections cause trouble for any 3D line method that can see them, but it's especially noticeable with colored screen space lines because the noise it creates is at pixel level.

**Half precision in the viewport widens that out to depths that are merely close**, since it can't separate nearby values reliably.

!!! note "Full compositor precision"
    The setup switches the **viewport** to Full precision. This is a different thing from the AOV storage below, it governs the compositor's own intermediate buffers. It only changes the viewport. On Auto, Blender already composites final renders at full precision and only drops to half for interactive work, so really this setting is about making the viewport match what you'll get out of a render. It does nothing for actual intersections, which are ambiguous at any precision.

Either way you notice this most in **Varying Color** mode, where the competing lines are different colors. In Uniform Color they both resolve to the same color, so the same ambiguity has nothing to show. The Object ID is the mesh ID behind that sort. See [The OBJ ID channel does a second job](custom-ids.md#the-obj-id-channel-does-a-second-job).



## How line data reaches the compositor

Everything the compositor detects from is written by the shader into 9 **AOVs**, and read back on the other side. In the viewport only EEVEE writes those, which is why a Cycles viewport shows no lines. A few things about that round trip are worth knowing if you ever edit the AOVs or author your own ID data.

**Values have to be flat, not gradients.** Detection compares neighboring pixels, so a gradient reads as a continuous run of differences and detects as a solid block rather than a line. That's why vertex data can't carry IDs, it interpolates across the face. See [Object & Custom IDs](custom-ids.md).

**Sub-pixel sampling blends values at boundaries.** EEVEE resolves its samples after the shader runs, so a pixel straddling a region boundary stores the *average* of both sides rather than either one. Detection is built around that. It compares values for equality or against a threshold, and a blended value just matches neither side. Anything that tried to decode a packed or bit encoded value instead would turn that blend into a plausible but wrong answer, which is why the line data is kept as plain values.

**AOV color passes are half float.** IDs are values between 0 and 1, and half float spacing is relative rather than fixed, so how much room you have depends on where in that range the value sits. Down near 0.01 the gaps are tiny, but from 0.5 up to 1.0 the spacing is 1/2048, which is the worst case. There are around 15,000 distinct values available across the whole range, and evenly spread IDs stay safe up to about 1000 of them.

Random values collide sooner than that though. Two IDs landing close enough to store as the same number only costs you anything if those two regions happen to be touching on screen, so in practice you would need a very complex setup before you saw it. When it does happen you get a missing line where you expected one, between two regions that look like they should differ. If you authored the ID yourself, changing its value fixes it. Making this properly robust is on the list for a future version, see [Future Plans](future-plans.md).

## Depth and Normal detection

Depth and Normal lines read data that varies pixel to pixel, which is what makes them less reliable than ID lines. They shift with small camera moves, detect areas only a few pixels across, and flicker or crawl in animation. Using both together covers most of each other's gaps, and the **Advanced Line Set** options (adding Depth and Normal into a Custom ID, or masking with them) give you finer control over where they apply. See [Line Types](line-types.md) and [Known Issues](known-issues.md).

**Depth detection can't tell a real depth discontinuity from steep curvature.** A surface angling away from you produces a big depth difference between neighboring pixels even though nothing is actually in front of anything. **Depth Grazing Correction** uses the normals to work out how much of that difference is just the angle, and discount it. It's an approximation, so it often doesn't quite do enough, or it overcorrects. Measuring real curvature in Geometry Nodes would be the proper fix, at the cost of computation per mesh. See [Future Plans](future-plans.md).

**Grazing Correction sits outside the threshold resolution compensation.** It attenuates the detection signal rather than the threshold, so surfaces near a grazing angle can still detect a bit differently between resolutions even with Adaptive threshold scaling on. Surfaces facing the camera aren't affected.

## Version specifics

- Requires **Blender 5.2+**. Earlier 5.x used a different geometry nodes modifier input API and didn't have some nodes the tool uses.
- **AOV clamping:** Blender clamps Color AOVs to 0 and above, which is a problem for anything needing negatives, like normals. The setup works around it by **adding 1** to some colors in the shader and **subtracting it back off** in the compositor. Worth knowing if you edit the AOVs by hand.

---

**Related:** [How It Works](how-it-works.md) · [Known Issues](known-issues.md) · [Troubleshooting](troubleshooting.md)