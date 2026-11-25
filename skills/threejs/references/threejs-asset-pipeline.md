# Asset pipeline

Selected technical examples from CloudAI-X, adapted for the local edition.

## Geometry Compression

Use an installed glTF Transform CLI for these optional offline conversions. Three codecs with different tradeoffs — pick per model, not per project:

- **Draco** (`--compress draco`, `draco` command): compresses triangle-mesh geometry only — animation, morph targets, textures, points and lines are not compressed. Runtime: DRACOLoader.
- **Meshopt** (`--compress meshopt`, `meshopt` command): compresses point, line and triangle geometry, morph targets and animation tracks, and decodes very quickly; pair it with lossless gzip or brotli over the wire. Runtime: MeshoptDecoder.
- **Quantize** (`quantize` command): stores float attributes as 8- or 16-bit integers under KHR_mesh_quantization — smaller on disk and in GPU memory, and no decoder to wire; GLTFLoader reads quantized attributes natively.

```bash
gltf-transform draco model.glb model.opt.glb --method edgebreaker --quantize-position 14
gltf-transform meshopt model.glb model.opt.glb --level high
gltf-transform quantize model.glb model.opt.glb
gltf-transform gzip model.opt.glb
```

`gzip` writes `model.opt.glb.gz` next to its input; serve it with `Content-Encoding: gzip` and the browser decompresses it transparently. It adds little on top of Draco or JPEG textures, and earns the most on top of meshopt and quantize.

Make `draco`, `meshopt` or `optimize` the last command in a chain: every other command that rewrites the model decodes Draco and meshopt geometry when it reads the file (it warns "Decoded KHR_draco_mesh_compression. Further compression will be lossy.") and writes it back uncompressed.

## Loader Setup for Each Output

The pipeline choice decides the loader wiring. The Draco decoder and the Basis transcoder load from the three package by default — call `setDecoderPath` or `setTranscoderPath` only when you host those files yourself, and then pin the path to the three release you ship. Create one KTX2Loader for the app and share it between GLTFLoaders: each active instance loads its own transcoder and workers, and three.js warns when several are active.

```javascript
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { DRACOLoader } from "three/addons/loaders/DRACOLoader.js";
import { KTX2Loader } from "three/addons/loaders/KTX2Loader.js";
import { MeshoptDecoder } from "three/addons/libs/meshopt_decoder.module.js";

// Wire every codec the pipeline may emit; a missing one throws at load time
const gltfLoader = new GLTFLoader()
  .setDRACOLoader(new DRACOLoader()) // KHR_draco_mesh_compression
  .setMeshoptDecoder(MeshoptDecoder) // EXT_meshopt_compression
  .setKTX2Loader(new KTX2Loader().detectSupport(renderer)); // KHR_texture_basisu

const gltf = await gltfLoader.loadAsync("model.opt.glb");
scene.add(gltf.scene);
```

What each missing piece throws: a Draco file without a DRACOLoader ("No DRACOLoader instance provided"), a meshopt file without a decoder ("setMeshoptDecoder must be called before loading compressed files"), a KTX2 file without a KTX2Loader ("setKTX2Loader must be called before loading KTX2 textures"), and a KTX2Loader that never ran `detectSupport` ("Missing initialization with `.detectSupport( renderer )`"). WebP and AVIF textures, quantized attributes and EXT_mesh_gpu_instancing need none of this.
