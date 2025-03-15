from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/cube", response_class=HTMLResponse)
async def cube_page(request: Request):
    return templates.TemplateResponse("cube.html", {"request": request})

#Create a static folder and a templates folder in the same directory as your python file.
#Inside static create a javascript file called cube.js
#Inside templates create index.html and cube.html

#static/cube.js:
"""
const canvas = document.getElementById('cubeCanvas');
const ctx = canvas.getContext('2d');

let rotationX = 0;
let rotationY = 0;
let rotationZ = 0;

function updateRotation() {
    rotationX = parseFloat(document.getElementById('rotationX').value);
    rotationY = parseFloat(document.getElementById('rotationY').value);
    rotationZ = parseFloat(document.getElementById('rotationZ').value);
    drawCube();
}

function project(point, rotationX, rotationY, rotationZ) {
    const cosX = Math.cos(rotationX);
    const sinX = Math.sin(rotationX);
    const cosY = Math.cos(rotationY);
    const sinY = Math.sin(rotationY);
    const cosZ = Math.cos(rotationZ);
    const sinZ = Math.sin(rotationZ);

    let x = point[0];
    let y = point[1];
    let z = point[2];

    // Rotation around X-axis
    let y1 = y * cosX - z * sinX;
    let z1 = y * sinX + z * cosX;
    y = y1;
    z = z1;

    // Rotation around Y-axis
    let x2 = x * cosY + z * sinY;
    let z2 = -x * sinY + z * cosY;
    x = x2;
    z = z2;

    // Rotation around Z-axis
    let x3 = x * cosZ - y * sinZ;
    let y3 = x * sinZ + y * cosZ;
    x = x3;
    y = y3;

    // Perspective projection
    const scale = 200 / (z + 400); // Adjust perspective
    return [x * scale + canvas.width / 2, y * scale + canvas.height / 2];
}

function drawCube() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const vertices = [
        [-100, -100, -100],
        [100, -100, -100],
        [100, 100, -100],
        [-100, 100, -100],
        [-100, -100, 100],
        [100, -100, 100],
        [100, 100, 100],
        [-100, 100, 100]
    ];

    const edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],
        [4, 5], [5, 6], [6, 7], [7, 4],
        [0, 4], [1, 5], [2, 6], [3, 7]
    ];

    ctx.strokeStyle = 'black';
    ctx.lineWidth = 2;

    for (const edge of edges) {
        const p1 = project(vertices[edge[0]], rotationX * Math.PI / 180, rotationY * Math.PI / 180, rotationZ * Math.PI / 180);
        const p2 = project(vertices[edge[1]], rotationX * Math.PI / 180, rotationY * Math.PI / 180, rotationZ * Math.PI / 180);

        ctx.beginPath();
        ctx.moveTo(p1[0], p1[1]);
        ctx.lineTo(p2[0], p2[1]);
        ctx.stroke();
    }
}

drawCube(); // Initial draw

document.getElementById('rotationX').addEventListener('input', updateRotation);
document.getElementById('rotationY').addEventListener('input', updateRotation);
document.getElementById('rotationZ').addEventListener('input', updateRotation);
"""

#templates/index.html:
"""
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI Cube</title>
</head>
<body>
    <h1>Welcome to the Cube App!</h1>
    <a href="/cube">View Cube</a>
</body>
</html>
"""

#templates/cube.html:
"""
<!DOCTYPE html>
<html>
<head>
    <title>Rotatable Cube</title>
</head>
<body>
    <h1>Rotatable Cube</h1>
    <canvas id="cubeCanvas" width="600" height="400" style="border: 1px solid black;"></canvas>
    <br>
    Rotation X: <input type="range" id="rotationX" min="-180" max="180" value="0"><span id="xValue">0</span><br>
    Rotation Y: <input type="range" id="rotationY" min="-180" max="180" value="0"><span id="yValue">0</span><br>
    Rotation Z: <input type="range" id="rotationZ" min="-180" max="180" value="0"><span id="zValue">0</span><br>

    <script src="/static/cube.js"></script>
    <script>
        document.getElementById('rotationX').addEventListener('input', function() {
            document.getElementById('xValue').textContent = this.value;
        });

        document.getElementById('rotationY').addEventListener('input', function() {
            document.getElementById('yValue').textContent = this.value;
        });

        document.getElementById('rotationZ').addEventListener('input', function() {
            document.getElementById('zValue').textContent = this.value;
        });

    </script>
</body>
</html>
"""
