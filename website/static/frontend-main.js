
//Create a 50x50 Simulation Grid
simSpace = new SimulationGrid(50);
simSpace.populateGrid();
console.log("done setting up grid!");

//Assign functions for each button
simButton = document.getElementById('simulateButton');
newSimButton = document.getElementById('newSimulationButton');

let heatMapdisplayed = false;
let isSimRunning = false;
toggleClimateButton = document.getElementById('toggleClimateButton');

toggleClimateButton.addEventListener('click', function(){
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
});

//Start/Pause Simulation
simButton.addEventListener('click', function(){
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
});

//Create a new Simulation
newSimButton.addEventListener('click', function()
{
    simSpace.newSimulation();
});