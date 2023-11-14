/**
 * @class
 * @classdesc A square grid that displays a simulated environment
 */
class SimulationGrid{
    /**
     * Create an NxN simulation grid object
     * @param {Int} width The width to set for the grid
     * @param {Int} SimulationGrid.width The width of the grid
     * @property {Cell[]} SimulationGrid.cells array containing Cell objects (refer to cell.js for more info)
     * @property {Element} simContainerElement SimulationGrid container
     */
    constructor(width){
        //Set SimulationGrid Width
        this.width = width;
        //Create NxN Array to store Cell objects
        this.cells = new Array(this.width * this.width);
        //Visually create a NxN container
        const simContainerElement = document.querySelector('.sim-container');
        simContainerElement.style.gridTemplateColumns = `repeat(${this.width}, 18px)`;
        //Create NxN square grid containing Cell objects
        for(let i = 0; i < this.width * this.width; i++){
            //Add create and add Cell to container
            let position = [Math.floor(i/this.width), i % this.width];
            let curCell = new Cell(position);
            simContainerElement.append(curCell.element);
            this.cells[i] = curCell;
        }
        //Make SimulationGrid on backend
        this.setupGrid();
    }
    
    /**
     * Retreive Simulation data from backend
     * @var {Array[((X,Y), RGB)]} creatures array containing position (X,Y) and color RGB of all creatures
     * @var {Array[(X,Y)]} walls Array containing positions of all Walls
     *  @var {Array[(X,Y), Array[Layers]]} layers Array containing Layer information at all positions (X,Y)
     */
    setupGrid(){
        console.log("SETTING GRIED");
        fetch('/new_setup_grid')
        .then((response) => response.json())
        .then((packet) => {
            //"position, numConsumer, numProduc, isWall, temperature)"
            for(let data of packet){
                var position = data[0];
                var numConsumer = data[1];
                var numProducer = data[2];
                var isWall = data[3];
                var temp = data[4];
                var cell = this.cells[this.width * position[0] + position[1]];
                cell.updateProperties(numConsumer, numProducer, isWall, temp);
            }
           
            
        })
        .catch((error) =>{
            console.error('Error:', error);
        });
    }

    //Request state of simulation grid from server, then apply these changes on the frontend
    getGridData(){
        //Request simulation grid data
        fetch('/get_grid_data')
        .then((response) => response.json())
        .then((packet) => {
            for(let data of packet){
                //Per creature(oldPos, newPos) call this CreatureInfo (should supplant position)
                var position = data[0];
                var numConsumer = data[1];
                var numProducer = data[2];
                var isWall = data[3];
                var temp = data[4];
                var cell = this.cells[this.width * position[0] + position[1]];
                cell.updateProperties(numConsumer, numProducer, isWall, temp);
            }   
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
        .then((packet) => {
            for(let data of packet){
                var position = data[0];
                var numConsumer = data[1];
                var numProducer = data[2];
                var isWall = data[3];
                var temp = data[4];
                var cell = this.cells[this.width * position[0] + position[1]];
                cell.updateProperties(numConsumer, numProducer, isWall, temp);
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

    //Display cellOverlay for all Cells
    displayHeatmap(){
        for(let cell of this.cells){
            cell.displayCellOverlay();
        }
    }

     //Hide cellOverlay for all Cells
    stopHeatmapDisplay(){
        for(let cell of this.cells){
            cell.hideCellOverlay();
        }
        console.log("stopping heatmap..");
    }
    

    //USED FOR DEBUGGING
    print(){
        for(let cell of this.cells){
            cell.print();
        }
    }
}