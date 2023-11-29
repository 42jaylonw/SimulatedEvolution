
let placementButtons = [];

document.addEventListener("DOMContentLoaded", function (){
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
    // Disable a selected button using it's ID
    function placeButtonClicked(buttonID) {
        for(var pButton of placementButtons){
            
            pButton.disabled = pButton.id == buttonID;
        }
        // Change the default function to be called when pressing left click
        mode = buttonID;

    }

    // Call menu method based on selected mode
    function handleUserClick(ev){
        if(ev == null || ev.target.id == '' || !ev.target.id.includes("cell")){
            return;
        }
        switch(mode){
            case placeWallButton.id:
                AddWall(ev.target.id);
                break;
            case selectButton.id:
                break;

        }
        
    }
    document.addEventListener('click', handleUserClick);

});
//Cell-row-col
function AddWall(element){
    cellInformation = element.split("-")
    console.log(cellInformation[1] + cellInformation[2]);
    const data = {position: [parseInt(cellInformation[1]), parseInt(cellInformation[2])]};
    fetch('/add_wall', {method: "POST", headers:{"Content-Type": "application/json"}, body: JSON.stringify(data)})
    .then((response) => response.json())
    .then((data) => {
        simSpace.visualUpdate(data);
    })
    .catch((error) =>{
        console.error('Error:', error);
    });
    // simSpace.visualUpdate();
}


