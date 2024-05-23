
var socket = io();
var mouseCoords = document.getElementById('mouse_coords');

document.getElementById('video').addEventListener('mousemove', function(event) {
    var rect = event.target.getBoundingClientRect();
    var x = event.clientX - rect.left;
    var y = event.clientY - rect.top;

    socket.emit('mouse_move', { x: x, y: y });
});

document.getElementById('video').addEventListener('click', function(event) {
    var rect = event.target.getBoundingClientRect();
    var x = event.clientX - rect.left;
    var y = event.clientY - rect.top;

    socket.emit('mouse_click', { x: x, y: y });
});

socket.on('update_coords', function(data) {
    mouseCoords.textContent = `(${data.x}, ${data.y})`;
});

socket.on('response', function(data) {
    console.log(data.status);
});

