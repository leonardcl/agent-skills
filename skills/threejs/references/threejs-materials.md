# Materials

Selected technical examples from CloudAI-X, adapted for the local edition.

## MeshStandardMaterial (PBR)

Physically-based rendering. Recommended for realistic results.

```javascript
const map = await new THREE.TextureLoader().loadAsync("color.jpg");
map.colorSpace = THREE.SRGBColorSpace;
const ormMap = await new THREE.TextureLoader().loadAsync("orm.jpg"); // glTF ORM: ao red, roughness green, metalness blue; scalar: keep default

const material = new THREE.MeshStandardMaterial({
  color: 0xffffff, // multiplied with the map
  roughness: 1.0, // 0 = mirror, 1 = fully diffuse; multiplied by roughnessMap (green)
  metalness: 1.0, // 0 = dielectric, 1 = metal; multiplied by metalnessMap (blue), so keep 1 with a map
  map,
  roughnessMap: ormMap,
  metalnessMap: ormMap,
  normalMap: null, // surface detail; scale with normalScale (a Vector2)
  aoMap: ormMap, // ambient occlusion (red); intensity with aoMapIntensity
  displacementMap: null, // vertex displacement; scale with displacementScale, offset with displacementBias
  emissive: 0x000000,
  emissiveIntensity: 1,
  emissiveMap: null, // sRGB
  envMap: null, // or rely on scene.environment (see below)
  fog: true,
});
```

`lightMap` (with `lightMapIntensity`) bakes indirect light the same way aoMap bakes occlusion; an HDR or EXR lightMap is `LinearSRGBColorSpace`, which the loaders set.

### UV channels: aoMap and lightMap read the channel you pick

Every UV-mapped texture samples the attribute selected by `texture.channel`: 0 reads `uv` (the default), 1 reads `uv1`, 2 reads `uv2`, 3 reads `uv3`. aoMap and lightMap need no second UV set - they sample `uv` unless you change `channel`. GLTFLoader loads `TEXCOORD_1` as `uv1` and sets `channel` itself.

```javascript
const aoMap = await new THREE.TextureLoader().loadAsync("ao.jpg"); // scalar: keep default
const material = new THREE.MeshStandardMaterial({ aoMap }); // samples uv: no extra attribute needed

// Alternative for a separate unwrap (a baked AO or light map): copy your baker's u,v pairs into uv1
const bakedUv = new THREE.Float32BufferAttribute(mesh.geometry.attributes.position.count * 2, 2); // zero-filled until you copy them in
mesh.geometry.setAttribute("uv1", bakedUv); mesh.material = material;
aoMap.channel = 1; // this material now samples uv1 instead of uv
```

## Runtime Changes, Cloning, Disposal

```javascript
mesh.material.color.set(0xff0000); // uniform values: no recompile needed
mesh.material.roughness = 0.8;

// material.needsUpdate = true after changing a setting compiled into the shader:
// transparent, side, blending, flatShading, vertexColors, dithering, premultipliedAlpha, alphaHash,
// adding or removing a map slot, or shader source (alphaTest and envMap recompile by themselves)

const clone = mesh.material.clone(); // copies values; map slots share their textures, ShaderMaterial uniforms are cloned
```

Dispose a material nothing else uses: `material.dispose()` releases its GPU programs, which are deleted once no other material uses them; textures need their own `texture.dispose()`.

Performance, in order of impact:

1. Share one material instance across meshes - the renderer re-uploads material uniforms whenever consecutive draws switch material (identical settings already share one compiled program).
2. Prefer opaque rendering: transparent materials are sorted back to front by object and drawn after the opaque ones, still writing depth unless `depthWrite: false`, so stacked layers overdraw and intersecting ones misorder; for cutouts, alphaTest keeps the material opaque, so it draws in the opaque pass, correctly in any order.
3. Pick the cheapest material that looks right: Basic, then Lambert, Phong, Standard, Physical.
