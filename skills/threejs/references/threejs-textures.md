# Textures

Selected technical examples from CloudAI-X, adapted for the local edition.

## Color Space

Color management is on by default and every texture starts at `NoColorSpace`:

- LDR color images get `SRGBColorSpace`: `map`, `emissiveMap`, `specularMap`, sheen color and specular color maps, LDR matcaps, and canvas or video used as color.
- Scalar data keeps `NoColorSpace`: normal, bump, displacement, roughness, metalness, ambient-occlusion and alpha maps.
- HDR environments are `LinearSRGBColorSpace`; the HDR loaders set that themselves. GLTFLoader sets the color spaces of the textures it loads.

```javascript
const colorMap = new THREE.TextureLoader().load("color.jpg");
colorMap.colorSpace = THREE.SRGBColorSpace; // authored color image

const normalMap = new THREE.TextureLoader().load("normal.jpg");
// normalMap stays at NoColorSpace: it is data, not color
```

## Filtering, Mipmaps, Anisotropy

```javascript
const texture = new THREE.TextureLoader().load("diffuse.jpg");

// Minification (many texture pixels per screen pixel)
texture.minFilter = THREE.LinearMipmapLinearFilter; // default: trilinear blend between mip levels
texture.minFilter = THREE.NearestFilter; // hard pixel look, samples only the base level

// Magnification (texture magnified on screen)
texture.magFilter = THREE.LinearFilter; // default
texture.magFilter = THREE.NearestFilter; // pixelated

// Mipmaps are generated whenever generateMipmaps is true, whatever the filters.
// Turn generation off to save memory (UI sprites, data textures):
texture.generateMipmaps = false;
texture.minFilter = THREE.LinearFilter; // and do not request a mipmap filter

// Sharper at grazing angles; clamp to what the hardware supports
texture.anisotropy = renderer.capabilities.getMaxAnisotropy();
```
