# Marked Edges

!!! info "Work in progress"
    This page is **minimum viable content** for the initial release. The text covers
    the essentials, but images, diagrams, and clips are still being made, and some
    sections will be expanded. More is being added over the coming weeks.

Marked edges are a special form of [Custom IDs](custom-ids.md). ID lines are drawn between regions holding different flat values, so on their own they can only follow boundaries that fully enclose an area. Marked edges can also handle floating lines that don't connect to anything. The trick is that, under the surface, it actually does complete a full region. The floating edge gets connected to a mesh boundary or another marked line, and these connection edges are masked out of the detection. But this requires an extra Attribute and AOV in the sahder over regular ID group lines (and you only get 15 total attributes in an Eevee material!) So it is kept as an extra optional line set that can be disabled via the addon to save those resources (or disabled per-material by making a copy of Shader_Data for that material and deleting the nodes in the marked edges frame.)

## How it works

You mark the edges you want as lines (Freestyle by default), and mark **completion edges** (Bevel by default) to close those chains into complete boundaries. Running **Set Marked Edge Boundaries** then reads both and bakes a region map onto the mesh: each face gets a region ID plus a small set of *tags (think overlapping mask groups)*. A line is drawn where two regions meet **and** share a tag, which is true along the edges you marked and false along the completion edges that merely closed the shape.

You don't have to mark the completion edges manually. The script defaults to auto-detecting them by walking the mesh edges. But it can make mistakes, especially on complex or unusual topology. If lines are not behaving correctly, try marking the completion edges manually.

See [Authoring-Tools](authoring-tools.md) for the script's options.

!!! note "Re-run after editing marks"
    The region map is baked, not live. You won't see changes to marked edges until you run the script again.

!!! warning "Boundary edges"  
    Because it relies on a face existing on *both* sides, marking **open/boundary edges does not work**. There's nothing on the other side to differ from.

## Splitting mixed boundaries

There's a catch in the scheme above. A marked chain and the completion edges that close it form a **single loop**, so the two regions either side of it share *both* kinds of boundary: some of it marked, some of it completion. Since the region ID and tags are the same all the way along that shared border, no comparison can draw on one part and skip the other.

**Set Marked Edge Boundaries** resolves this by cutting the mesh further, adding invisible internal boundaries so that each pair of regions only ever shares one kind of border. Those extra cuts don't draw lines; they exist purely to keep the marked and completion parts in separate region pairs.

This happens automatically and needs no setup. Two things follow from it that are worth knowing:

- **More marked edges means more regions.** A dense set of marks on one mesh produces a finely divided region map. That's normal.
- **It can't always succeed.** Where a chain doesn't close properly, the split has nothing to work with, and the tool lists the unresolved boundaries in the console rather than guessing.

!!! note "Tag slots"
    Each region carries up to three tags. A region needs more than one when it has several marked boundaries whose neighboring regions also touch each other, which the extra cuts above can bring about. The console reports **slots per region** each run; if it ever reports more than three, some lines will be missed, and the fix is to simplify the marking in that area or add a completion edge to separate the crowded regions.

---

**Next:** [Distance Scaling](distance-scaling.md) · [Authoring Tools](authoring-tools.md)