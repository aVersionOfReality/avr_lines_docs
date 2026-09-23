# Quick Start

<iframe src="https://www.youtube.com/embed/Ejzm687bvzA?start=581"
        title="Getting started"
        style="width:100%;max-width:860px;aspect-ratio:16/9;border:0;"
        allowfullscreen>
</iframe>

The add-on's **Setup Tools** do every step for you; this page is just the order to run them in. For what each one does, see [Setup Tools](setup-tools.md).

## The steps

Open the **aV_Line Art** N-panel → **Tools** → **[Setup Tools](setup-tools.md)**, and run these in order. **Warnings** will clear as you go.

1. **Append Node Groups** brings the AVR_Lines node groups into your file.
2. **Set Render Settings** enables the Depth pass, turns off anti-aliasing (Filter Size 0), sets the compositor to GPU, and creates the AOVs. Leave the defaults on for a first run.
3. **Add Compositor Nodes** splices the Line_Art group into your compositor before the output, along with the anti-aliasing node. If the scene has no compositor tree, it makes one.
4. **Add Geometry Node Group** adds the Geo_Data modifier to your selected objects.
5. **Add AOV Group to Materials** adds the Shader_Data group to those objects' materials.

Enter Active Camera view or do a full F12 render and you should have lines. By default, you'll have Normal, Depth, and Object lines. Normal and Depth lines probably won't look great with default settings. Next, start adjusting their thickness or thresholds.  Or setup Custom ID groups to better control where lines appear and avoid many of the issues with Normal and Depth lines.

!!! note
    The guide and examples are being worked on!

## Undoing it

The **Batch Cleanup** button (Tools → [Authoring Tools](authoring-tools.md)) opens a dialog to remove the added node groups, modifiers, materials, AOVs, and to reset render settings. Tick what you want removed and run it.

---

**Next:** [How It Works](how-it-works.md) · [Line Types](line-types.md) · [Troubleshooting](troubleshooting.md)
