# Animation

Selected technical examples from CloudAI-X, adapted for the local edition.

## AnimationMixer

```javascript
const track = new THREE.NumberKeyframeTrack(".rotation[y]", [0, 2], [0, Math.PI * 2]);
const clip = new THREE.AnimationClip("spin", 2, [track]);

// One mixer per animated root; it reaches the root and all descendants
const mixer = new THREE.AnimationMixer(mesh);
const action = mixer.clipAction(clip); // cached: calling it again for this clip and root returns the same action
action.play();

const timer = new THREE.Timer();
timer.connect(document);

function animate() {
  timer.update();
  mixer.update(timer.getDelta()); // required: advances every active action
  renderer.render(scene, camera);
}

renderer.setAnimationLoop(animate);

// Events fire on the mixer while it updates; "finished" needs LoopOnce or finite repetitions
mixer.addEventListener("finished", (e) => console.log("finished:", e.action.getClip().name));
mixer.addEventListener("loop", (e) => console.log("looped:", e.action.getClip().name));
```

## Blending Clips by Weight

```javascript
const mixer = new THREE.AnimationMixer(mesh);
const idleClip = new THREE.AnimationClip("idle", 2, [
  new THREE.NumberKeyframeTrack(".position[y]", [0, 1, 2], [0, 0.05, 0]),
]);
const runClip = new THREE.AnimationClip("run", 1, [
  new THREE.NumberKeyframeTrack(".position[y]", [0, 0.5, 1], [0, 0.3, 0]),
]);

const idle = mixer.clipAction(idleClip).play();
const run = mixer.clipAction(runClip).play();

// Both sample every frame; the weights mix their poses
function setBlend(speed) {
  const t = Math.min(speed / 5, 1); // 0 = idle, 5 and up = full run
  idle.setEffectiveWeight(1 - t);
  run.setEffectiveWeight(t);
}

setBlend(2.5); // half idle, half run
```

### Additive Animation

```javascript
const mixer = new THREE.AnimationMixer(mesh);
const walkClip = new THREE.AnimationClip("walk", 1, [
  new THREE.NumberKeyframeTrack(".rotation[y]", [0, 1], [0, Math.PI]),
]);
const breathClip = new THREE.AnimationClip("breath", 2, [
  new THREE.NumberKeyframeTrack(".position[y]", [0, 1, 2], [0, 0.02, 0]),
]);

// Re-bases every track on its frame 0 and marks the clip additive
THREE.AnimationUtils.makeClipAdditive(breathClip);

mixer.clipAction(walkClip).play(); // normal base clip
mixer.clipAction(breathClip).play(); // adds its offsets on top of the base pose
```
