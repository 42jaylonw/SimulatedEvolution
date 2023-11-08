
//Create a 50x50 Simulation Grid
simSpace = new SimulationGrid(50);
simSpace.populateGrid();


//Assign functions for each button
startSimButton = document.getElementById('simulateButton');
pauseSimButton = document.getElementById('pauseSimulationButton');
newSimButton = document.getElementById('newSimulationButton');
//Start Simulation
startSimButton.addEventListener('click', function(){
    simSpace.runSimulation();
    startSimButton.disabled = true;
});

//Pause Simulation
pauseSimButton.addEventListener('click', function(){
    simSpace.pauseSimulation();
    startSimButton.disabled = false;
});

//Create a new Simulation
newSimButton.addEventListener('click', function()
{
    simSpace.newSimulation();
});