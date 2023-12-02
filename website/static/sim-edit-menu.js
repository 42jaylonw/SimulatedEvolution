
let placementButtons = [];

document.addEventListener("DOMContentLoaded", function (){
    var analysisContainer = document.querySelector('.analysis-container');
    var selectButton = document.getElementById('selectButton');
    selectButton.disabled = true;
    var placeWallButton = document.getElementById('addWallButton');
    var placeLightSourceButton = document.getElementById('addLightSourceButton');
    var placeHeatSourceButton = document.getElementById('addHeatSourceButton');
    var placeConsumerButton = document.getElementById('addConsumerButton');
    var placeProducerButton = document.getElementById('addProducerButton');
    var eraserButton = document.getElementById('eraserButton');

    selectButton.addEventListener("click", function(){placeButtonClicked(selectButton.id)});
    placeWallButton.addEventListener("click", function(){placeButtonClicked(placeWallButton.id)});
    placeLightSourceButton.addEventListener("click", function(){placeButtonClicked(placeLightSourceButton.id)});
    placeHeatSourceButton.addEventListener("click", function(){placeButtonClicked(placeHeatSourceButton.id)});
    placeConsumerButton.addEventListener("click", function(){placeButtonClicked(placeConsumerButton.id)});
    placeProducerButton.addEventListener("click", function(){placeButtonClicked(placeProducerButton.id)});
    eraserButton.addEventListener("click", function(){placeButtonClicked(eraserButton.id)});


    placementButtons.push(selectButton);
    placementButtons.push(placeWallButton);
    placementButtons.push(placeLightSourceButton);
    placementButtons.push(placeHeatSourceButton);
    placementButtons.push(placeConsumerButton);
    placementButtons.push(placeProducerButton);
    placementButtons.push(eraserButton);

    console.log(placementButtons);
    let mode = selectButton.id;
    let curMenu;

    // Disable a selected button using it's ID
    function placeButtonClicked(buttonID) {
        for(var pButton of placementButtons){
            
            pButton.disabled = pButton.id == buttonID;
        }
        // Change the default function to be called when pressing left click
        mode = buttonID;
        refreshParameterMenu(mode);
                
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


    //Cell-row-col
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
        performGridSpaceOperation(element, '/add_creature_consumer');
    }

    function placeProducer(element){
        console.log("adding producer");
        performGridSpaceOperation(element, '/add_creature_producer');
    }

    function placeLightSource(element){
        console.log("adding light source");
        performGridSpaceOperation(element, '/add_lightsource');
    }

    function placeHeatSource(element){
        console.log("adding heat source");
        
        performGridSpaceOperation(element, '/add_heatsource');
        simSpace.toggleOverlayDisplay(true, "heatmap");
    }

    function performGridSpaceOperation(element, route){
        cellInformation = element.split("-") 
        console.log(cellInformation[1] + "," + cellInformation[2]);
        const dataToSend = {position: [parseInt(cellInformation[1]), parseInt(cellInformation[2])]};
        fetch(route, {method: "POST", headers:{"Content-Type": "application/json"}, body: JSON.stringify(dataToSend)})
        .then((response) => response.json())
        .then((data) => {
            if(route == '/get_creatures_at_grid_space'){
                var producers = data["producers"];
                var consumers = data["consumers"];
                var emitters = data["emitters"];
                // var analysisContainer = document.querySelector('.analysis-container');
                analysisContainer.innerHTML += `<br>` + generateEmitterText("EMITTERS", emitters);
                analysisContainer.innerHTML =   `<h2 class="text-center" class="details-text">Information at ${cellInformation[1]}, ${cellInformation[2]}</h2> ` + 
                generateCreatureText("CONSUMERS", consumers) + "<br>" + generateCreatureText("PRODUCERS", producers) + "<br>" + generateEmitterText("EMITTERS", emitters);
                return;
            }
            if(route == '/add_heatsource' || route == '/add_lightsource')
            {
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
         * 
         * @param {string} creatureClass name of type of creature 
         * @param {Element[]} creatures Creature along with its properties
         * @returns {string} formatted string that contains a creature's properties
         */
    function generateCreatureText(creatureClass, creatures){
        var creatureText = creatureClass;
        for(let creature of creatures){
            creatureText += `<p>Genome: ${creature["genome"]} <br>Size: ${creature["size"]} <br>Energy ${creature["energy"]} </p>`;
        }
        return creatureText;
    }

    function generateEmitterText(emitterClass, emitters){
        var emitterText = emitterClass
        for(let emitter of emitters){
            emitterText += `<p>Emit Range: ${emitter["range"]} <br>Emit Strength: ${emitter["strength"]}`;
        }
        return emitterText
    }

    function refreshParameterMenu(buttonID){
        var menuToAdd;
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
            default:
                menuToAdd = null;
        }

        if(curMenu != null){
            analysisContainer.removeChild(curMenu);
        }
        
        if (menuToAdd != null){
            
            analysisContainer.append(menuToAdd);
        }
        
        curMenu = menuToAdd;
    }


    function createEmitterMenu(){
        var emitterMenu = document.createElement("div");
        emitterMenu.classList.add("emitter-menu");
        emitterMenu.innerHTML = `Emitter Menu`;
        return emitterMenu;
    }

    function createCreatureMenu(){
        var creatureMenu = document.createElement("div");
        creatureMenu.classList.add("creature-menu");
        creatureMenu.innerHTML = `Consumer Menu`;
        return creatureMenu;
    }
});