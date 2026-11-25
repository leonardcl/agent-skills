---
name: threejs
description: "Build or diagnose a browser 3D scene, including assets, materials, camera, lighting, interaction and frame budget."
---

# Three.js

A rotating specimen viewer needs geometry, picking and resize behavior. Use this skill for the rendered scene. Use the game skill when inputs advance a goal or score.

Choose the [task procedure](references/workflows.md) matching the requested outcome. Available topics include threejs-animation, threejs-asset-pipeline, threejs-fundamentals, threejs-geometry.

Try the [offline viewer](example/index.html) using the local setup below.

Copy the example directory into scratch. Inside that copy, make Three.js 0.186.0 available at `node_modules/three` (normal setup: `npm install --ignore-scripts --no-save three@0.186.0`). Serve the directory with `python3 -m http.server 8000 --bind 127.0.0.1` and open the local page. After package setup the example needs only loopback access.

## Try it

Render a colored box, resize the window, then select the object without moving the camera.

**Expected result.** The canvas retains its proportions and selecting the box changes its visible state.

**Limit.** An installed Three.js module and a browser with a supported graphics backend are needed for a rendered result.
