/*
    Variables
*/

// Connect to WebSockets server
const myWebSocket = new WebSocket(`${
    document.body.dataset.scheme === 'http' 
        ? 'ws' 
        : 'wss'
    }://${
        document.body.dataset.host
        }/ws/social-network/`);

const inputAuthor = document.querySelector("#message-form__author");
const inputText = document.querySelector("#message-form__text");
const inputSubmit = document.querySelector("#message-form__submit");

/** 
 * Send data to Websocket server
 * @param {string} message
 * @param {WebSocket} webSocket
 * @return {void}
*/

function sendData(message, webSocket) {
    webSocket.send(JSON.stringify(message));
}

/**
 * Send new Message
 * @param {Event} event
 * @return {void}
 */

function sendNewMessage(event) {
    event.preventDefault();
    // Prepare the information we will send
    const newData = {
        "action": "add message",
        "data": {
            "author": inputAuthor.value,
            "text": inputText.value
        }
    };

    // Send the data to the server
    sendData(newData, myWebSocket);
    // Clear message form
    inputText.value = "";
}

/*
    Events
*/

// Event when a new message is received by WebSockets
myWebSocket.addEventListener("message", (event) => {
    // Parse the data received
    const data = JSON.parse(event.data);
    // Renders the HTML received from the Cunsumer
    document.querySelector(data.selector).innerHTML = data.html;
});

// Send new message when you click on Submit
inputSubmit.addEventListener("click", sendNewMessage);