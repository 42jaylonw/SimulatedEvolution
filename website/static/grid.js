//TODO: handle user submitting quantity of producers and consumers 
const output = document.querySelector('.sim-container');

const grid={rows:50, cols:50};

createGrid(grid.rows * grid.cols);
populateGrid();

// Create grid
function createGrid(total)
{
    for(i = 0; i < total; i++)
    {
        const cell = document.createElement('div');
        // Cell id is 'cell-<row>-<col>'
        cell.id = 'cell-' + Math.floor(i/grid.rows) + '-' + i % grid.cols;
        //Add cell to container
        output.append(cell);
        //Add style classification for cell
        cell.classList.add('grid-item');
        cell.style.backgroundColor = "white";
        //Add event listeners to each cell
        cell.onmouseenter = function() {showCellBorder(this)};
        cell.onmouseleave = function() {hideCellBorder(this)};
    }
}

//Create an outline for each cell that the mouse hovers over
function showCellBorder(cell)
{
    cell.style.border = "1px solid black";
    console.log("Entering " + cell.id);
}

//Remove outline when mouse leaves cell
function hideCellBorder(cell)
{
    cell.style.border = "none";
    console.log("Leaving " + cell.id);
}
//Edit a specified cell
function editCell(cellId, color)
{
    const cell = document.getElementById(cellId);
    cell.style.backgroundColor = color;
}

//Create a new simulation grid on the server, then request the simulation grid information, then apply this data to frontend 
let simulationID;
function populateGrid()
{
    //Create simulation grid and request its information
    fetch('/setup_grid')
    .then((response) => response.json())
    .then((data) => {
        //Apply received data to grid
        for(let organism of data)
        {
            position = organism[0]
            color = organism[1]
            editCell('cell-' + position[0] + '-' + position[1], `rgb(${(color[0] *255)}, ${(color[1] * 255)}, ${(color[2] * 255)})`);
        }
        
    })
    .catch((error) =>{
        console.error('Error:', error);
    });
}

//Request state of simulation grid from server, then apply these changes on the frontend
function getGridData()
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
            editCell('cell-' + oldPosition[0] + '-' + oldPosition[1], 'white');
            editCell('cell-' + newPosition[0] + '-' + newPosition[1], `rgb(${(color[0] *255)}, ${(color[1] * 255)}, ${(color[2] * 255)})`);
        }
        
    })
    .catch((error) =>{
        console.error('Error:', error);
    });
}

//Request simulation grid data from server every 0.5 seconds
function runSimulation()
{
    simulationID = setInterval(getGridData, 500);
}

//Stop sending simulation grid data requests
function pauseSimulation()
{
    clearInterval(simulationID);
}
