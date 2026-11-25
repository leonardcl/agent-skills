---
name: threejs-game-creation
description: "Build an offline Three.js game loop with player input, a goal, feedback, replay and observable release checks."
---

# Three.js game creation

Write the starting state, input, win condition and reset before adding detail. Keep game state outside the drawing routine so the same input sequence can reproduce a run. Start with local geometry and a keyboard route. Profile the full play loop before increasing visual complexity.

Choose the [task procedure](references/workflows.md) matching the requested outcome. Available topics include threejs-3d-generator, threejs-aaa-graphics-builder, threejs-audio-generator, threejs-debug-profiler.

Try the [collecting game](example/index.html) using the local setup below.

Copy the example directory into scratch. Inside that copy, make Three.js 0.186.0 available at `node_modules/three` (normal setup: `npm install --ignore-scripts --no-save three@0.186.0`). Serve the directory with `python3 -m http.server 8000 --bind 127.0.0.1` and open the local page. After package setup the example needs only loopback access.

## Try it

Make a three-tile collecting game with arrow keys and a restart control.

**Expected result.** A player can finish, see the score and restart with all tiles restored. Repeat the same route after reset.

**Limit.** A desktop run verifies only that input device and browser. Local stand-ins do not test external asset providers.
