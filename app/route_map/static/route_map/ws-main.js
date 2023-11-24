/*

Websocket main js file: a base for page-specific
js files.

Hierachy:
  1. ol-main.js (do not depend on ws-main.js)
  2. ws-main.js (do not depend on ol-main.js)
  3. ws-ol-interaction.js (layer that mixes ol and ws apis together)
  4. page-sepecific js files that use the first three js files and build on top

*/

// connecting to websocket
const socket = new WebSocket(`${
    document.body.dataset.scheme === 'http' 
        ? 'ws' 
        : 'wss'
    }://${
        document.body.dataset.host
        }/ws/system-health/`);

// Make the function wait until the connection is made...
function waitForSocketConnection(socket, callback){
    setTimeout(
        function () {
            if (socket.readyState === 1) {
                console.log("Connection is made")
                if (callback != null){
                    callback();
                }
            } else {
                console.log("wait for connection...")
                waitForSocketConnection(socket, callback);
            }

        }, 5); // wait 5 milisecond for the connection...
}

 // Function to send data to websocket server
 function sendData(serverData, webSocket){
    waitForSocketConnection(webSocket, function(){
        console.log("message sent!!!");
        webSocket.send(JSON.stringify(serverData));
    });
}

function prepareAndSendRequest(event, action, name, ip) {
    // prevent page refreshing
    event.preventDefault();

    // Build our json data to send to WS Server
    const data = {
        "action": action,
        "data": {
            "system_name": name,
            "system_ip": ip
        }
    };

    // Send our data and request to WS Server
    sendData(data, socket);

}

// helper functions for sending out requests to WS Server and the loop for buttons
const addSpinnerButton = (buttonID) => {
    // Has sideeffects
    var spinner1 = document.createElement("span")
    spinner1.setAttribute("class", "spinner-grow spinner-grow-sm")
    spinner1.setAttribute("role", "status")
    spinner1.setAttribute("aria-hidden", "true")
    document.querySelector(`[id="${buttonID}"]`).prepend(spinner1);
}

const getCurrentDate = () => {
    // no side effects
    const date = Date.now();
    const formattedDate = new Date(date);

    return formattedDate.toISOString();
}

const getCurrentTime = () => {
    // no side effects
    const currentDate = new Date();
    const timeString = `${currentDate.getHours()}:${currentDate.getMinutes()}:${currentDate.getSeconds()}`

    return timeString;
}