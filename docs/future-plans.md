# Future Plans

There are various compositor optimizations and improvements on Blender's roadmap that will help this addon. Most significantly is the option to run the Anti-Aliasing step *after* the Compositor, which will remove the need to use the Anti-Aliasing node for the whole setup. 

This is an early version of a workflow that hasn't really been available in Blender before, so expect it to keep moving for a while. Existing files shouldn't break between versions, but they will probably need adjusting. **Update Nodes** brings in the new node groups and keeps your parameter values, which should cover most changes. But it can't re-author your setup when the better ways of doing something come, or systems are improved.

What goes into version 1.1 will depend on feedback to the 1.0 release. Here are the main areas I'm looking at next for future development (*Disclaimer: this is not a commitment, nor would it all land in 1.1*)

- More user facing node groups to get certain effects more easily without having to build it all yourself.
- The option to use nodes to determine your line set mixing and priority instead of just the UI panel. This is easy to setup on the surface, but becomes complicated because the Compositor does not optimize node groups well. But hopefully that will change in the future.
- Adding the Raycast node as a line detection option. This could improve performance and solve the Anti-Aliasing problem. Currently the Raycast node only supports Attributes in Cycles, but that is hopefully coming to Eevee soon. But even in its current state it might improve Normal and Depth lines.
- Improving Normal and Depth for better Contour lines. There are various possibilities to explore here such as Dual Thresholding and fdog smoothing.
- The Is_Viewport node is set to come in 5.3 and will allow the setup to work accurately in the viewport camera, not only when viewing through the active camera.
- An option to inject Geometry Lines into the system, allowing for geo lines to be used in areas they are stronger. Or even to pipe in results from other line tools like Grease Pencil.
- Better options for pruning unused Attributes from materials.
- Support for conventiently applying/baking some parts of the Geometry Nodes group to save on performance on complex meshes.
- Improve the robustness of ID generation to avoid collisions.
- Expanded Distance Scaling node group options to make it easier to get the results you want at a given range.
- Add Color to the priority sorting system.
- Improve Trace Completions in Set Marked Edge Boundaries operator.

---

**Related:** [Known Issues](known-issues.md) · [Changelog](changelog.md)