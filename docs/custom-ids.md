# Object & Custom IDs

!!! info "Work in progress"
    This page is **minimum viable content** for the initial release. The text covers
    the essentials, but images, diagrams, and clips are still being made, and some
    sections will be expanded. More is being added over the coming weeks.

Depth and normal detection only go so far. Object IDs and Custom IDs let you draw lines wherever you define a region. Use them for any areas where you always want a line. This works for creating lines between different surfaces, and also detail lines on the same surface. ID lines give the best results and should be used for the majority of your lines. Use them to separate different parts of a character's outfit, or for sharp edges on a hardsurface mesh, or even for seams on clothing. And you can use the [advanced line set options](#advanced-line-set-options) to mix additional Normal and Depth lines into custom IDs to catch those sorts of areas while sharing the ID line set's width. See [Line Types](line-types.md) for more info.

## How IDs work

IDs are regions with a shared value. Lines are detected where those values are different. So you define the line by putting different values on either side of it. If you set every face of a mesh to have a different ID value, you'd get lines between every face. If you set half the mesh to have one value and the other half another, you'd get a line down the middle of the mesh, etc. But if you have a gradient, every pixel in it will detect as a line because there are differences between each neighboring pixel (so there must not be any gradients). What these values actually are makes no difference as long as they are flat values. The point is simply to identify different areas by them having different values. See [How It Works](how-it-works.md).

IDs can be authored in many ways. You can manually create them with Vertex Paint Mode set on Face selection (to avoid gradients which will be caused by Vertex Selection.) Or in Geoemtry Nodes with Face Data. Or paint them on a texture (set brush falloff to constant). Or in the material even with procedural textures or shading as long as the result is flat values. These can be forced by Ramping or Quantizing (Greater Than math node, Color Ramp on Constant, Or Map Range on Stepped are some methods.) This addon has its own scripts to author IDs based on various mesh data like marked edges of various types, material boundaries, etc. See [Authoring Tools](authoring-tools.md).

The big limitation of IDs is that they cannot support a floating, disconnected edge/line by definiton. Since they must be solid regions, every line must connect to another one, or to a mesh boundary. This must be planned for when marking them on a mesh. If you have a situation that does need a free floating line tip, then your choices are to extend and connect the line and then scale that area to 0 thickness to hide it (which can be unreliable at different camera angles), or use the [Marked Edges](marked-edges.md) system, which is a more robust version of that (but costs more attributes, AOV passe, and computation.)

If you are using thick lines anyway, you can also work around the limitation by having multiple different region boundaries right next to each other. This will cause overdetection of lines and force a minimum thickness. But that doesn't matter if you were going to have them at least that thick anyway.

### Combining IDs

The Geo_Data and Shader_Data groups both have **Combine with…** inputs. When one is above 0, its value is **hashed into** the current ID, letting you merge multiple ID sources into a single line set. So you can define part of an ID on the mesh and part in the shader, and combine them.

The combining is done using the White Noise procedural texture. White Noise is deterministic based on the inputted coordinates. A face/pixel at the same location gets the same value, and every location gets a different value. This lets you combine up to 4 IDs by using them as the vector XYZ and W inputs. 2D white noise uses only X and Y, 3D uses XYZ, and 4D adds the W. If you wanted to combine more than 4, chain the white noises. The Geo_Data and Shader_Data groups already have inputs setup for this combining, but if you needed to do more advanced combines you can easily setup the nodes outside the group and use the ID Mix inputs to replace them, or even edit the group and move the Store Attributes or AOVs outside.

!!! warning "Partial mixes can create gradients"
    If mixing ID groups based on a mask, make sure it doesn't have a gradient. And remember that the mask itself is going to implicitly define a new region boundary.

## Object IDs

Every object gets a unique random ID, so lines appear wherever different objects meet (or meet the background). This gives you silhouette-like outer lines. The Object ID line set is not inherently different from the Custom IDs except that the object ID is already loaded into it. It is used in the Jump Flood Expansion to help determine if areas are the same or different surfaces and avoid depth ambiguity that can occur between neighbors with similar depth. If you combine other ID attributes into it, these will also be used for this, which is generally good as long as they are also mesh based. If they are shader based and don't correspond to actual geoemtry edges (such as toon shading or a texture) it can get weird, so put those in a Custom ID instead.

The **Treat Islands as Objects** option (Geo_Data) extends this: each connected mesh island becomes its own ID, so a single object's separate parts get boundary lines between them.

## Custom IDs

Three custom ID passes let you draw lines on regions you define. There are two places to author them, and you can combine both.

### From mesh attributes (Geometry Nodes)

Author **Face** data where each region has a distinct value, and point a Custom ID input at that attribute name.  The [Authoring Tools](authoring-tools.md) can generate these for you.

!!! warning "Face data only"
    IDs can't use gradients, and **vertex data gets interpolated** into a gradient across each face. Use Face data stored in Face or Face Corner attributes so a hard difference only exists between neighboring faces. More explanation in [Line Types](line-types.md).

### From the shader

Feed a Custom ID from anything in the material, such as a texture, a procedural mask, or toon bands. Use **ramps** or **steps** to snap values into flat regions so there are no gradients to overdetect.

## Advanced Line Set Options

Each ID line set has two extra controls that change how it interacts with the others. Both live in the **Advanced Line Set Options** sub-panel. See [The Addon Panel](addon-panel.md#advanced-line-set-options) for the exact fields.

### Priority

Where two line sets both detect the same pixel, only one of them can decide its width. By default the **thicker** line wins. That is usually the correct behavior, but it can cause problems when a detail that should be small exists in multiple line sets. For example, if a fine seam on clothing was included in a Custom ID group set to a thin size, but is also detected by thicker Normal lines from some view angles. In some situations it is enough to use different scale within the same line set for different sizes, but this can break at different camera angles and is a hassle.

The line set with the higher priority value wins. The actual values don't matter. You could use 1, 2, 3, etc or 100, 200, 300.

Priority only matters where sets overlap. If your line sets never detect the same pixels, it has no effect. It also has no effect on line Expansion. It won't stop a thick line from expanding over a thin one adjacent to it.

### Including Depth and Normals in an ID line set

ID lines can only follow boundaries you have defined as regions. Some things are awkward to author that way, such as a fold that only shows at certain angles, or two parts overlapping in a way that depends on the pose. Those are cases Depth and Normal detection handle well.

**Include in Line Set** adds Depth and/or Normal detection *into* an ID line set. The result belongs to that line set: it takes that set's width, scale, and priority, rather than the global Depth or Normal line settings. This is completely separate from the Depth and Normal line sets themselves, which continue to work independently.

Use it to fill gaps an ID can't reach, while keeping the line weight consistent with the rest of that set.

Each channel of a line set (its own ID edge, Depth, and Normal) has a **role**:

- **Off**: ignore that channel.
- **Include**: add it to the line set. Lines appear where the ID *or* that channel detects.
- **Mask**: restrict the line set to where that channel *also* detects. Lines appear only where both agree.

**Include** widens what the set catches; **Mask** narrows it. Setting several channels to Mask narrows it further, since the line then only survives where all of them detect. Mask is the one to reach for when an ID boundary catches too much and you want to keep only the part that is also a real depth or normal feature.

Each line set carries its own Depth and Normal thresholds, independent of the global ones, and they follow **Threshold Scaling Mode** in the same way.

A common example where this system is useful is the chin of a character. If you mark the face and neck as separate IDs, it will work fine from front angles where the boundary isn't visible. But from lower angles, you'll see the boundary marked with the line instead. If you use only the Depth or Normal lines, they can be unreliable from different angles unless you paint detailed Threshold groups for them, and you may even need different thresholds for different camera directions to look correct. But if you have that ID and mask it by Depth (or vice versa), you'll only get lines when both are true. You can use a much lower depth threshold to ensure you pick up the difference between the chin and neck without overdetecting.

## The Tools:

The add-on's **[Authoring Tools](authoring-tools.md)** generate ID attributes for you:

- **Create Custom Line ID:** assign region IDs by object, material, island, or marked boundaries.
- **Assign New ID to Selection:** paint IDs onto selected faces, area by area.

See [Authoring Tools](authoring-tools.md).

---

**Next:** [Marked Edges](marked-edges.md) · [Distance Scaling](distance-scaling.md)