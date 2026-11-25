# Shaders

Selected technical examples from CloudAI-X, adapted for the local edition.

## Uniforms

```javascript
const texture = await new THREE.TextureLoader().loadAsync("textures/diffuse.jpg");
texture.colorSpace = THREE.SRGBColorSpace; // a color image: decoded to linear when sampled

const material = new THREE.ShaderMaterial({
  uniforms: {
    floatValue: { value: 1.5 },
    vec3Value: { value: new THREE.Vector3(1, 2, 3) },
    colorValue: { value: new THREE.Color(0xff0000) }, // hex converted to the linear working space
    mat4Value: { value: new THREE.Matrix4() },
    mapValue: { value: texture },
  },
  // vertexShader and fragmentShader as usual
});
```

The matching GLSL declarations — sample the texture with `texture(mapValue, vUv)`:

```glsl
uniform float floatValue;
uniform vec3 vec3Value;
uniform vec3 colorValue;    // a THREE.Color arrives as vec3
uniform mat4 mat4Value;
uniform sampler2D mapValue;
```

Update a uniform by assigning `.value` from the frame loop (`material.uniforms.floatValue.value = 2.0;`); vectors and colors mutate in place (`material.uniforms.vec3Value.value.set(1, 2, 3);`). Never name a uniform `position`, `normal`, `uv`, `modelViewMatrix` or `cameraPosition` — three.js already declares those in the vertex shader, and the redeclaration is a compile error.

## Output Color and Tone Mapping

`THREE.Color` converts hex input from sRGB to the linear working color space, so a color uniform holds linear values. A ShaderMaterial writes its output as-is: tone mapping and the output color space conversion happen only if the fragment shader ends with the two includes:

```glsl
gl_FragColor = vec4(color, 1.0);
#include <tonemapping_fragment>
#include <colorspace_fragment>
```

`tonemapping_fragment` applies `renderer.toneMapping` (a no-op with `NoToneMapping`); `colorspace_fragment` encodes to `renderer.outputColorSpace` (`SRGBColorSpace` by default). Without them, mid-tone colors render darker than the same hex on a built-in material. Both chunks write `gl_FragColor`, so they require `glslVersion` unset. An 8-bit RGBA texture with `texture.colorSpace = THREE.SRGBColorSpace` decodes to linear on sampling, so sampled colors combine correctly with the includes in place. A `VideoTexture` does not: three.js uploads it without sRGB decoding and decodes it only inside built-in materials, so decode it yourself with `sRGBTransferEOTF(texture(videoMap, vUv))` (the ShaderMaterial prefix declares that function). Rendering into a render target, as inside an EffectComposer, both includes leave the color linear and `OutputPass` encodes it at the end.
