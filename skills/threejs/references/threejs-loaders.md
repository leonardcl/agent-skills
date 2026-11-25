# Loaders

Selected technical examples from CloudAI-X, adapted for the local edition.

## LoadingManager

One manager coordinates several loaders and reports combined progress. `loadAsync` still rejects on failure; `manager.onError` fires as well.

```javascript
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

const manager = new THREE.LoadingManager();

manager.onStart = (url, loaded, total) => {
  console.log(`Started loading: ${url}`);
};

manager.onProgress = (url, loaded, total) => {
  console.log(`Loading: ${((loaded / total) * 100).toFixed(1)}%`);
};

manager.onLoad = () => {
  console.log("All assets loaded");
};

manager.onError = (url) => {
  console.error(`Error loading: ${url}`);
};

const gltfLoader = new GLTFLoader(manager);
const textureLoader = new THREE.TextureLoader(manager);

// onLoad fires when every tracked item has finished
await Promise.all([
  gltfLoader.loadAsync("model.glb"),
  textureLoader.loadAsync("texture.jpg"),
  textureLoader.loadAsync("normal.jpg"),
]);
```

`manager.abort()` cancels in-flight requests for loaders that load through FileLoader (models, HDR, EXR, KTX2). Loaders that load through an HTML image element, such as TextureLoader, ignore it.

```javascript
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

const manager = new THREE.LoadingManager();
const timeoutId = setTimeout(() => manager.abort(), 30000);

try {
  const gltf = await new GLTFLoader(manager).loadAsync("model.glb");
  scene.add(gltf.scene);
} catch (error) {
  console.error(error);
} finally {
  clearTimeout(timeoutId);
}
```

## Cloning and Disposal

`Object3D.clone()` on a skinned model shares the skeleton: every copy stays bound to the original's bones, so copies follow the original and ignore their own animation. Use `SkeletonUtils.clone()` for instances.

```javascript
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import * as SkeletonUtils from "three/addons/utils/SkeletonUtils.js";

const gltf = await new GLTFLoader().loadAsync("character.glb");
scene.add(gltf.scene);

const copy = SkeletonUtils.clone(gltf.scene);
scene.add(copy);
```

`object.dispose()` frees renderer-side state for that object only (WebGPU bindings, InstancedMesh buffers) and does not visit children or dispose geometry, materials or textures — traverse the subtree:

```javascript
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

const gltf = await new GLTFLoader().loadAsync("model.glb");
const model = gltf.scene;
scene.add(model);

// ... later
scene.remove(model);
model.traverse((child) => {
  child.dispose(); // per-object renderer state: InstancedMesh buffers, WebGPU bindings
  if (child.geometry) { // meshes, lines and points
    child.geometry.dispose();
    const materials = Array.isArray(child.material) ? child.material : [child.material];
    for (const material of materials) {
      for (const value of Object.values(material)) {
        if (value?.isTexture) value.dispose();
      }
      material.dispose();
    }
  }
});
```
