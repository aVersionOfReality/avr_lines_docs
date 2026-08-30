# Authoring Tools

The **Authoring Tools** are various scripts to help setup and manage things. These are one-shot python operators.

## Add Distance Scale Group

Inserts a **Distance_Scale** group and wires it into a width-scale socket, so line width varies with distance. See [Distance Scaling](distance-scaling.md) for the concept. This is what you use to have lines taper based on distance from camera or some fixed point, or to have them change thickness as you zoom in/out. The script batch adds the Distance Scale group to either Material Nodes or Geometry Nodes (two versions of the group exist.)

**Operator Dialog:**

- **Mode:**
    - *Material:* Distance_Scale_Mat into materials, wired to Shader_Data.
    - *Geometry Nodes:* Distance_Scale_GN into the Geo_Data container, wired to Geo_Data.
- **Apply To:** which materials (Material mode) or objects (Geo mode) to affect.
- **Modifier to add into** *(Geo mode)*: the container group name, with an option to match renamed/duplicated containers.
- **Connect To:** wire into **Scale All**, or pick specific width-scale sockets.
- **Distance Scale Group Values:** the group's inputs (Min/Max Distance, Scale @ Min/Max, Distance Source, Falloff), edited live.
- **Behavior:** remove existing groups first, and skip sockets that already have a connection.



## Bulk Copy Node Parameters

Copies AVR_Lines parameter values from one object/material to one or more destinations. Handles both the **Shader_Data** (material) and **Geo_Data** (modifier) groups, can create the group on destinations that lack it, and can optionally match renamed/duplicated groups.

## Create Custom Line ID Attribute

Generates a random face-region ID attribute (Color, Float, or Int) on each target mesh, grouped by any combination of **object, material, island**, and boundary edges (Freestyle, seam, sharp, bevel, crease, or a named edge attribute). This is the main way to author [Custom ID lines](custom-ids.md).

**Notable options:**

- **Run On:** selected objects or a collection.
- **Attribute / Type:** the attribute name and data type.
- **Group by:** Object ID, Material, Island, plus edge-boundary sources.
- **Keep-Same / Force-Different Attribute or Group:** force faces sharing a value to the same ID, or force differing faces apart.
- **Delete the Attribute Instead:** cleanup mode.



## Assign New ID to Selection

Assigns a fresh ID (distinct from the rest of the object) to your selected faces, writing to the active attribute. Run it repeatedly to build up an ID mask area by area.

## Set Marked Edge Boundaries

Saves the region data that [Marked Edge lines](marked-edges.md) read. Run it on a mesh after marking edges, and again whenever you change which edges are marked. The data is stored as a mesh, not recalculated live.

Marked Edges are a special form of [Custom IDs](custom-ids.md). ID group edges are drawn between regions of different flat values. That means they cannot handle floating marked edges, since it has to be a fully enclosed region. So to get a floating edge, we fake it by extending it to a boundary to form a full region, and then masking out those completion edges.

The script reads two edge attributes: the edges you want **drawn as lines** (Freestyle by default), and the **completion edges** that close those chains into boundaries (Bevel by default). Completion edges never draw lines themselves; they exist so the marked chain encloses a region. From those it works out the face regions on either side of every boundary and writes, per face, a region ID plus a small set of *tags*. A line is drawn where two regions meet **and** share a tag: true along your marked edges, false along the completion edges.

For best results, mark the completion edges yourself: mark from the end of the Freestyle line to a mesh boundary or another freestyle line. If you don't, the script will attempt to auto-detect and mark these completion edges. But it may get it wrong or even fail on complex or messy topology!

**Notable options:**

- **Marked Edges / Completion Edges:** which edge attributes to read. Accepts the built-in marks (`freestyle_edge`, `bevel_weight_edge`, `sharp_edge`) or any named edge attribute.
- **Trace Completions:** route completion edges automatically when the completion attribute selects none.
- **Write To:** the Face Corner color attribute the data is written to. Replaced each run.

!!! warning "Chains have to close"
    A marked chain that dead-ends in the middle of a surface can't be resolved. The regions either side end up sharing both marked and completion boundary, and nothing can tell those apart. Extend it to a mesh boundary or to another marked chain. Anything the tool couldn't resolve is listed in the console with the region pairs involved.

!!! note "Check the console"
    The tool prints a summary each run: region count, how many boundaries are marked, tag slots used, and any unresolved borders. Worth a glance if lines don't appear where you expect.

---

**Related:** [Object & Custom IDs](custom-ids.md) · [Marked Edges](marked-edges.md) · [Distance Scaling](distance-scaling.md)