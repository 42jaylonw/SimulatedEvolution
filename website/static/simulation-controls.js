
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
        toggleHeatmap();
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

function toggleHeatmap()
{
    if(heatMapdisplayed)
    {
        simSpace.stopHeatmapDisplay();
        toggleClimateButton.textContent = "Show Heatmap"
    }
    else
    {
      simSpace.displayHeatmap(); 
      toggleClimateButton.textContent = "Hide Heatmap"
        
    }
    heatMapdisplayed = !heatMapdisplayed;
}