# Three.js game creation workflows

## threejs-3d-generator

Build a local prop from primitives or import a cleared GLB already on disk. Check scale against the player, pivot at the intended contact point, material count and missing textures. Keep the proxy playable if final art is absent.

## threejs-aaa-graphics-builder

Choose a visual target for the game's actual viewing distance. Separate silhouette, light direction and material response. Compare a repeatable gameplay frame before and after a lighting change, then measure frame time at the same resolution.

## threejs-audio-generator

Map each audible cue to a game event. For a collectible, synthesize a short local tone triggered by a user gesture or use cleared audio. Check mute, replay and that one pickup emits only one cue.

## threejs-debug-profiler

Keep a deterministic input sequence. If the world is blank, verify a plain mesh and camera first. If rendering works but play stalls, compare simulation updates with render timing under the same sequence.

## threejs-game-director

Write the one-minute play loop as start, choice, visible feedback, finish and replay. Build the simplest playable path before commissioning assets. A player must be able to start and finish using only the included controls.

## threejs-game-ui-designer

Make goal, current score and the available action visible in each state. Move focus to a usable control after completion. Verify restart by keyboard and touch without leaving stale victory text.

## threejs-gameplay-systems

Store position, collectibles and score in one game state. Handle input exactly once per intended action. Process collection before testing the win condition and protect already-collected items from double scoring.

## threejs-image-generator

Make a local texture or icon with a canvas or cleared input. Test transparency, rendering at actual size, high-contrast silhouette and graceful fallback if an asset is unavailable.

## threejs-qa-release

Replay a normal run, an early restart and rapid repeated inputs. Capture start, mid-game, finish and reset with the same viewport. Count resources or listeners across resets and report which devices actually ran.
