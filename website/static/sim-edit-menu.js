
let placementButtons = [];

document.addEventListener("DOMContentLoaded", function (){

    var selectButton = document.getElementById('selectButton');
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
    
    function placeButtonClicked(buttonID) {
        for(var pButton of placementButtons){
            pButton.disabled = pButton.id == buttonID;
        }
    }
});