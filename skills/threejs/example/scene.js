import * as THREE from './node_modules/three/build/three.module.js';

const canvas = document.querySelector('canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf1eee5);
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 30);
camera.position.set(2.4, 1.8, 3.8);
camera.lookAt(0, 0, 0);
const shape = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1.5, 1.5),
  new THREE.MeshStandardMaterial({ color: 0x226f91, roughness: 0.6 }));
scene.add(shape, new THREE.HemisphereLight(0xffffff, 0x64605a, 2));
const light = new THREE.DirectionalLight(0xffffff, 2);
light.position.set(3, 4, 1);
scene.add(light);
function draw() {
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
  camera.aspect = canvas.clientWidth / canvas.clientHeight;
  camera.updateProjectionMatrix();
  renderer.render(scene, camera);
}
let selected = false;
const button = document.querySelector('button');
function toggle() {
  selected = !selected;
  shape.material.color.setHex(selected ? 0xc45e28 : 0x226f91);
  button.textContent = selected ? 'Clear selection' : 'Select specimen';
  document.querySelector('output').textContent = selected ? 'Selected' : 'Unselected';
  draw();
}
button.addEventListener('click', toggle);
canvas.addEventListener('pointerup', event => {
  const box = canvas.getBoundingClientRect();
  const point = new THREE.Vector2(2 * (event.clientX - box.left) / box.width - 1,
    1 - 2 * (event.clientY - box.top) / box.height);
  const ray = new THREE.Raycaster();
  ray.setFromCamera(point, camera);
  if (ray.intersectObject(shape).length) toggle();
});
new ResizeObserver(draw).observe(canvas);
draw();
