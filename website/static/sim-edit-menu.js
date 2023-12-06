
let placementButtons = [];

document.addEventListener("DOMContentLoaded", function (){
    let heatMapdisplayed = false;
    document.addEventListener('keydown', function (e) {
        //Press Tab to toggle heatmap
        if(e.code === 'Tab'){
            e.preventDefault();
            toggleOverlay("heatmap");
        }
        //Press SHIFT + M to toggle lightmap
        if(e.shiftKey && e.code ==='KeyM'){
            toggleOverlay("lightmap");
        }
    });
    // Toggle the overlay of the simulation
    function toggleOverlay(mode){
        //Change state
        heatMapdisplayed = !heatMapdisplayed;
        simSpace.toggleOverlayDisplay(heatMapdisplayed, mode);
    }
    
    //HTML elements for pre-simulation
    var analysisContainer = document.querySelector('.analysis-container');
    var selectButton = document.getElementById('selectButton');
    selectButton.disabled = true;
    var placeWallButton = document.getElementById('addWallButton');
    var placeLightSourceButton = document.getElementById('addLightSourceButton');
    var placeHeatSourceButton = document.getElementById('addHeatSourceButton');
    var placeConsumerButton = document.getElementById('addConsumerButton');
    var placeProducerButton = document.getElementById('addProducerButton');
    var eraserButton = document.getElementById('eraserButton');

    //Listeners for pre-simulation HTML elements
    selectButton.addEventListener("click", function(){placeButtonClicked(selectButton.id)});
    placeWallButton.addEventListener("click", function(){placeButtonClicked(placeWallButton.id)});
    placeLightSourceButton.addEventListener("click", function(){placeButtonClicked(placeLightSourceButton.id)});
    placeHeatSourceButton.addEventListener("click", function(){placeButtonClicked(placeHeatSourceButton.id)});
    placeConsumerButton.addEventListener("click", function(){placeButtonClicked(placeConsumerButton.id)});
    placeProducerButton.addEventListener("click", function(){placeButtonClicked(placeProducerButton.id)});
    eraserButton.addEventListener("click", function(){placeButtonClicked(eraserButton.id)});

    //Store all HTML buttons in an array
    placementButtons.push(selectButton);
    placementButtons.push(placeWallButton);
    placementButtons.push(placeLightSourceButton);
    placementButtons.push(placeHeatSourceButton);
    placementButtons.push(placeConsumerButton);
    placementButtons.push(placeProducerButton);
    placementButtons.push(eraserButton);

    //Store mode based on selected user button
    //Store menu that is associated with the selected button
    let mode = selectButton.id;
    let curMenu;

    // Disable a selected button using it's ID
    function placeButtonClicked(buttonID) {
        for(var pButton of placementButtons){
            
            pButton.disabled = pButton.id == buttonID;
        }
        // Change the default function to be called when pressing left click
        mode = buttonID;
        //Display menu associated with selected button
        refreshParameterMenu(mode);
        //Reset simspace overlay
        simSpace.toggleOverlayDisplay(false, "none");    
    }

    // Call menu method based on selected mode
    function handleUserClick(ev){
        if(ev == null || ev.target.id == '' || !ev.target.id.includes("cell")){
            return;
        }
        switch(mode){
            case placeWallButton.id:
                addWall(ev.target.id);
                break;
            case selectButton.id:
                selectSpace(ev.target.id);
                break;
            case eraserButton.id:
                eraseSpace(ev.target.id);
                break;
            case placeConsumerButton.id:
                placeConsumer(ev.target.id);
                break;
            case placeProducerButton.id:
                placeProducer(ev.target.id);
                break;
            case placeLightSourceButton.id:
                placeLightSource(ev.target.id);
                break;
            case placeHeatSourceButton.id:
                placeHeatSource(ev.target.id);
                break;
            
        }
        
    }
    document.addEventListener('click', handleUserClick);


    function addWall(element){
        performGridSpaceOperation(element, '/add_wall');
    }

    function eraseSpace(element){
        performGridSpaceOperation(element, '/erase_space');
    }

    function selectSpace(element){
        performGridSpaceOperation(element, '/get_creatures_at_grid_space');
    }

    function placeConsumer(element){
        console.log("adding consumer");
        performGridSpaceOperation(element, '/add_creature_consumer', payload={headers: ["preset-id"], values: [document.getElementById("preset-input").value]});
    }

    function placeProducer(element){
        console.log("adding producer");
        performGridSpaceOperation(element, '/add_creature_producer',  payload={headers: ["preset-id"], values: [document.getElementById("preset-input").value]});
    }

    function placeLightSource(element){
        console.log("adding light source");
        performGridSpaceOperation(element, '/add_lightsource', payload={headers: ["emit_range", "emit_strength"], values: [parseInt(document.getElementById("emit_range").value), parseInt(document.getElementById("emit_strength").value)]});
    }

    function placeHeatSource(element){
        console.log("adding heat source");
        performGridSpaceOperation(element, '/add_heatsource', payload={headers: ["emit_range", "emit_strength"], values: [parseInt(document.getElementById("emit_range").value), parseInt(document.getElementById("emit_strength").value)]});
        simSpace.toggleOverlayDisplay(true, "heatmap");
    }

    /**
     * Perform an operation on the back-end simulation and update the front-end repreentation
     * of it.
     * @param {Element} element selected HTML element
     * @param {string} route route to call in the Python back-end
     * @param {object{}} payload additional information to send to Python back-end
     */
    function performGridSpaceOperation(element, route, payload=null){
        //Element should follow format "cell-<row>-<col>"
        cellInformation = element.split("-") 
        
        //Add any additional data to send to the back-end
        const dataToSend = constructDataToSend(payload);
        
        //Make POST request
        fetch(route, {method: "POST", headers:{"Content-Type": "application/json"}, body: JSON.stringify(dataToSend)})
        .then((response) => response.json())
        .then((data) => {
            //Response from back-end
            //Update menu on the right side of the menu when using select button
            if(route == '/get_creatures_at_grid_space'){
                var producers = data["producers"];
                var consumers = data["consumers"];
                var emitters = data["emitters"];
                analysisContainer.innerHTML += `<br>` + generateEmitterText("EMITTERS", emitters);
                analysisContainer.innerHTML =   `<h2 class="text-center" class="details-text">Information at ${cellInformation[1]}, ${cellInformation[2]}</h2> ` + 
                generateCreatureText("CONSUMERS", consumers) + "<br>" + generateCreatureText("PRODUCERS", producers) + "<br>" + generateEmitterText("EMITTERS", emitters);
                return;
            }
            //Update simulation overlay when placing emitters
            if(route == '/add_heatsource' || route == '/add_lightsource')
            {
                simSpace.visualUpdate(data, isBatch=true);
                simSpace.toggleOverlayDisplay(true, route);
                return;
            }
            //Update simulation after erasing objects
            if(route == '/erase_space'){ 
                if(data != undefined && data.length == undefined){
                    simSpace.visualUpdate(data);
                }
                else if(data.length > 1)
                    simSpace.visualUpdate(data, isBatch=true);
                return;
            }
            // update the visual grid based on function associated with route
            simSpace.visualUpdate(data);
        })
        .catch((error) =>{
            console.error('Error:', error);
        });
    }

    /**
     * Create a data packet to send to the python back-end based on specified headers and values
     * @param {object{}} additionalInfo data that should be send to Python back-end 
     * @returns a list of headers and values associated with the specified additionalInfo 
     */
    function constructDataToSend(additionalInfo=null){
        var dataToSend = {position: [parseInt(cellInformation[1]), parseInt(cellInformation[2])]};

        if (additionalInfo != null){
            var headers = additionalInfo.headers;
            var values = additionalInfo.values;

            for(var i = 0; i < headers.length; i++){
                dataToSend[headers[i]] = values[i];
            }
        }
        
        return dataToSend;
    }

    /**
     * Generates text given a list of creatures and specified class
     * @param {string} creatureClass name of type of creature 
     * @param {Element[]} creatures Creature along with its properties
     * @returns {string} formatted string that contains a creature's properties
     */
    function generateCreatureText(creatureClass, creatures){
        var creatureText = creatureClass;
        for(let creature of creatures){
            creatureText += `<p>SpeciesID: ${creature["species"]} <br>Genome: ${creature["genome"]} <br>Size: ${creature["size"]} <br>Energy ${creature["energy"]} </p>`;
        }
        return creatureText;
    }
    /**
     * Generates text given a list of emitters and specified class
     * @param {string} emitterClass name of type of emitter 
     * @param {Element[]} emitters Emitter along with its properties
     * @returns formatted string that contains emitter's properties
     */
    function generateEmitterText(emitterClass, emitters){
        var emitterText = emitterClass
        for(let emitter of emitters){
            emitterText += `<p>Emit Range: ${emitter["range"]} <br>Emit Strength: ${emitter["strength"]}`;
        }
        return emitterText
    }

    /**
     * Change the menu to display based on the button pressed
     * @param {string} buttonID ID button that was selected 
     */
    function refreshParameterMenu(buttonID){
        var menuToAdd;
        //Remove old menu that is currently displayed
        analysisContainer.innerHTML = '';
        //Display new menu according to pressed button
        switch(buttonID){
            case placeHeatSourceButton.id:
                menuToAdd = createEmitterMenu();
                break;
            case placeLightSourceButton.id:
                menuToAdd = createEmitterMenu();
                break;
            case placeConsumerButton.id:
                menuToAdd = createCreatureMenu();
                break;
            case placeProducerButton.id:
                menuToAdd = createCreatureMenu();
                break;
            default:
                menuToAdd = null;
        }
        
        if (menuToAdd != null){
            analysisContainer.append(menuToAdd);
        }
        //Mark the newly assigne menu as the current menu displayed    
        curMenu = menuToAdd;
    }

    /**
     * Create a HTML element that allows users to specify the range 
     * and strength of placed emitters
     * @returns HTML element to display
     */
    function createEmitterMenu(){
        var emitterMenu = document.createElement("div");

        emitterMenu.classList.add("emitter-menu");
        emitterMenu.innerHTML = `<h1>Emitter Menu</h1><br>Range<br>` + generatePlaceValueSlider("emit_range", 1, 25);
        emitterMenu.innerHTML += `<br>Strength<br>` + generatePlaceValueSlider("emit_strength", 1, 100);

        return emitterMenu;
    }

    /**
     * Create HTML slider with specified id and min/max values
     * @param {string} id id assigned to created slider
     * @param {int} min minimum value for created slider
     * @param {int} max maximum value for created slider
     * @returns HTML slider with specified parameters
     */
    function generatePlaceValueSlider(id, min, max){
        returnValueHTML = `<div class="slidecontainer"><input type="range" min="${min}" max="${max}" value="${max}" class="slider" id=${id}> </div>`;
        return returnValueHTML;
    }

    /**
     * Create a HTML element that allows users to load in Creatures
     * with a preset genome
     * @returns HTML element to display
     */
    function createCreatureMenu(){
        var creatureMenu = document.createElement("div");
        creatureMenu.classList.add("creature-menu");
        creatureMenu.innerHTML = `<h1>Creature Menu</h1> <br> Enter a Genome Preset: <br>`;

        //Add inputFields
        var presetInput = createInputField("presetID", "Enter Preset ID");
        presetInput.id = "preset-input";
        //Return menu 
        creatureMenu.appendChild(presetInput);
        return creatureMenu;
    }

    /**
     * Create an HTML input field with specified name and placeholder
     * @param {string} name name for created HTML input field 
     * @param {string} placeholder placeholder for created HTML input field
     * @returns HTML input field
     */
    function createInputField(name, placeholder="placeholder"){
        var newInputField = document.createElement("input");
        newInputField.setAttribute("type", "text");
        newInputField.setAttribute("name", name);
        newInputField.setAttribute("placeholder", placeholder);
        return newInputField
    }
});