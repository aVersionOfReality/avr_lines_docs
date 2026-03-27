# aVersionOf_Compositor Line Art Documentation

## Screen Space Extraction (SSE) Line Art for Blender's Compositor v0.1

This description is not done yet! This is an early test version.

This tool is a compositor node group that creates line art by detecting edges in image data (differences between adjacent pixels). This is a port of the line art from the Malt Render Engine Addon adapted to compositor nodes.

A very high degree of control is achieved by using many input data passes to detect different line sets, and more to pass parameters from the material or mesh. There are also Geometry Nodes and Shader Nodes groups to provide this control. Lines can be drawn based on mesh attributes passed to the material, or on any data generated in the material. Lines can be based on depth, normals, or any arbitrary data you want. Edge Marks are also supported.

v0.1 is a soft release for testers and motivated early adopters. It is complete in terms of core features, but not in terms of UI/UX. There are known issues that I can definitely fix, others that I can probably fix, and some I cannot. And the details may depend on what features get added to Blender in future updates.

The tool is nodes. There will be a typical python addon coming to help with setup (automating appending of node groups, setting up AOVs, adding nodes to target objects and materials, changing settings that need node connections changed, etc.) Some of these scripts are already included and can be manually run to help with setup. They are only for convenience and are not necessary to use the nodes. (Note: I'm a technical artist, not a developer. I use code assistants to help write the python.)