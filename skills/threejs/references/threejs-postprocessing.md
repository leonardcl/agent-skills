# Postprocessing

Selected technical examples from CloudAI-X, adapted for the local edition.

## Pass Order

The composer's buffers hold linear colors; tone mapping and the sRGB conversion happen once, in `OutputPass`, using the renderer's settings. Build chains in this order: `RenderPass` → linear-space effects (bloom, depth of field, SSAO, outline, ...) → `SMAAPass`, after the effects whose edges it should smooth → `OutputPass` → `FXAAPass` (`three/addons/postprocessing/FXAAPass.js`) only when FXAA is used, because FXAA needs sRGB input. Without FXAA, `OutputPass` is the last pass.

`SSAOPass` darkens the image produced by the previous pass, so a `RenderPass` must come before it. `RenderPixelatedPass` renders the scene itself and replaces `RenderPass`. `pass.enabled = false` skips a pass without rebuilding the chain.

```javascript
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { SMAAPass } from "three/addons/postprocessing/SMAAPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new UnrealBloomPass(new THREE.Vector2(window.innerWidth, window.innerHeight), 1.5, 0.4, 0.85));
composer.addPass(new SMAAPass()); // no arguments; the composer sizes it
composer.addPass(new OutputPass());
```

## Composer Setup

- The composer copies the renderer's pixel ratio at construction. Call `renderer.setPixelRatio()` before constructing it, or `composer.setPixelRatio()` afterwards.
- The composer's buffers are not multisampled; `antialias: true` on the renderer does not reach them. For MSAA on the scene render and the composer's buffers, pass your own buffer with `samples` (CSS-pixel size) and size the composer once:

```javascript
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";

const composer = new EffectComposer(
  renderer,
  new THREE.WebGLRenderTarget(window.innerWidth, window.innerHeight, {
    type: THREE.HalfFloatType,
    samples: 4, // MSAA on the composer's two buffers
  }),
);
composer.setSize(window.innerWidth, window.innerHeight); // scales the buffer by the pixel ratio
```

- On resize, call `camera.aspect = w / h; camera.updateProjectionMatrix(); renderer.setSize(w, h); composer.setSize(w, h);` — the composer resizes its buffers and every pass, pixel-ratio included. Never resize a pass by hand.
- `composer.render()` drives time-based passes (FilmPass) from its own internal timer; pass a delta in seconds only if you manage time yourself.
- The composer assigns `renderToScreen` to the last enabled pass every frame. Set `composer.renderToScreen = false` only to keep the result off screen, as selective bloom does below.
