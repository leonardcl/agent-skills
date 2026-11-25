import * as THREE from './node_modules/three/build/three.module.js';

const canvas = document.querySelector('canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xeff4e8);
const camera = new THREE.OrthographicCamera(-3, 3, 2, -2, 0.1, 30);
camera.position.set(0, 3, 5);
camera.lookAt(0, 0, 0);
scene.add(new THREE.HemisphereLight(0xffffff, 0x769076, 2.2));
const key = new THREE.DirectionalLight(0xffffff, 2);
key.position.set(-2, 4, 3);
scene.add(key);
function mesh(geometry, color, x, y) {
  const object = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({color}));
  object.position.set(x, y, 0);
  scene.add(object);
  return object;
}
const pieces = [];
for (let i = 0; i < 4; i++) {
  mesh(new THREE.BoxGeometry(.94,.18,1), 0x49715a, i-1.5, 0);
  if (i) pieces.push(mesh(new THREE.OctahedronGeometry(.2), 0xf4ad37, i-1.5, .35));
}
const pawn = mesh(new THREE.SphereGeometry(.24, 20, 12), 0x30578e, -1.5, .38);
let position, collected;
function draw() {
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
  const aspect = canvas.clientWidth / canvas.clientHeight;
  const halfWidth = Math.max(2.35, 1.5 * aspect);
  camera.left = -halfWidth;
  camera.right = halfWidth;
  camera.top = halfWidth / aspect;
  camera.bottom = -camera.top;
  camera.updateProjectionMatrix();
  pawn.position.x = position - 1.5;
  pieces.forEach((piece,i) => { piece.visible = !collected.has(i+1); });
  document.querySelector('output').textContent = collected.size === 3
    ? 'Complete · 3 of 3' : 'Collected '+collected.size+' of 3';
  renderer.render(scene,camera);
}
function restart() { position=0; collected=new Set(); draw(); }
function move(step) {
  if (collected.size === 3) return;
  position = Math.max(0,Math.min(3,position+step));
  if (position) collected.add(position);
  draw();
  if (collected.size === 3) document.querySelector('#reset').focus();
}
document.querySelector('#left').onclick=()=>move(-1);
document.querySelector('#right').onclick=()=>move(1);
document.querySelector('#reset').onclick=restart;
window.addEventListener('keydown', e=>{
  if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
  e.preventDefault();
  if (!e.repeat) move(e.key === 'ArrowLeft' ? -1 : 1);
});
restart();
new ResizeObserver(draw).observe(canvas);
