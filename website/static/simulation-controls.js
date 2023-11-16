
let heatMapdisplayed = false;
let isSimRunning = false;

//Event listener for entire window
document.addEventListener('keydown', function (e) {
    //Press space to start or pause simulation
    if (e.code === 'Space') {
        // Prevent scrolling on spacebar press
        e.preventDefault(); 
        changeSimulationMode();
    }
    //Press shift + 'N' to create a new simulation
    if(e.shiftKey && e.code === 'KeyN'){
        simSpace.newSimulation();
    }
    //Press Tab to toggle heatmap
    if(e.code === 'Tab'){
        e.preventDefault();
        toggleHeatmap("heatmap");
    }
    if(e.shiftKey && e.code ==='KeyM'){
        toggleHeatmap("lightmap")
    }
});

//Assign functions for each button
simButton = document.getElementById('simulateButton');
newSimButton = document.getElementById('newSimulationButton');
toggleClimateButton = document.getElementById('toggleClimateButton');

//Change simulation view to heatmap view
toggleClimateButton.addEventListener('click', function(){
   toggleHeatmap();
});

//Start/Pause Simulation button
simButton.addEventListener('click', function(){
    changeSimulationMode();
});

//Create a new Simulation
newSimButton.addEventListener('click', function()
{
    simSpace.newSimulation();
});

//Start or Pause the simulation
function changeSimulationMode()
{
    if(!isSimRunning)
    {
        simSpace.runSimulation();
        simButton.textContent = "Pause Simulation"
    }
    else
    {
        simSpace.pauseSimulation();
        simButton.textContent = "Play Simulation"
    }
    isSimRunning = !isSimRunning;
}

//Display/hide heatmap based on last state of heatmap
function toggleHeatmap(mode)
{
    //Change state
    heatMapdisplayed = !heatMapdisplayed;
    //Change text on toggle button
    if(heatMapdisplayed){
        toggleClimateButton.textContent = "Hide Heatmap"
    }
    else{
      toggleClimateButton.textContent = "Show Heatmap"
    }
    //toggle heatmap
    simSpace.toggleHeatmapDisplay(heatMapdisplayed, mode);
    
}