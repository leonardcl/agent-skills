# Three.js workflows

## threejs-animation

Use a local clip on the same root passed to the mixer. Advance it once per frame with elapsed seconds. Check pose at start, halfway and after replay before tuning blends. See the [technical examples](threejs-animation.md).

## threejs-asset-pipeline

Keep the input asset intact. Record file size, draw calls, triangle count and visible appearance before compression. Choose a decoder available locally and compare the resulting scene against the source asset. See the [technical examples](threejs-asset-pipeline.md).

## threejs-fundamentals

Start with one visible mesh and a known camera direction. Resize the renderer and update the projection matrix together. If a canvas is blank, try a simple unlit material, check frustum and geometry, then restore lighting. See the [technical examples](threejs-fundamentals.md).

## threejs-geometry

Compare changing a single mesh with drawing many repeated copies. Reuse geometry, mark changed instance data for upload and measure draw calls at the same camera position. See the [technical examples](threejs-geometry.md).

## threejs-interaction

Compute pointer coordinates relative to the canvas bounds. Test picking before and after resizing and verify the selected object matches the face under the pointer. See the [technical examples](threejs-interaction.md).

## threejs-lighting

Choose a key light and target before adding fill. If the object casts no shadow, check the renderer, light, caster, receiver and shadow camera in that order. See the [technical examples](threejs-lighting.md).

## threejs-loaders

Use a known local asset, show a pending state and provide a visible error for a missing file. Distinguish loading completion from a visible, correctly scaled model. See the [technical examples](threejs-loaders.md).

## threejs-materials

Match the material model to the lighting available. Clone only when an edit must affect one object independently. Dispose unused resources once the last consumer releases them. See the [technical examples](threejs-materials.md).

## threejs-performance

Compare the same camera path, content and canvas size. Lower pixel ratio to test fill cost, then vary object count to test submission overhead. Record which change moved the measurement. See the [technical examples](threejs-performance.md).

## threejs-postprocessing

Render the unprocessed scene first. Add passes one at a time and compare output at identical exposure. Keep output conversion at the intended final stage and resize all dependent render targets. See the [technical examples](threejs-postprocessing.md).

## threejs-react-three-fiber

Keep frame updates inside the canvas. A continuous transform belongs in the frame loop, while a selected object ID belongs to application state. Dispose externally shared assets only after their consumers unmount. See the [technical examples](threejs-react-three-fiber.md).

## threejs-shaders

Start with a constant color, then add one uniform and vary it through a known range. Confirm output color handling before debugging a material that looks washed out. See the [technical examples](threejs-shaders.md).

## threejs-textures

Mark color images and data maps according to their meaning. Compare a textured surface front-on and at a grazing angle and check filtering before increasing texture size. See the [technical examples](threejs-textures.md).
