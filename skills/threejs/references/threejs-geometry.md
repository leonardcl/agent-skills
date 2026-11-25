# Geometry

Selected technical examples from CloudAI-X, adapted for the local edition.

## BufferGeometry

The base class of every geometry: typed arrays of vertex data plus an optional index. Attributes are named buffers of `itemSize` values per vertex; `position`, `normal` and `uv` are the ones materials read by default.

### Custom BufferGeometry

```javascript
const geometry = new THREE.BufferGeometry();

// Four vertices, three floats each (x, y, z)
const vertices = new Float32Array([-1, -1, 0, 1, -1, 0, 1, 1, 0, -1, 1, 0]);
geometry.setAttribute("position", new THREE.BufferAttribute(vertices, 3));

// Indices reuse vertices across the two triangles
const indices = new Uint16Array([0, 1, 2, 0, 2, 3]);
geometry.setIndex(new THREE.BufferAttribute(indices, 1));

// Normals drive the lighting, UVs address textures
const normals = new Float32Array([0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]);
geometry.setAttribute("normal", new THREE.BufferAttribute(normals, 3));
const uvs = new Float32Array([0, 0, 1, 0, 1, 1, 0, 1]);
geometry.setAttribute("uv", new THREE.BufferAttribute(uvs, 2));
// Optional per-vertex colors, rendered with material.vertexColors = true
const colors = new Float32Array([1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0]);
geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));

scene.add(new THREE.Mesh(geometry, new THREE.MeshBasicMaterial({ vertexColors: true })));
```

### Attribute Types

```javascript
const count = 4;
const geometry = new THREE.BufferGeometry();
// Float32 for positions, normals, UVs and floating-point colors
geometry.setAttribute("position", new THREE.BufferAttribute(new Float32Array(count * 3), 3));
// Uint16 indices address vertices 0 to 65534 (65535 is the primitive-restart value); setIndex([...]) with a plain array picks Uint16 or Uint32 itself
geometry.setIndex(new THREE.BufferAttribute(new Uint16Array(count), 1));
// Uint8 colors need normalized = true (third argument) so bytes reach the shader as 0.0-1.0
geometry.setAttribute("color", new THREE.BufferAttribute(new Uint8Array(count * 3), 3, true));
```

### Updating a BufferGeometry

```javascript
const geometry = new THREE.PlaneGeometry(2, 2);
const positions = geometry.attributes.position;
positions.setXYZ(0, -2, -2, 0); // overwrite vertex 0
positions.getX(0); // read single components with getX / getY / getZ
positions.needsUpdate = true; // upload the change; an array cannot grow after its first render, so allocate the maximum and use geometry.setDrawRange(0, n)
geometry.computeVertexNormals(); // normals must match the new positions
geometry.computeBoundingBox(); // bounding volumes drive frustum culling and raycasting
geometry.computeBoundingSphere();
```

### Interleaved Buffers

```javascript
// One buffer holding position (3 floats) and uv (2 floats) per vertex
const interleavedBuffer = new THREE.InterleavedBuffer(
  new Float32Array([
    -1, -1, 0, 0, 0, 1, -1, 0, 1, 0, 1, 1, 0, 1, 1, -1, 1, 0, 0, 1, // four vertices: xyz + uv
  ]),
  5, // stride: floats per vertex
);
const geometry = new THREE.BufferGeometry();
geometry.setAttribute("position", new THREE.InterleavedBufferAttribute(interleavedBuffer, 3, 0));
geometry.setAttribute("uv", new THREE.InterleavedBufferAttribute(interleavedBuffer, 2, 3));
geometry.setIndex([0, 1, 2, 0, 2, 3]); // two triangles over the four vertices
// BufferGeometryUtils.interleaveAttributes([position, normal, uv]) packs existing attributes this way
```

## InstancedMesh

One draw call for many copies of one geometry, each with its own transform.

```javascript
const geometry = new THREE.BoxGeometry(0.2, 0.2, 0.2);
const material = new THREE.MeshBasicMaterial(); // multiplies by instance colors; MeshNormalMaterial ignores them
const count = 1000;
const instancedMesh = new THREE.InstancedMesh(geometry, material, count);
const dummy = new THREE.Object3D();
for (let i = 0; i < count; i++) {
  dummy.position.set((Math.random() - 0.5) * 20, (Math.random() - 0.5) * 20, (Math.random() - 0.5) * 20);
  dummy.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, 0);
  dummy.scale.setScalar(0.5 + Math.random());
  dummy.updateMatrix();
  instancedMesh.setMatrixAt(i, dummy.matrix);
}
instancedMesh.instanceMatrix.needsUpdate = true; // needed after changes once the mesh has rendered; harmless before

// setColorAt creates instanceColor on first use; flag it after the loop
for (let i = 0; i < count; i++) {
  instancedMesh.setColorAt(i, new THREE.Color(Math.random(), Math.random(), Math.random()));
}
instancedMesh.instanceColor.needsUpdate = true;

scene.add(instancedMesh);
```

At runtime, update and raycast instances like this:

```javascript
// mesh here is an InstancedMesh
const matrix = new THREE.Matrix4();
const index = 7;
mesh.getMatrixAt(index, matrix);
matrix.setPosition(0, 2, 0); // move just this instance
mesh.setMatrixAt(index, matrix);
mesh.instanceMatrix.needsUpdate = true; // flag after any batch of setMatrixAt calls
mesh.computeBoundingSphere(); // instances moved: refresh the bounds used by frustum culling and raycasting

// Raycasting reports which instance was hit
const raycaster = new THREE.Raycaster();
const hits = raycaster.intersectObject(mesh);
if (hits.length > 0) {
  const instanceId = hits[0].instanceId; // undefined for a non-instanced object
}
```
