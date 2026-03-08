const { createCanvas } = require('canvas');
const fs = require('fs');

const W = 800, H = 1200;
const canvas = createCanvas(W, H);
const ctx = canvas.getContext('2d');

// Background
const bg = ctx.createLinearGradient(0, 0, 0, H);
bg.addColorStop(0, '#05051a');
bg.addColorStop(0.5, '#0a0a2e');
bg.addColorStop(1, '#05051a');
ctx.fillStyle = bg;
ctx.fillRect(0, 0, W, H);

// Radial glow
const glow = ctx.createRadialGradient(W/2, H*0.42, 30, W/2, H*0.42, 450);
glow.addColorStop(0, 'rgba(0,150,255,0.1)');
glow.addColorStop(1, 'transparent');
ctx.fillStyle = glow;
ctx.fillRect(0, 0, W, H);

const cx = W / 2;
const scale = 1.0;
const offsetY = 60;

function tx(x) { return cx + x * scale; }
function ty(y) { return offsetY + y * scale; }

// Better athletic male figure - front view, arms slightly out, V-taper
// All coords as [x, y] relative to center
const outline = [
  // Top of head
  [0, 30],
  // Head right side
  [18, 35], [28, 50], [32, 70], [30, 90], [26, 105],
  // Jaw
  [22, 115], [15, 125],
  // Neck right
  [18, 135], [20, 148],
  // Trap / shoulder slope
  [40, 152], [70, 155], [100, 158], [125, 163],
  // Right deltoid cap (broad shoulder)
  [148, 168], [162, 178], [168, 192], [165, 208],
  // Right bicep
  [158, 225], [152, 250], [148, 270],
  // Right elbow
  [145, 290], [144, 300],
  // Right forearm
  [142, 320], [138, 345], [134, 370],
  // Right wrist/hand
  [130, 390], [126, 405], [124, 418], [128, 425], [122, 430],
  [118, 425], [120, 410],
  // Right side torso - lat spread then V taper
  [118, 390], [115, 360],
  // Lat insertion
  [118, 330], [122, 300], [125, 270],
  // V taper waist
  [118, 310], [108, 360], [95, 400], [82, 430],
  // Waist / hip
  [72, 455], [68, 470], [70, 485],
  // Right hip bone
  [78, 495],
  // Right quad outer
  [90, 520], [100, 560], [105, 600], [106, 630],
  // Right knee
  [104, 660], [102, 680], [100, 695],
  // Right calf
  [103, 720], [106, 760], [105, 800], [102, 840],
  // Right ankle
  [98, 870], [96, 885],
  // Right foot
  [88, 900], [82, 910], [110, 915], [118, 908], [105, 895],
  [98, 888],
  // Right inner leg going up
  [92, 870], [88, 840], [84, 800], [80, 760], [78, 720],
  [76, 695], [74, 680],
  // Right inner knee
  [73, 660],
  // Right inner thigh
  [70, 630], [66, 600], [60, 560], [52, 520],
  // Inner thigh top
  [42, 498], [35, 490],
  // Crotch center
  [10, 488], [0, 490], [-10, 488],
  // Left inner thigh
  [-35, 490], [-42, 498],
  [-52, 520], [-60, 560], [-66, 600], [-70, 630],
  [-73, 660], [-74, 680], [-76, 695],
  [-78, 720], [-80, 760], [-84, 800], [-88, 840],
  [-92, 870], [-98, 888],
  // Left foot
  [-105, 895], [-118, 908], [-110, 915], [-82, 910], [-88, 900],
  [-96, 885], [-98, 870],
  // Left calf
  [-102, 840], [-105, 800], [-106, 760], [-103, 720],
  [-100, 695], [-102, 680], [-104, 660],
  // Left knee / quad
  [-106, 630], [-105, 600], [-100, 560], [-90, 520],
  [-78, 495],
  // Left hip
  [-70, 485], [-68, 470], [-72, 455],
  // Left waist up
  [-82, 430], [-95, 400], [-108, 360], [-118, 310],
  [-125, 270], [-122, 300], [-118, 330],
  // Left lat
  [-115, 360], [-118, 390],
  // Left hand/wrist
  [-120, 410], [-118, 425], [-122, 430],
  [-128, 425], [-124, 418], [-126, 405], [-130, 390],
  // Left forearm
  [-134, 370], [-138, 345], [-142, 320],
  // Left elbow
  [-144, 300], [-145, 290],
  // Left bicep
  [-148, 270], [-152, 250], [-158, 225],
  // Left deltoid
  [-165, 208], [-168, 192], [-162, 178], [-148, 168],
  // Left shoulder / trap
  [-125, 163], [-100, 158], [-70, 155], [-40, 152],
  // Left neck
  [-20, 148], [-18, 135],
  // Left jaw / head
  [-15, 125], [-22, 115], [-26, 105],
  [-30, 90], [-32, 70], [-28, 50], [-18, 35],
];

// Ray casting for point-in-polygon
const txOutline = outline.map(p => [tx(p[0]), ty(p[1])]);

function isInside(px, py) {
  let inside = false;
  for (let i = 0, j = txOutline.length - 1; i < txOutline.length; j = i++) {
    const xi = txOutline[i][0], yi = txOutline[i][1];
    const xj = txOutline[j][0], yj = txOutline[j][1];
    if ((yi > py) !== (yj > py) && px < (xj - xi) * (py - yi) / (yj - yi) + xi) {
      inside = !inside;
    }
  }
  return inside;
}

// Draw filled silhouette with gradient
ctx.beginPath();
ctx.moveTo(txOutline[0][0], txOutline[0][1]);
for (let i = 1; i < txOutline.length; i++) {
  ctx.lineTo(txOutline[i][0], txOutline[i][1]);
}
ctx.closePath();

const bodyGrad = ctx.createLinearGradient(cx - 170, 0, cx + 170, H);
bodyGrad.addColorStop(0, '#00d4ff');
bodyGrad.addColorStop(0.25, '#0099cc');
bodyGrad.addColorStop(0.5, '#006688');
bodyGrad.addColorStop(0.75, '#004455');
bodyGrad.addColorStop(1, '#003344');
ctx.fillStyle = bodyGrad;
ctx.fill();

// Generate interior points for triangulation
const allPts = [];
// Outline points
for (const p of txOutline) allPts.push(p);

// Interior grid with jitter
const seed = 42;
let rng = seed;
function rand() { rng = (rng * 1664525 + 1013904223) & 0x7fffffff; return rng / 0x7fffffff; }

for (let gx = cx - 170; gx <= cx + 170; gx += 30) {
  for (let gy = 80; gy <= 980; gy += 28) {
    const jx = gx + (rand() - 0.5) * 16;
    const jy = gy + (rand() - 0.5) * 16;
    if (isInside(jx, jy)) {
      allPts.push([jx, jy]);
    }
  }
}

// Draw low-poly triangles using nearest-neighbor connections
function dist(a, b) { return Math.hypot(a[0] - b[0], a[1] - b[1]); }

// Draw wireframe edges
ctx.lineWidth = 0.4;

const drawnTriangles = new Set();

for (let i = 0; i < allPts.length; i++) {
  const p = allPts[i];
  // Find nearest neighbors
  const neighbors = [];
  for (let j = 0; j < allPts.length; j++) {
    if (j === i) continue;
    const d = dist(p, allPts[j]);
    if (d < 65 && d > 3) neighbors.push({ idx: j, d });
  }
  neighbors.sort((a, b) => a.d - b.d);
  const nearest = neighbors.slice(0, 5);

  for (const n of nearest) {
    const q = allPts[n.idx];
    const mx = (p[0]+q[0])/2, my = (p[1]+q[1])/2;
    if (!isInside(mx, my)) continue;

    // Edge
    ctx.strokeStyle = 'rgba(0, 220, 255, 0.18)';
    ctx.beginPath();
    ctx.moveTo(p[0], p[1]);
    ctx.lineTo(q[0], q[1]);
    ctx.stroke();

    // Triangle with third point
    for (const m of nearest) {
      if (m.idx <= n.idx) continue;
      const r = allPts[m.idx];
      if (dist(q, r) < 65) {
        const tmx = (p[0]+q[0]+r[0])/3, tmy = (p[1]+q[1]+r[1])/3;
        if (!isInside(tmx, tmy)) continue;
        const key = [i, n.idx, m.idx].sort().join(',');
        if (drawnTriangles.has(key)) continue;
        drawnTriangles.add(key);

        // Color variation based on position
        const normY = (tmy - 80) / 900;
        const h = 190 + normY * 15;
        const l = 25 + rand() * 20;
        ctx.fillStyle = `hsla(${h}, 80%, ${l}%, 0.12)`;
        ctx.beginPath();
        ctx.moveTo(p[0], p[1]);
        ctx.lineTo(q[0], q[1]);
        ctx.lineTo(r[0], r[1]);
        ctx.closePath();
        ctx.fill();
        ctx.strokeStyle = 'rgba(0, 200, 255, 0.15)';
        ctx.stroke();
      }
    }
  }
}

// Vertex dots
for (const p of allPts) {
  if (isInside(p[0], p[1])) {
    ctx.beginPath();
    ctx.arc(p[0], p[1], 1.2, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(0, 240, 255, 0.5)';
    ctx.fill();
  }
}

// Glowing outline
ctx.strokeStyle = 'rgba(0, 200, 255, 0.6)';
ctx.lineWidth = 1.2;
ctx.shadowColor = '#00ddff';
ctx.shadowBlur = 12;
ctx.beginPath();
ctx.moveTo(txOutline[0][0], txOutline[0][1]);
for (let i = 1; i < txOutline.length; i++) {
  ctx.lineTo(txOutline[i][0], txOutline[i][1]);
}
ctx.closePath();
ctx.stroke();
ctx.shadowBlur = 0;

// Floating particles
for (let i = 0; i < 300; i++) {
  const px = cx + (rand() - 0.5) * 600;
  const py = 30 + rand() * 950;
  if (!isInside(px, py)) {
    const size = 0.3 + rand() * 1.8;
    ctx.beginPath();
    ctx.arc(px, py, size, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(0, 200, 255, ${0.05 + rand() * 0.25})`;
    ctx.fill();
  }
}

// Title
ctx.font = 'bold 30px sans-serif';
ctx.textAlign = 'center';
ctx.fillStyle = 'rgba(0, 210, 255, 0.6)';
ctx.shadowColor = '#00ccff';
ctx.shadowBlur = 25;
ctx.fillText('A T H L E T I C', cx, H - 70);
ctx.font = '13px sans-serif';
ctx.fillStyle = 'rgba(0, 210, 255, 0.35)';
ctx.fillText('G E O M E T R I C   F O R M', cx, H - 45);
ctx.shadowBlur = 0;

// Save
const out = '/home/ubuntu/.openclaw/workspaces/main/athletic_figure.png';
fs.writeFileSync(out, canvas.toBuffer('image/png'));
console.log('Done:', out);
