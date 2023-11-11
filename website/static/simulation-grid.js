/**
 * @class
 * @classdesc A square grid that displays a simulated environment
 */
class SimulationGrid{
    /**
     * Create an NxN simulation grid object
     * @param {Int} width The width of the grid
     * @property {Array[cell]} SimulationGrid.cells array containing Cell objects
     * @property {Element} simContainerElement SimulationGrid container
     */
    constructor(width){
        this.width = width;
        this.cells = new Array(this.width * this.width);
        const simContainerElement = document.querySelector('.sim-container');
        //Create NxN square grid containing Cell objects
        for(let i = 0; i < this.width * this.width; i++){
            //Add create and add Cell to container
            let position = [Math.floor(i/this.width), i % this.width];
            let curCell = new Cell(position);
            simContainerElement.append(curCell.element);
            this.cells[i] = curCell;
        }
        this.setupGrid();
    }
    
    /**
     * Retreive Simulation data from backend
     * @var {Array[((X,Y), RGB)]} creatures array containing position (X,Y) and color RGB of all creatures
     * @var {Array[(X,Y)]} walls Array containing positions of all Walls
     *  @var {Array[(X,Y), Array[Layers]]} layers Array containing Layer information at all positions (X,Y)
     */
    setupGrid(){
        //Create simulation grid and request its information
        fetch('/setup_grid')
        .then((response) => response.json())
        .then((data) => {
            //Apply received data to grid
            let creatures = data[0];
            let walls = data[1];
            let layers = data[2];       
            this.handleGridData(creatures, layers, walls);
            
        })
        .catch((error) =>{
            console.error('Error:', error);
        });
    }

    //FIXME: adjust Walls should be static so, Walls should only be iterated over during setupGrid()
    /**
     * Update Simulation Grid object with data received from the backend
     * @param {Array[((X,Y), RGB)]} creatureInfo Array containing position (X,Y) and color RGB of all creatures
     * @param {Array[(X,Y), Array[Layers]]} layers Array containing Layer information at all positions (X,Y)
     * @param {Array[(X,Y)]} walls Array containing positions of all Walls
     * @param {bool} setCreatures Mode in which to update the Simulation Grid
     */
    handleGridData(creatureInfo=[], layers=[], walls=[], setCreatures=false){
        //Check if data received specifies creature movement
        if(setCreatures){
            //Update simulation grid according to creature movement
             for(let organism of creatureInfo){
                //Clear old Cell that Creature occupied then update the newly occupied Cell
                let oldPosition = organism[0];
                let newPosition = organism[1];
                let color = organism[2];
                var oldCell = this.cells[this.width * oldPosition[0] + oldPosition[1]];
                var newCell = this.cells[this.width * newPosition[0] + newPosition[1]];
                oldCell.setCellColor("white");
                newCell.setCellColor(`rgb(${(color[0] *255)}, ${(color[1] * 255)}, ${(color[2] * 255)})`);
            }
        }
        //Set up initial Creature positions
        else{
            //Update simulation grid according to initial positions
            for(let organism of creatureInfo){
                var position = organism[0];
                let color = organism[1];
                //Access cell object instead of the element directly
                var cell = this.cells[this.width * position[0] + position[1]];
                cell.setCellColor(`rgb(${(color[0] *255)}, ${(color[1] * 255)}, ${(color[2] * 255)})`);
            }
        }
        //Set up walls
        for(let wall of walls)
        {
            var position = wall;
            var cell = this.cells[this.width * position[0] + position[1]];
            cell.setCellColor("black");
        }
        //Update layer information
        for(let layer of layers){
            let layerPosition = layer[0];
            let layerInformation = layer[1];
            var cell = this.cells[this.width * layerPosition[0] + layerPosition[1]];
            cell.updateProperties(layerInformation);
        }
    }

    //Request state of simulation grid from server, then apply these changes on the frontend
    getGridData(){
        //Request simulation grid data
        fetch('/get_grid_data')
        .then((response) => response.json())
        .then((data) => {
            let creatureInfo = data[0];
            let layers = data[1];
            this.handleGridData(creatureInfo, layers, [], true);       
        })
        .catch((error) =>{
            console.error('Error:', error);
        });
    }

    //Visually clear the simulation grid
    clearSimulation(){   
        for(let i = 0; i < this.width * this.width; i++)
        {
            let curCell = this.cells[i];
            curCell.setCellColor("white");
        }
    }

    //Create a new simulation
    newSimulation(){
        //Clear any information of an old simulation
        this.clearSimulation();
        //Create GET request for new simluation information
        fetch('/new_grid')
        .then((response) => response.json())
        //Request SUCCESS
        .then((data) => {
            //Apply received data to grid
            let creatures = data[0]
            for(let organism of creatures)
            {
                var position = organism[0];
                let color = organism[1];
                //Access cell object instead of the element directly
                var cell = this.cells[this.width * position[0] + position[1]];
                cell.setCellColor(`rgb(${(color[0] *255)}, ${(color[1] * 255)}, ${(color[2] * 255)})`);
            }
            let walls = data[1]
            for(let wall of walls)
            {
                var position = wall
                var cell = this.cells[this.width * position[0] + position[1]];
                cell.setCellColor("black");
            }
            console.log("Created new Grid!");
            
        })
        //Request FAILURE
        .catch((error) =>{
            console.error('Error:', error);
        });
    }
    
    //Request simulation grid data from server every 0.500 seconds
    runSimulation(){
        this.simulationID = setInterval(() => {this.getGridData()}, 500);
    }

    //Stop sending simulation grid data requests
    pauseSimulation(){
        console.log("stopping calls..");
        clearInterval(this.simulationID);
    }

    displayHeatmap(){
        for(let cell of this.cells){
            cell.displayCellOverlay();
        }
    }

    stopHeatmapDisplay(){
        for(let cell of this.cells){
            cell.hideCellOverlay();
        }
        console.log("stopping heatmap..");
    }
}