# Performance

Selected technical examples from CloudAI-X, adapted for the local edition.

## Measure First

Optimize what the numbers name, not what a hunch suspects. WebGLRenderer's `renderer.info` object is read after `render()`:

```javascript
function animate() {
  renderer.render(scene, camera);
  console.table({
    calls: renderer.info.render.calls, // draw calls submitted by this render
    triangles: renderer.info.render.triangles,
    lines: renderer.info.render.lines,
    points: renderer.info.render.points,
    geometries: renderer.info.memory.geometries, // geometry buffers live on the GPU
    textures: renderer.info.memory.textures,
    programs: renderer.info.programs.length, // compiled shader programs in the cache
  });
}

renderer.setAnimationLoop(animate);
```

Details worth knowing when reading these:

- The counters reset at the start of every `render()` call while `info.autoReset` is true (the default). Reading them before `render()` reports the previous frame, and a frame with several `render()` calls (picking, reflections, post passes) shows only the last one's numbers.
- Shadow-map drawing runs through the same counters: each shadow-casting light re-draws its casters from the light's view inside `render()`, and those draws appear in `calls` and `triangles`. Toggling a light's `castShadow` is directly visible here.
- `info.memory.geometries` and `info.memory.textures` count uploads, not bytes; they drop when the matching `dispose()` runs. Geometries and textures upload once and are shared by every mesh that references them.

When a frame really has several `render()` calls, accumulate over the whole frame yourself:

```javascript
renderer.info.autoReset = false; // render() stops clearing the counters

function animate() {
  renderer.render(scene, camera);
  console.log(renderer.info.render.calls); // every render of this frame, summed
  renderer.info.reset(); // once per frame, after the last render
}

renderer.setAnimationLoop(animate);
```

`Timer` gives the frame interval; average it over a second of frames, single frames jitter too much to compare. The interval never drops below one display refresh (16.7 ms at 60 Hz), so it shows dropped frames but not headroom; time the CPU side of the frame with `performance.now()` around the work:

```javascript
const timer = new THREE.Timer();
timer.connect(document); // pauses while the tab is hidden

let interval = 0;
let cpu = 0;
let frames = 0;

function animate() {
  timer.update();
  interval += timer.getDelta(); // seconds since the previous frame, never less than one display refresh
  const start = performance.now();
  renderer.render(scene, camera);
  cpu += performance.now() - start; // CPU time spent in render(); the GPU executes the commands later
  frames++;
  if (frames === 60) {
    console.log(`${((interval / frames) * 1000).toFixed(2)} ms per frame, ${(cpu / frames).toFixed(2)} ms CPU in render()`);
    interval = 0;
    cpu = 0;
    frames = 0;
  }
}

renderer.setAnimationLoop(animate);
```

For anything deeper than frame time, use the browser profiler — the Chrome DevTools Performance panel shows long main-thread tasks, scripting versus rendering time, and GPU work on its GPU track. The `stats-gl` package shows a live per-frame statistics overlay when you want the numbers always visible.

## Draw Calls

Each visible mesh queues one draw call, or one per geometry group when the material is an array, and two settings multiply that: a `transparent` material with `side: THREE.DoubleSide` draws each mesh twice, back faces then front faces (`forceSinglePass: true` makes it one), and while any MeshPhysicalMaterial with `transmission` above 0 is in view, every opaque object is drawn a second time into the transmission buffer. Without those two, a thousand single-material meshes is a thousand draw calls; `info.render.calls` is the number to watch. The classic reducers:

**Merge static geometry.** Many meshes that never move and share one material become one mesh and one call:

```javascript
import * as BufferGeometryUtils from "three/addons/utils/BufferGeometryUtils.js";

const rockGeometry = new THREE.DodecahedronGeometry(1, 0);
const transform = new THREE.Matrix4();
const parts = [];
for (let i = 0; i < 200; i++) {
  const baked = rockGeometry.clone();
  transform.setPosition((Math.random() - 0.5) * 40, 0, (Math.random() - 0.5) * 40);
  baked.applyMatrix4(transform); // bake the placement into the vertices
  parts.push(baked);
}
const merged = BufferGeometryUtils.mergeGeometries(parts); // inputs need matching attributes and index state
scene.add(new THREE.Mesh(merged, new THREE.MeshNormalMaterial())); // 200 rocks, one call — but one bounding sphere for all of them
```

Merging trades culling granularity for the call count: the merged mesh has a single bounding sphere, so frustum culling is all-or-nothing. Keep world-sized clusters merged per cluster, not one merge for a whole level.

**Instance repeats.** One geometry drawn many times with per-instance transforms stays one call:

```javascript
const tree = new THREE.ConeGeometry(0.5, 2, 6);
const trees = new THREE.InstancedMesh(tree, new THREE.MeshNormalMaterial(), 500);
const placement = new THREE.Object3D();
for (let i = 0; i < 500; i++) {
  placement.position.set((Math.random() - 0.5) * 40, 1, (Math.random() - 0.5) * 40);
  placement.rotation.y = Math.random() * 6.28;
  placement.updateMatrix();
  trees.setMatrixAt(i, placement.matrix);
}
// culling tests one sphere around all instances (computed lazily on the first cull test), so all 500 draw whenever it touches the view;
// after moving instances later, set trees.instanceMatrix.needsUpdate = true and call trees.computeBoundingSphere()
scene.add(trees);
```

**Batch different geometries.** Many geometries sharing one material pack into shared buffers:

```javascript
const material = new THREE.MeshNormalMaterial();
const batchedMesh = new THREE.BatchedMesh(500, 20000, 20000, material);
const coneId = batchedMesh.addGeometry(new THREE.ConeGeometry(0.5, 2, 6));
const boxId = batchedMesh.addGeometry(new THREE.BoxGeometry(1, 1, 1));
const placement = new THREE.Matrix4();
for (let i = 0; i < 500; i++) {
  const instanceId = batchedMesh.addInstance(i % 2 ? coneId : boxId); // a geometry renders only through an instance
  placement.makeTranslation((Math.random() - 0.5) * 40, 1, (Math.random() - 0.5) * 40);
  batchedMesh.setMatrixAt(instanceId, placement);
}
scene.add(batchedMesh);
```

Unlike InstancedMesh, it culls and sorts each instance on its own (`perObjectFrustumCulled` and `sortObjects`, both on by default). WebGLRenderer multi-draws these in one call where the browser supports `WEBGL_multi_draw`, one draw per instance otherwise; the WebGPU backend issues one draw per instance. `threejs-geometry` covers both APIs in depth.

**Drop detail with distance.** `LOD` keeps every level as a child and, inside every `render()` (its `autoUpdate` is on by default), shows only the level for the current camera distance, so far objects submit fewer triangles — the call count stays the same:

```javascript
const detailMaterial = new THREE.MeshNormalMaterial();
const lod = new THREE.LOD();
lod.addLevel(new THREE.Mesh(new THREE.SphereGeometry(1, 64, 32), detailMaterial), 0); // distances are camera-to-object
lod.addLevel(new THREE.Mesh(new THREE.SphereGeometry(1, 16, 8), detailMaterial), 12);
lod.addLevel(new THREE.Mesh(new THREE.SphereGeometry(1, 8, 4), detailMaterial), 30);
scene.add(lod);
```

**Let culling skip whole calls.** Frustum culling is on by default: before a mesh is queued, its geometry's bounding sphere is tested against the camera frustum, and a failed test removes the draw entirely. Two ways to lose it silently: editing vertices on the CPU without `geometry.computeBoundingSphere()` leaves a stale sphere — one left smaller than the moved vertices hides the mesh while it is still in view — and moving vertices in a shader leaves the CPU sphere untouched, so set `mesh.frustumCulled = false` on that one mesh, not scene-wide.
