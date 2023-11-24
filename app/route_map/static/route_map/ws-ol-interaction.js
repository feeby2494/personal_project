/* 

Layer to help abstract openlayer API to use with websockets main file

Hierachy:
  1. ol-main.js (do not depend on ws-main.js)
  2. ws-main.js (do not depend on ol-main.js)
  3. ws-ol-interaction.js (layer that mixes ol and ws apis together)
  4. page-sepecific js files that use the first three js files and build on top

*/

// need to get a list of all buttons
var buttons = document.getElementsByTagName('button');

// then add event listeners for each buttons
for(const server of buttons){
    // Run initial ping test for each
    window.addEventListener("load", (event) => {
        prepareAndSendRequest(event, "system info", server.dataset.name, server.dataset.ip);
        
    });

    // Add eventlisteners for additional clicks
    server.addEventListener("click", (event) => {
        switch (event.target.id) {
            case `ping-${server.dataset.name}`: 
                // add spinner to button
                addSpinnerButton(`${event.target.id}`);

                // send request for new test results to WS Server
                prepareAndSendRequest(event, "ping server", server.dataset.name, server.dataset.ip);
                break;
            
        }
        
    });
}

// helper functions for listening for WS responese from WS Server
const removeSpinnerButton = (buttonID) => {
    // Has sideeffects
    var button = document.querySelector(`[id="${buttonID}"]`);
    if (button.getElementsByTagName('span')[0]) {
        button.removeChild(button.getElementsByTagName('span')[0]);
    }
}



// adding eventlistener for websocket will update divs with the new html
socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    console.log("Message from websocket server");
    // Kills eventlisteners
    // document.querySelector(`#${data.selector}`).innerHTML = data.html

    /* 
    
    want to get all devices for pickup 
    all devices for drop off, 
        with customer location info
        with customer devices info
        with customer messages
        with customer date and time info
    
    */

    switch (data.action) {
        case "get customer devices": 
            // remove spinner from button
            removeSpinnerButton(`ping-${data.selector}`);

            // re-populate with results from WS Server 
            document.querySelector(`[id="ping-result-${data.selector}"]`).innerHTML = data.html;

            // update time in footer of card
            document.querySelector(`[id="time-ping-${data.selector}"]`).innerText = `Ping: last updated: ${getCurrentTime()}`;

            break;
        case "get customer pickup info": 
            // remove spinner from button
            removeSpinnerButton(`system-info-request-${data.selector}`);

            // re-populate with results from WS Server 
            document.querySelector(`[id="system-info-result-${data.selector}"]`).innerHTML = data.html;

            // update time in footer of card
            document.querySelector(`[id="time-info-${data.selector}"]`).innerText = `Info: last updated: ${getCurrentTime()}`;

            break;
        case "get customer messages":
            // remove spinner from button
            removeSpinnerButton(`system-info-request-${data.selector}`);

            // re-populate with results from WS Server 
            document.querySelector(`[id="system-info-result-${data.selector}"]`).innerHTML = data.html;

            // update time in footer of card
            document.querySelector(`[id="time-info-${data.selector}"]`).innerText = `Info: last updated: ${getCurrentTime()}`;

            break;
    }
});