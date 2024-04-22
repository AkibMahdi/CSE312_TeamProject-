var socket = io();
socket.on('connect', function() {
    console.log('Connected');
});

socket.on('message', function(msg) {
    var item = document.createElement('li');
    item.textContent = msg;
    document.getElementById('messages').appendChild(item);
    window.scrollTo(0, document.body.scrollHeight);
});

function sendMessage() {
    var input = document.getElementById('message-input');
    socket.emit('message', input.value);
    input.value = '';
}

document.getElementById('message-input').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
        e.preventDefault();
    }
});