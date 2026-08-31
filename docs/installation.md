# Installation

!!! note     You do not need the add-on to use the tool. The node groups work on their own. The addon helps setup and improves user experience. Most of the addon's fields are simply the inputs of the Compositor node group. But many change actual connections within the group, and this is difficult to do by hand. But it means that once a file is setup, you can disable the addon and still use it if you don't need to change any of those settings. This also means that render farms do not need the addon installed for everything to work. But keep in mind that the Compositor groups are an asset of the addon, and it violates the license to distribute them, even if the rest of the addon is not shared. See [Manual / Node-Only Setup](#manual-node-only-setup) below if you prefer to wire things by hand.

The tool is a Blender **extension**, installed from disk.

!!! note "Blender version"
    Requires **Blender 5.2 or newer**.

## Where to get it

- **Gumroad**: coming soon
- **Superhive**: coming soon

## Install the extension

1. Download the extension `.zip`.
2. In Blender, open **Edit → Preferences → Get Extensions**.
3. Click the drop-down in the top-right and choose **Install from Disk…**, then select the `.zip`.

Once installed it appears under both **Extensions** and **Add-ons** in Preferences.

## Where to find it

Open the **N-panel** in the 3D Viewport (press N) and select the **aVersion_Lines** tab.

!!! tip
    The panel can also be shown in the Shader, Compositor, Geometry Nodes, and Image editors. Toggle these in the add-on's preferences if you want quick access while working in those editors.

Next: **[Quick Start](quick-start.md)** to get lines on screen.

---

## Manual / Node-Only Setup

The add-on is **pure convenience**, and the node groups work on their own. This section covers doing by hand what the [Setup Tools](setup-tools.md) automate, for users who want to work node-only or understand what's happening under the hood.

!!! tip
    Everything here is one button in the add-on. Use this section if you're not using the add-on, or you're curious what it does.

### 1. Append the node groups

Append these from the asset `.blend`:

- **AVR_Lines: Line_Art** (compositor)
- **AVR_Lines: Shader_Data** (shader)
- **AVR_Lines: Geo_Data** (geometry nodes)

The Distance_Scale groups come along as dependencies.

### 2. Create the AOVs

Add these view-layer AOVs with these **exact names**, all type **Color**:


| AOV name                  | Type  |
| ------------------------- | ----- |
| `AVR_lines_mesh_ID`       | Color |
| `AVR_lines_normals`       | Color |
| `AVR_lines_thresholds`    | Color |
| `AVR_lines_scales`        | Color |
| `AVR_lines_custom_IDs`    | Color |
| `AVR_lines_custom_scales` | Color |
| `AVR_lines_marked`        | Color |
| `AVR_lines_RGB`           | Color |


### 3. Render settings

- Enable the **Depth** pass: View Layer → Passes → Data → Z.
- Disable anti-aliasing: Render → Film → **Filter Size = 0**.
- Set **Compositor Device = GPU** (Compositor N-panel → Options). CPU works but is very slow.
- For colored lines in the viewport, enable **Full precision** in the same tab to avoid Z-fighting.
- If you want lines in the viewport, set the viewport **Compositor** to Always.

### 4. Add the data groups to objects

For each object you want lines on:

- Add **Geo_Data** as a Geometry Nodes modifier (or as a group inside a group used as a modifier) after any mesh-altering modifiers.
- Add **Shader_Data** to its material, and to the World material with Normals mixed to 0 and OBJ ID mixed to -1.

!!! note
    The setup can technically run without the data groups, since they only supply data beyond the defaults, but using them is the supported path.

### 5. Wire the compositor

- Add the **Line_Art** group and connect the AOVs and the Depth pass to its Passes inputs.
- Combine the **Lines** output with your render (usually an **Alpha Over** node).
- Because film AA is off, add an **Anti-Aliasing** node for the main render. The lines have their own AA inside the group; a second AA pass over everything last doesn't hurt.
- Note that the Anti-Aliasing node can blur the outermost pixels of the image. If you need a clean border, render slightly larger and crop. See [Known Issues](known-issues.md).

See also: [How It Works](how-it-works.md) · [Setup Tools](setup-tools.md) · [Technical Notes](technical-notes.md)