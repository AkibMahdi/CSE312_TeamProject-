document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect('http://localhost:5000');

    // Get references to DOM elements
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatLog = document.getElementById('chat-log');

    // Function to append a message to the chat log
    function appendMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.innerText = message;
        chatLog.appendChild(messageElement);
    }

    // Event listener for send button click
    sendButton.addEventListener('click', () => {
        const message = messageInput.value;
        if (message.trim() !== '') {
            socket.emit('message', { message: message });
            messageInput.value = ''; // Clear input field
        }
    });

    // Event listener for receiving messages from the server
    socket.on('message', (data) => {
        appendMessage(data.message);
    });
});