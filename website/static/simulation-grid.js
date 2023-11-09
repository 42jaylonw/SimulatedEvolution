/**
 * @class
 * @classdesc A square grid that displays a simulated environment
 */
class SimulationGrid{
    /**
     * @param {Int} width The width of the the NxN grid
     */
    constructor(width){
        this.width = width;
        this.cells = new Array(this.width * this.width);
        const output = document.querySelector('.sim-container');
        //Create NxN square grid containing Cell objects
        for(let i = 0; i < this.width * this.width; i++){
            //Add create and add Cell to container
            let position = [Math.floor(i/this.width), i % this.width];
            let curCell = new Cell(position);
            output.append(curCell.element);
        }
    }
    
    //Edit a specified cell by it's HTML Id
    changeCellColor(cellId, color){
        const cell = document.getElementById(cellId);
        cell.style.backgroundColor = color;
    }
    
    populateGrid(){
        //Create simulation grid and request its information
        fetch('/setup_grid')
        .then((response) => response.json())
        .then((data) => {
            //Apply received data to grid
            for(let organism of data)
            {
                let position = organism[0]
                let color = organism[1]
                this.changeCellColor('cell-' + position[0] + '-' + position[1], `rgb(${(color[0] *255)}, ${(color[1] * 255)}, ${(color[2] * 255)})`);
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
        .then((data) => {
            //update frontend grid 
            for(let organism of data){
                let oldPosition = organism[0]
                let newPosition = organism[1]
                let color = organism[2]
                //Change grid data
                this.changeCellColor('cell-' + oldPosition[0] + '-' + oldPosition[1], 'white');
                this.changeCellColor('cell-' + newPosition[0] + '-' + newPosition[1], `rgb(${(color[0] *255)}, ${(color[1] * 255)}, ${(color[2] * 255)})`);
            }
            
        })
        .catch((error) =>{
            console.error('Error:', error);
        });
    }

    //Visually clear the simulation grid
    clearSimulation(){   
        for(let i = 0; i < 50 * 50; i++)
        {
            this.changeCellColor('cell-' + Math.floor(i/this.width) + '-' + i % this.width, 'white');
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
            for(let organism of data){
                const position = organism[0]
                const color = organism[1]
                this.changeCellColor('cell-' + position[0] + '-' + position[1], `rgb(${(color[0] *255)}, ${(color[1] * 255)}, ${(color[2] * 255)})`);
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
        fetch('/generate_mock_climate')
        .then((response) => response.json())
        //Request SUCCESS
        .then((climateData) => {
            // let color = "white";
            let color;
            let cellnum = 0;
            for(let temperature of climateData){
                let cell = 'cell-' + Math.floor(cellnum/this.width) + '-' + cellnum % this.width;
                if (temperature < 0.2) 
                {
                    color = `rgb(0,0,255)`;
                } 
                else if (temperature < 0.4) 
                {
                    color = `rgb(0,255,255)`;
                } 
                else if (temperature < 0.6) 
                {
                   color = `rgb(0,255,0)`;
                } 
                else if (temperature < 0.8) 
                {
                    color = `rgb(255,255,0)`;
                } 
                else 
                {
                    color = `rgb(255,0,0)`;
                }
                this.changeCellColor(cell, color)
                cellnum++;

            }
        })
        //Request FAILURE
        .catch((error) =>{
            console.error('Error:', error);
        });
    }

    stopHeatmapDisplay(){
        this.clearSimulation();
        this.populateGrid();
        console.log("stopping heatmap..");
    }
}