
let placementButtons = [];

document.addEventListener("DOMContentLoaded", function (){

    var placeWallButton = document.getElementById('addWallButton');
    var placeLightSourceButton = document.getElementById('addLightSourceButton');
    var placeHeatSourceButton = document.getElementById('addHeatSourceButton');

    placeWallButton.addEventListener("click", function(){placeButtonClicked(placeWallButton.id)});
    placeLightSourceButton.addEventListener("click", function(){placeButtonClicked(placeLightSourceButton.id)});
    placeHeatSourceButton.addEventListener("click", function(){placeButtonClicked(placeHeatSourceButton.id)});

    placementButtons.push(placeWallButton);
    placementButtons.push(placeLightSourceButton);
    placementButtons.push(placeHeatSourceButton);

    console.log(placementButtons);
    
    function placeButtonClicked(buttonID) {
        for(var pButton of placementButtons){
            pButton.disabled = pButton.id == buttonID;
        }
    }
});