/*
    Variables
*/

// Take care of displaying map when first button clicked

    const mapButton = document.querySelector(`[data-action="switch to map view"]`);
    const mapContainer = document.querySelector(`[id="map-container"]`);
    const viewContainer = document.querySelector(`[id="view"]`);

    //Show view funct

    const showView = () => {
        viewContainer.classList.remove('d-none')
        viewContainer.classList.add('d-block')
    }

    const hideView = () => {
        viewContainer.classList.remove('d-block')
        viewContainer.classList.add('d-none')
    }

    //Show map funct

    const showMap = () => {
        mapContainer.classList.remove('d-none');
        mapContainer.classList.add('d-block');

        // hide view div
        if (viewContainer.classList.contains("d-block")) {
            hideView();
        }
    }

    //Hide map funct
    const hideMap = () => {
        mapContainer.classList.remove('d-block');
        mapContainer.classList.add('d-none');

        // hide view div
        if (viewContainer.classList.contains("d-none")) {
            showView();
        }
    }

    //event listener on button
    mapButton.addEventListener("click", (event) => {
        if (mapContainer.classList.contains('d-none')){
            console.log("showing map")
            showMap();
        }
        else {
            hideMap();
            console.log("hiding map")
        }
    });



// Connect to WebSockets server
const socket = new WebSocket(`${
    document.body.dataset.scheme === 'http' 
        ? 'ws' 
        : 'wss'
    }://${
        document.body.dataset.host
        }/ws/route-map/`);

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

// const switchToMap = document.querySelector("[data-action='switch to map view']");
// const switchToList = document.querySelector("[data-action='switch to list view']");
// const switchToNewOrder = document.querySelector("[data-action='switch to new order view']");

// Function to send data to websocket server
function sendData(serverData, webSocket){
    waitForSocketConnection(webSocket, function(){
        console.log("message sent!!!");
        webSocket.send(JSON.stringify(serverData));
    });
}

// for regular buttons and forms
function prepareAndSendRequest(event, action, create_id, dataset, value, selector) {
    // prevent page refreshing
    event.preventDefault();

    // Build our json data to send to WS Server
    const data = {
        "action": action,
        "data": dataset,
        "create_id": create_id,
        "value": value,
        "selector": selector,
    };

    // Send our data and request to WS Server
    sendData(data, socket);

}

// for final submission button for repairs
const submitRepairs = (event, repairs) => {
    // prevent page refreshing
    event.preventDefault();

    // Build our json data to send to WS Server
    const data = {
        "action": event.target.dataset.action,
        "data": repairs
    };

    // Send our data and request to WS Server
    sendData(data, socket);

}

/*
    Events
*/
// used to give new ids to new repair forms
var create_id = 0;

const initializeEventListenerToButtons = () => {

    // need to get a list of all buttons
    var buttons = document.querySelectorAll("[data-request-type='ws']")
    

    // then add event listeners for each buttons
    for(const element of buttons){
        // Add event listener flag
        element.dataset.eventListener = "True";

        if (element.tagName === "SELECT") {
            console.log("is select")
            
            element.addEventListener("change", (event) => {

                
                
                // send request for the action in the button's dataset
                prepareAndSendRequest(event, event.target.dataset.action, create_id, event.target.dataset, event.target.value, event.target.id);      
            });
        } else {
            console.log("is button")
            element.addEventListener("click", (event) => {

                // send request for the action in the button's dataset
                prepareAndSendRequest(event, event.target.dataset.action, create_id, event.target.dataset, event.target.value, event.target.id);      
            });
        }
        
    }

    // Submit button for submiting work order, then all orders, then clearing form, deleting all repair forms
    if (document.querySelector("[data-request-type='submit_order']")) {
        var submit_order = document.querySelector("[data-request-type='submit_order']")

        // Add event listener flag
        submit_order.dataset.eventListener = "True";

        const submission_obj = []

        console.log("We have submit buttons:" + submit_order)

        submit_order.addEventListener('click', (event) => {
            // prevent page refreshing
            event.preventDefault();

            

            console.log("button clicked " + counter)

            const repairFormElements = document.querySelectorAll("[data-submission-id]");
            var counter = 0;
            // our object we will send to WS server to add all repairs to order
            const repairs = {}

            console.log("button clicked " + counter)
            

            for (const element of repairFormElements) {

                console.log("We have repair forms:" + element)

                if (element.dataset.submissionId == counter) {
                    // current counter matches the submissionID, so we are on the same repair
                    if (repairs[counter]) {
                        // Array is already made, just add element's value to it
                        repairArray.push(element.value)
                        repairs[counter] = repairArray
                    } else {
                        // First time array is made for this repair with said submissionID
                        var repairArray = []
                        repairs[counter] = []

                        repairArray.push(element.value)
                        repairs[counter] = repairArray
                    }
                } else {
                    // current counter deosn't match the submissionID, time to itterate counter
                    // interate counter
                    counter++
                    if (repairs[counter]) {
                    // Array is already made, just add element's value to it
                        repairArray.push(element.value)
                        repairs[counter] = repairArray
                  
                    } else {
                        // First time array is made for this repair with said submissionID
                        var repairArray = []
                        repairs[counter] = []

                        repairArray.push(element.value)
                        repairs[counter] = repairArray
                    }
                }    
                    
            }
            // send request for the action in the button's dataset
            submitRepairs(event, repairs);      
        })
    }
    
}

const removeListeners = () => {
    // need to get a list of all buttons
    var buttons = document.querySelectorAll("[data-event-listener='True']")

    for(const element of buttons) {
        let oldElement = element
        let newElement = element.cloneNode(true);

        // keep selected option from old elements if it's a select tag
        newElement.value = oldElement.value;

        // set eventListener flag to flase on new element
        newElement.dataset.eventListener = "False";
        
        element.parentNode.replaceChild(newElement, oldElement);
    }
    console.log('Removed all listners');
}

// Add initial eventlisteners
initializeEventListenerToButtons();


// adding eventlistener for websocket will update divs with the new html
socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    console.log("Message from websocket server");
    // Kills eventlisteners
    // document.querySelector(`#${data.selector}`).innerHTML = data.html

    console.log(data.action)

    switch (data.action) {
        case "switch view": 
            // hide map view if it's shown
            if (mapContainer.classList.contains("d-block")) {
                hideMap();
            }

            // show view if it's hidden
            if (viewContainer.classList.contains("d-none")) {
                showView();
            }
            
            // re-populate with results from WS Server 
            document.querySelector(`[id="${data.selector}"]`).innerHTML = data.html;

            // re initialize eventlisteners
            removeListeners();
            initializeEventListenerToButtons();
            break;
        case "added repair form": 
            // get out original empty div that ws response will override
            var originalDiv = document.querySelector(`[id="${data.selector}"]`);

            // re-populate with results from WS Server 

            // create a new to house new repair form
            var newDiv = document.createElement("div");
            originalDiv.parentNode.appendChild(newDiv);
            // put new html in new div
            newDiv.innerHTML = data.html;

            create_id++;
            // re initialize eventlisteners
            removeListeners();
            initializeEventListenerToButtons();

            break;
        case "send model options":
            
            
            // This deos not replace second option form when changing brand, it adds it; not correct behavior
            // var newDiv = document.createElement("div");
            // document.querySelector(`[id="${data.selector}"]`).parentElement.appendChild(newDiv).innerHTML = data.html;   
            
            // Want to replace element with new one from received string: html
            document.querySelector(`[id=${data.selector}]`).outerHTML = data.html;
            


            // re initialize eventlisteners
            removeListeners();
            initializeEventListenerToButtons();
            break;
    }
    
});