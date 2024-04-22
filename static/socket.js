document.addEventListener('DOMContentLoaded', function() {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        const form = document.getElementById('send-message-form');
        form.onsubmit = function(e) {
            e.preventDefault();
            let messageInput = document.getElementById('message');
            let message = messageInput.value;
            socket.emit('send_message', {'message': message});
            messageInput.value = '';
        };
    });

    socket.on('receive_message', function(data) {
        const messages = document.getElementById('messages');
        const li = document.createElement('li');
        li.innerHTML = `<b>${data.username}</b>: ${data.message}`;
        messages.appendChild(li);
    });
});