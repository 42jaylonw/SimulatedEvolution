class SimulationGrid
{
    constructor(size)
    {
        this.cells = new Array(size * size);
        const output = document.querySelector('.sim-container');
        //Create NxN square grid containing Cell objects
        for(let i = 0; i < this.cells.length; i++)
        {
            //Add cell to container
            let id = 'cell-' + Math.floor(i/size) + '-' + i % size;
            let curCell = new Cell(id);
            output.append(curCell.element);
            //Add cell to internal array
            this.cells[i] = curCell;
        }
    }
    
    //Edit a specified cell
    editCell(cellId, color)
    {
        const cell = document.getElementById(cellId);
        cell.style.backgroundColor = color;
    }
    
    populateGrid()
    {
        //Create simulation grid and request its information
        fetch('/setup_grid')
        .then((response) => response.json())
        .then((data) => {
            //Apply received data to grid
            for(let organism of data)
            {
                const position = organism[0]
                const color = organism[1]
                //console.log('cell-' + position[0] + '-' + position[1], `rgb(${(color[0] *255)}, ${(color[1] * 255)}, ${(color[2] * 255)})`);
                this.editCell('cell-' + position[0] + '-' + position[1], `rgb(${(color[0] *255)}, ${(color[1] * 255)}, ${(color[2] * 255)})`);
            }
            console.log("done setting up grid!");
            
        })
        .catch((error) =>{
            console.error('Error:', error);
        });
    }

    //Request state of simulation grid from server, then apply these changes on the frontend
    getGridData()
    {
        //Request simulation grid data
        fetch('/get_grid_data')
        .then((response) => response.json())
        .then((data) => {
            //update frontend grid 
            for(let organism of data)
            {
                oldPosition = organism[0]
                newPosition = organism[1]
                color = organism[2]
                //Change grid data
                this.editCell('cell-' + oldPosition[0] + '-' + oldPosition[1], 'white');
                this.editCell('cell-' + newPosition[0] + '-' + newPosition[1], `rgb(${(color[0] *255)}, ${(color[1] * 255)}, ${(color[2] * 255)})`);
            }
            
        })
        .catch((error) =>{
            console.error('Error:', error);
        });
    }
    //Request simulation grid data from server every 0.45 seconds
    runSimulation()
    {
        this.simulationID = setInterval(this.getGridData, 1000);
    }

    //Stop sending simulation grid data requests
    pauseSimulation()
    {
        clearInterval(this.simulationID);
    }
}