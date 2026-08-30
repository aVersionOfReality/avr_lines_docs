# Documentation Structure Plan (Phase 1)

Block-in of the SSE Line Art (aVersionOf_Compositor Line Art) documentation.
Edit this freely — it drives what gets written in Phase 2. Nothing here is
published; it lives outside `docs/`.

**Model:** midpoint between Fondant's many-small-pages and the current
grouped drafts — **one page per user-facing node group**, plus **concept pages**
for the big ideas, wrapped by the standard Overview → Install → … → Roadmap
frame. Written for **intermediate Blender users** (comfortable with materials,
modifiers, basic compositor/geo nodes), targeting **the current 1.0 addon**
(automated setup, Pixel/Adaptive width, current panel/node names). Old drafts
are raw material only.

---

## Proposed navigation (mkdocs `nav:`)

Grouped into sections (Material theme renders these as collapsible groups).

```
Home:                         index.md          (Overview)
Getting Started:
  Installation:               installation.md
  Quick Start:                quick-start.md
Concepts:
  How It Works:               how-it-works.md
  Line Types:                 line-types.md
  Width & Scaling:            width-and-scaling.md
  IDs & Edge Marking:         ids-and-marking.md
  Distance Scaling:           distance-scaling.md
Reference — Addon:
  The Addon Panel:            addon-panel.md
  Setup Tools:                setup-tools.md
  Authoring Tools:            authoring-tools.md
Reference — Node Groups:
  Line_Art (Compositor):      node-line-art.md
  Shader_Data:                node-shader-data.md
  Geo_Data:                   node-geo-data.md
  Distance_Scale:             node-distance-scale.md
Advanced:
  Manual / Node-Only Setup:   manual-setup.md
  Technical Notes:            technical-notes.md
Help:
  Troubleshooting & FAQ:      troubleshooting.md
  Known Issues:               known-issues.md
  Future Plans:               future-plans.md
  Changelog:                  changelog.md
```

Total: ~21 pages. Adjust freely — flag any you want merged or split.

---

## What goes on each page

### Home — `index.md` (Overview)
- One-paragraph "what this is": compositor-based screen-space line art, ported
  from Malt, controlled via AOVs + Shader/Geo node groups.
- Hero image/clip of results. *[IMAGE: showcase render(s)]* · *[CLIP: lines
  updating live in viewport]*
- "Who it's for / what makes it different" (high control via data passes;
  depth/normal/ID/marked lines; per-object + per-material + per-pixel control).
- Honest scope note (screen-space limits, AA caveat, performance is flat-per-pixel).
- Quick links: Installation, Quick Start, How It Works.

### Installation — `installation.md`
- Install as an Extension from disk (Get Extensions → Install from Disk).
  *[IMAGE: extension install]* (reuse `extension_install.png`)
- Where it appears afterward (Extensions + Add-ons; N-panel "aV Line Art" tab).
  *[IMAGE: N-panel location]* (reuse `setup_addon_panel-1.png`)
- Blender version requirement (5.2+). Link to Quick Start.

### Quick Start — `quick-start.md`
- The fast path: have a compositor tree → select objects → press the Setup
  Tools buttons in order → watch Warnings clear.
- Numbered steps with bold action labels (Fondant style).
- *[CLIP: pressing setup buttons, warnings resolving, lines appearing]*
- Pointer to Batch Cleanup to undo. Pointer to concept pages for tuning.

### How It Works — `how-it-works.md`  *(concept)*
- Core idea: edges = differences between neighboring pixels in image data.
- The pipeline: Geo_Data (mesh data) → Shader_Data (writes AOVs) → Line_Art
  (compositor reads AOVs, detects + expands lines). *[IMAGE/DIAGRAM: data flow]*
- Why AOVs, why AA must be off, why Depth pass needed.
- Jump Flood expansion in brief (how thickness happens; ties to Max Width cost).
- Sets up vocabulary used across the concept pages.

### Line Types — `line-types.md`  *(concept)*
- Depth, Normal, Object ID, Custom ID (×3), Marked Edges — what each detects,
  what the threshold means (or why ID types have none). *[IMAGE: each line type
  isolated on the same model]*
- Thresholds & ranges (soft falloff), grazing correction for depth.
- Islands-as-objects option. Custom IDs from attributes vs shader.
- The multiply chain (Geo × Shader × Compositor scales) with the worked example.

### Width & Scaling — `width-and-scaling.md`  *(concept)*
- Base Width + per-line-type Width Scales (where they live in each group).
- Pixel vs Adaptive width modes (replaces old Pixel/Screen/World — Adaptive now
  compensates for resolution + focal length vs Reference settings).
  *[IMAGE: same shot at two resolutions, Pixel vs Adaptive]*
- Minimum Width and sub-pixel behavior.
- Max Width (Jump Flood): what it costs, why not to over-set it. *[IMAGE: Max
  Width control]* Ties back to How It Works.

### IDs & Edge Marking — `ids-and-marking.md`  *(concept)*
- Object IDs (silhouette-ish), Custom IDs from face attributes / vertex colors /
  shader, why gradients/vertex-interpolation don't work for IDs.
- Combining IDs (the "Combine with…" hashing inputs).
- Edge Marking: how the geo-nodes setup makes it work, marked edge extensions,
  the boundary-edge limitation. *[CLIP: marking edges → lines appear]*
- The Authoring Tools that create these (Create Custom Line ID, ID Boundaries
  from Edges, Assign New ID) — link to Authoring Tools reference.

### Distance Scaling — `distance-scaling.md`  *(concept)*
- What Distance_Scale does (scale line width by distance from camera/point).
- Adding it via Add Distance Scale Group (Material vs Geometry Nodes flavour).
  *[CLIP: distance scale in action as camera moves]*
- Distance Source modes, Min/Max + Scale @ Min/Max, Falloff shapes.
- Viewport caveat (Active Camera only for some data).

### The Addon Panel — `addon-panel.md`  *(reference)*
- Tour of the N-panel: Camera Source, Line Detection, Line Scale Normalization,
  Line Expansion sections + the Detection/Scale/Expansion popover + docked
  Thresholds/Width Scales/Advanced Line Set Options.
  *[IMAGE: annotated panel]*
- Each control: one line + link to the concept page that explains it deeply.
- The `?` docs button, Warnings panel.

### Setup Tools — `setup-tools.md`  *(reference)*
- Each Setup Tools popover operator: Append Node Groups, Set Render Settings
  (+ its options and AOV toggles), Add Compositor Nodes, Add Geo Nodes (Mode
  dialog), Add AOV Group, Update Nodes, Batch Cleanup.
- What each does + when to use it. *[IMAGE: Setup Tools popover]*

### Authoring Tools — `authoring-tools.md`  *(reference)*
- Add Distance Scale Group, Bulk Copy Node Parameters, Create Custom Line ID,
  Assign New ID to Selection, ID Boundaries from Edges.
- Dialog options for each. *[IMAGE per dialog]* · *[CLIP: Create Custom Line ID
  on a mesh]*

### Node group pages (`node-*.md`)  *(reference)*
One page each. Structure per page: what the group is / where it sits in the
pipeline → its interface sockets by panel (pull tooltips from `tooltips_nodes.md`)
→ notes on non-obvious sockets. *[IMAGE: the group's node + its panels]*
- **Line_Art (Compositor):** the output group; Passes inputs, Thresholds, Width
  Scales, debug outputs.
- **Shader_Data:** AOV writer; Mix With Attribute, ID Groups,
  Width Scales, Mask Line Expansion.
- **Geo_Data:** the modifier group; ID Attributes, Width Scales, per-object
  threshold overrides, attribute inputs.
- **Distance_Scale:** _Mat and _GN flavours (shared interface); Distance Source,
  Falloff Shape. Cross-link to the Distance Scaling concept page.

### Manual / Node-Only Setup — `manual-setup.md`  *(advanced)*
- For users who want to use the node groups without the addon.
- The manual steps the addon automates: append groups, create AOVs (names+types),
  render settings, add modifiers/shader groups, wire the compositor.
- *[IMAGE: compositor wiring]* (reuse `setup_Compositor_nodes.png`)
- Note that the addon is pure convenience; nodes work standalone.

### Technical Notes — `technical-notes.md`  *(advanced)*
- Performance model (flat per-pixel; Max Width cost; don't run the group twice).
- Anti-aliasing deep dive (why AA off; the compositor AA node; sub-pixel; the
  before-AA proposal; raycast possibility).
- AOV clamping workaround (the +1/-1 normal trick). Any 5.2 specifics.

### Troubleshooting & FAQ — `troubleshooting.md`  *(help)*
- Symptom → cause → fix table/list: no lines showing, doubled/blurry lines (AA
  on), wrong width in viewport (camera source), z-fighting on colored lines,
  vram spikes, warnings meanings.
- FAQ: "why must AA be off", "why is it slower than Malt", "can I use it without
  the addon", etc.

### Known Issues — `known-issues.md`  *(help)*
- Kept from the current draft, updated: can-probably-fix / fix-as-Blender-adds-
  features / probably-never. (Could merge into Troubleshooting — flag if so.)

### Future Plans — `future-plans.md`  *(help)*
- *[NEEDS AUTHOR INPUT — no reference material for this. I'll block out the page
  and leave a note for you to fill in what you want to share publicly. I won't
  invent roadmap items.]*

### Changelog — `changelog.md`  *(help)*
- Version history. Start at 1.0; note the 5.2 update.

---

## Notes / decisions to confirm

1. **mkdocs config additions needed** for Phase 2 to render well (all standard
   for Material, and the Fondant site uses them):
   - `markdown_extensions: [admonition, pymdownx.details, attr_list, md_in_html,
     pymdownx.superfences]` — enables `!!! note/tip/warning` boxes and image
     captions/figures. Without these, note boxes render as plain text.
   - Optional: `pymdownx.emoji`, `pymdownx.highlight` for polish.
   I'll add these in Phase 2 unless you object.

2. **Old draft pages** (`setup.md`, `line-types.md`, `technical-notes.md`,
   `how-it-works.md`, `examples.md`, `parameter-input-guide.md`,
   `known_issues.md`, `index.md`): per your instruction, I'll **rename them with
   a `_OLD` suffix** (e.g. `setup_OLD.md`) and drop them from `nav:` so they stay
   for reference but don't publish, then write the new pages fresh. We delete the
   `_OLD` files once done.

3. **Reused media** already in `docs/media/`: `extension_install.png`,
   `setup_addon_panel-1.png`, `setup_Compositor_nodes.png`, the Max Width /
   Connections / Width Scale option shots. Many are from the old node-only UI, so
   some will need reshooting for the addon — I'll mark those in Phase 2.

4. **Image/clip markers:** every `*[IMAGE: …]*` / `*[CLIP: …]*` above is a
   placeholder for you to author in Phase 4. In Phase 2 I'll place these inline
   where they belong, with a caption, so you can see exactly what visual goes
   where. **More visuals than Fondant** — concept/reference pages get several
   images and clips; **each node-group page gets exactly one image**.

5. **Per-page video timestamp:** a YouTube video covers the same material. Each
   page gets a small linked callout near the top pointing to the video timestamp
   for that page's topic. Placeholder format I'll use in Phase 2:
   `> 🎬 **Video:** [Watch this section](VIDEO_URL&t=0s) *(timestamp TBD)*`
   — you swap `VIDEO_URL` and the `t=` once the video is cut. If you'd prefer a
   different widget (embedded player vs. link), say so.

6. **Future Plans / Changelog** — no reference material exists. I'll block out
   the pages and leave `[TODO: author fills in]` notes rather than invent
   content.

7. **"Examples" page** from the old draft — folded into the Home showcase +
   per-concept images rather than a standalone gallery. Flag if you want a
   dedicated Examples/Gallery page back.

8. **Parameter Input Guide** (old draft, was blocked on "nodes finalized") — its
   content is now covered by the per-node-group reference pages + Width/Line
   concept pages. Not a standalone page unless you want it.
