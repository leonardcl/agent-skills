# React three fiber

Selected technical examples from CloudAI-X, adapted for the local edition.

## The Scene Graph as JSX

Every export of the three namespace is an element: lowercase tag, capitalized class (`<mesh>` → `THREE.Mesh`, `<meshStandardMaterial>` → its material). Props apply to the instance; shorthand values work anywhere three has a `.set()`: `position={[1, 2, 3]}`, `position={new THREE.Vector3(1, 2, 3)}`, `position={5}` (setScalar), `color="#d9915b"`. Dashed props pierce (`rotation-x`, `material-color`, `geometry-attributes-position`); `attach="material-0"` attaches into an array index.

`args` is the constructor argument list; changing it rebuilds the object from scratch. Geometries and materials attach to their parent mesh automatically — no `attach` needed.

```jsx
function Torus() {
  return (
    <mesh position={[0, 1, 0]}>
      <torusKnotGeometry args={[0.7, 0.25, 128, 24]} />
      <meshStandardMaterial
        color="#42699c"
        roughness={0.2}
        metalness={0.8}
        onUpdate={(self) => console.log(self.type)}
      />
    </mesh>
  );
}
```

Mount an object you already hold with `<primitive object={obj} />`; one object per primitive (fiber keeps its per-object state on the object), and clone for copies. Fiber never disposes primitives — their lifetime is yours. `dispose={null}` on any element opts it out of unmount disposal. Register classes outside the three namespace with `extend`:

```jsx
import { extend } from "@react-three/fiber";
import { Water } from "three/addons/objects/Water.js";

extend({ Water });
// then render <water args={[geometry]} /> anywhere in the Canvas
```

In TypeScript the tags `line`, `audio`, `source` and `path` collide with DOM types; write `threeLine`, `threeAudio`, `threeSource`, `threePath` (fiber strips the prefix and resolves the three class).

## Hooks

`useFrame(callback, renderPriority?)` subscribes to the render loop; it runs before the scene renders:

```jsx
import { useRef } from "react";
import { useFrame } from "@react-three/fiber";

function Spinner({ radius = 2 }) {
  const ref = useRef();
  useFrame((state, delta) => {
    ref.current.rotation.y += delta;
    ref.current.position.x = Math.sin(state.clock.elapsedTime) * radius;
  });
  return (
    <mesh ref={ref}>
      <sphereGeometry args={[0.4, 32, 16]} />
      <meshBasicMaterial color="#e8b4a0" />
    </mesh>
  );
}
```

Subscribers with a positive `renderPriority` take rendering into their own hands — the Canvas stops rendering, and your callback must call `state.gl.render(state.scene, state.camera)` itself. At default priority, calling `gl.render` yourself double-renders.

`useThree(selector?)` reads Canvas state reactively; with no selector it returns the whole state (`gl`, `camera`, `scene`, `raycaster`, `pointer`, `size`, `viewport`, `invalidate`, `setDpr`, `setFrameloop`, `controls`, `performance`):

```jsx
import { useThree } from "@react-three/fiber";

const camera = useThree((state) => state.camera);
const invalidate = useThree((state) => state.invalidate);
```

Inside `useFrame` use the `state` argument instead — it is the same state without a re-render. `state.clock` is a `THREE.Clock` that fiber 9.8 creates, so every Canvas logs three's Clock deprecation warning; it does not come from your code.

`useLoader(ClassOrInstance, url, extensions?, onProgress?)` suspends until any three loader resolves and caches by loader and URL; its caller must sit under a Suspense boundary. The extensions callback runs on the one loader instance fiber keeps per class, so a setting it makes (a path, a decoder) applies to every later `useLoader` call with that class. `useGraph(object)` builds named lookup maps (`{ nodes, materials, meshes }`) from an object tree:

```jsx
import { useGraph, useLoader } from "@react-three/fiber";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

function Model({ url }) {
  const gltf = useLoader(GLTFLoader, url, (loader) => loader.setPath("assets/"));
  const { nodes } = useGraph(gltf.scene);
  return <primitive object={gltf.scene} />;
}
```

`useLoader.preload(Class, url)` warms the cache outside React; `useLoader.clear(Class, url)` drops an entry.
