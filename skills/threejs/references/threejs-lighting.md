# Lighting

Selected technical examples from CloudAI-X, adapted for the local edition.

## DirectionalLight

```javascript
// DirectionalLight(color, intensity): parallel rays from position towards target; the distance only matters to the shadow camera
const dirLight = new THREE.DirectionalLight(0xffffff, 3);
dirLight.position.set(5, 10, 5);

// Shines from its position towards target; add the target to the scene when you move it
dirLight.target.position.set(0, 0, 0);
scene.add(dirLight.target);
scene.add(dirLight);
```

### SunLight: automatic cascaded shadows

`SunLight` (`three/addons/lights/SunLight.js`) is a parallel light with two cascaded shadow maps, suited to large scenes. It has no target: it shines from its position towards the origin, straight down by default. With WebGLRenderer it works out of the box; under WebGPURenderer register it first (see WebGPU and TSL).

```javascript
import { SunLight } from "three/addons/lights/SunLight.js";

const sun = new SunLight(0xfff2e3, 3);
sun.position.set(100, 160, 60);
sun.castShadow = true;
scene.add(sun);
```

The cascades are fitted automatically to slices of the camera's view frustum, up to `sun.shadow.camera.far` or the view camera's far plane, whichever is smaller. `shadow.camera.left/right/top/bottom` are ignored; the default `mapSize` is 1024 × 1024 per cascade. There is no shadow frustum to hand-tighten.

## Shadows

```javascript
// 1. Renderer: shadow maps are off by default; PCFShadowMap is the soft filtered default,
// VSMShadowMap blurs the map itself, BasicShadowMap is hard-edged
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFShadowMap;

// 2. Light
const dirLight = new THREE.DirectionalLight(0xffffff, 3);
dirLight.position.set(5, 10, 5);
dirLight.castShadow = true;
scene.add(dirLight);

// 3. Objects
mesh.castShadow = true;
mesh.receiveShadow = true;
```

`shadow.radius` above 1 widens the PCF filter and the VSM blur; it has no effect with BasicShadowMap. VSM also exposes `shadow.blurSamples` (default 8), and PointLight shadows do not support VSM at all — WebGLRenderer warns and skips the light's shadow. PCFSoftShadowMap is deprecated: it warns and falls back to PCFShadowMap, which is already soft. With VSMShadowMap, every mesh that receives shadows also casts them.

### Tuning a directional shadow

```javascript
const dirLight = new THREE.DirectionalLight(0xffffff, 3);
dirLight.position.set(5, 10, 5); // every caster must lie between near and far from here
dirLight.castShadow = true;

// The shadow camera sits at the light's position and looks at its target: near and far
// are distances from the light; left/right/top/bottom frame the area around the target
const shadowCam = dirLight.shadow.camera;
shadowCam.left = -10;
shadowCam.right = 10;
shadowCam.top = 10;
shadowCam.bottom = -10;
shadowCam.near = 0.5;
shadowCam.far = 50;
shadowCam.updateProjectionMatrix(); // needed whenever these change after the first render

dirLight.shadow.mapSize.set(2048, 2048); // powers of two

// Acne: normalBias offsets the lookup along the surface normal (light grazing a surface);
// bias offsets the depth compared against the map — start tiny, negative fights acne
dirLight.shadow.normalBias = 0.02;
dirLight.shadow.bias = -0.0001;

// Lighten shadows without adding fill lights: 0 removes, 1 is full darkness
dirLight.shadow.intensity = 0.7;
```

### Point and spot shadow cameras are derived

The renderer rebuilds these cameras on every shadow pass: a spot light's shadow fov is `2 × angle × shadow.focus` (in degrees) and its far comes from `light.distance`; a point light's far also comes from `light.distance`. The fov is always overwritten, and a manual `far` survives only while `distance` is 0. Control the cone with `angle` and `shadow.focus`, the range with `distance`.

```javascript
const deskLamp = new THREE.SpotLight(0xffffff, 250, 30);
deskLamp.castShadow = true;
deskLamp.shadow.mapSize.set(1024, 1024);
deskLamp.shadow.focus = 0.9; // shadow fov as a fraction of the light's cone
deskLamp.shadow.bias = -0.0001;
```

Visualize a directional or spot light's shadow camera with `new THREE.CameraHelper(light.shadow.camera)` added to the scene, and call the helper's `update()` after changing the camera.

### Contact shadows (fake, cheap)

A shadow map per light is overkill for a grounded look; a radial-gradient blob costs one textured quad.

```javascript
// A soft blob under the object: no shadow map, works under both renderers
const size = 128;
const canvas = document.createElement("canvas");
canvas.width = canvas.height = size;
const ctx = canvas.getContext("2d");
const gradient = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
gradient.addColorStop(0, "rgba(0,0,0,0.6)");
gradient.addColorStop(1, "rgba(0,0,0,0)");
ctx.fillStyle = gradient;
ctx.fillRect(0, 0, size, size);

const shadowTexture = new THREE.CanvasTexture(canvas);
shadowTexture.colorSpace = THREE.SRGBColorSpace; // a canvas used as a color map is sRGB

const blob = new THREE.Mesh(
  new THREE.PlaneGeometry(2, 2),
  new THREE.MeshBasicMaterial({ map: shadowTexture, transparent: true, depthWrite: false })
);
blob.rotation.x = -Math.PI / 2;
blob.position.y = 0.001; // just above the floor to avoid z-fighting
scene.add(blob);
```

For a blob that follows the object's silhouette, render depth from below into a render target and blur it — the official `webgl_shadow_contact` example does this with `HorizontalBlurShader` and `VerticalBlurShader` from `three/addons/shaders/`.
