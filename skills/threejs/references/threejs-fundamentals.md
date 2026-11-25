# Fundamentals

Selected technical examples from CloudAI-X, adapted for the local edition.

## Cameras

### PerspectiveCamera

```javascript
// PerspectiveCamera(fov in degrees, aspect, near, far)
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 5, 10);
camera.lookAt(0, 0, 0); // rotates the camera to face the target

camera.fov = 60;
camera.updateProjectionMatrix(); // required after changing fov, aspect, near or far
```

### OrthographicCamera

```javascript
// OrthographicCamera(left, right, top, bottom, near, far); frustum size in world units
const aspect = window.innerWidth / window.innerHeight;
const frustumHeight = 10;
const camera = new THREE.OrthographicCamera(
  (-frustumHeight * aspect) / 2,
  (frustumHeight * aspect) / 2,
  frustumHeight / 2,
  -frustumHeight / 2,
  0.1,
  1000,
);
// on resize: recompute left and right from the new aspect, then call camera.updateProjectionMatrix()
```

### ArrayCamera

```javascript
// Renders the scene once per sub-camera, each into its own viewport.
// Viewport units under WebGLRenderer are drawing-buffer pixels (CSS size × pixel ratio);
// WebGPURenderer multiplies CSS pixels by the pixel ratio itself.
const width = window.innerWidth;
const height = window.innerHeight;
const dpr = renderer.getPixelRatio();
const cameras = [];
for (let i = 0; i < 4; i++) {
  const subCamera = new THREE.PerspectiveCamera(75, width / height, 0.1, 100);
  subCamera.viewport = new THREE.Vector4(
    ((i % 2) * width * dpr) / 2,
    (Math.floor(i / 2) * height * dpr) / 2,
    (width * dpr) / 2,
    (height * dpr) / 2,
  );
  subCamera.position.set(-2 + (i % 2) * 4, 1.5, 6);
  subCamera.lookAt(0, 0, 0);
  subCamera.updateMatrixWorld(); // sub-cameras are not scene-graph children; update them when they move
  cameras.push(subCamera);
}
const arrayCamera = new THREE.ArrayCamera(cameras);
arrayCamera.position.set(0, 1.5, 6); // WebGLRenderer culls every viewport with this camera's frustum (fov 50, aspect 1 by default); WebGPURenderer uses each sub-camera's frustum
renderer.render(scene, arrayCamera);
```

### CubeCamera

```javascript
const cubeRenderTarget = new THREE.WebGLCubeRenderTarget(256);
const cubeCamera = new THREE.CubeCamera(0.1, 1000, cubeRenderTarget);
scene.add(cubeCamera);

const chrome = new THREE.Mesh(
  new THREE.SphereGeometry(1, 32, 16),
  new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 1, roughness: 0 }),
);
chrome.material.envMap = cubeRenderTarget.texture;
scene.add(chrome);

// every frame: hide the reflective mesh, or it is drawn into the map it samples
chrome.visible = false;
cubeCamera.position.copy(chrome.position);
cubeCamera.update(renderer, scene);
chrome.visible = true;
```

With WebGPURenderer, build the target with `CubeRenderTarget` from `three/webgpu` instead of `WebGLCubeRenderTarget`.

## Cleanup

```javascript
scene.remove(mesh);
// dispose geometry, materials and textures only when nothing else still uses them
mesh.geometry.dispose();
const materials = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
for (const material of materials) {
  for (const value of Object.values(material)) {
    if (value?.isTexture) value.dispose(); // material.dispose() leaves its textures alone
  }
  material.dispose();
}
mesh.dispose(); // frees renderer state kept for this object only

renderer.setAnimationLoop(null); // stop the loop
renderer.dispose(); // frees the renderer's GPU resources; the WebGL context stays alive
renderer.forceContextLoss(); // also release the context when the canvas is discarded
```

`Object3D.dispose()` releases per-object renderer state (WebGPURenderer bindings, WebGLRenderer instanced-mesh buffers); it does not visit children or free geometry, material or textures. To tear down a subtree, `traverse` it and dispose each mesh as above. A custom Object3D subclass that overrides `dispose()` calls `super.dispose()`. `timer.dispose()` disconnects a connected timer.
