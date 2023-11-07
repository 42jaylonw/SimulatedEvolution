
simSpace = new SimulationGrid(50);
simSpace.populateGrid();

document.getElementById('simulateButton').addEventListener('click', function(){
    simSpace.runSimulation();
});