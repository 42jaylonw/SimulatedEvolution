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
        this.creatureImages = {};
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
        const data = {size: this.width};
        fetch('/new_setup_grid', {method: "POST", headers:{"Content-Type": "application/json"}, body: JSON.stringify(data)})
        .then((response) => response.json())
        .then((packet) => {
            //"position, numConsumer, numProduc, isWall, temperature)"
            for(let data of packet){

                this.handleInitialData(data);
            } 
        })
        .catch((error) =>{
            console.error('Error:', error);
        });
    }

    makeSimulation(){
        fetch('/setup_data');
    }

    //Request state of simulation grid from server, then apply these changes on the frontend
    getGridData(){
        //Request simulation grid data
        fetch('/get_grid_data')
        .then((response) => response.json())
        .then((packet) => {
            for(let data of packet){
                this.handleData(data);
            }   
        })
        .catch((error) =>{
            console.error('Error:', error);
        });
    }

    visualUpdate(data){
       this.handleData(data);
    }
    //Visually clear the simulation grid
    clearSimulation(){   
        for(let i = 0; i < this.width * this.width; i++)
        {
            let curCell = this.cells[i];
            curCell.setCellColor("white");
            curCell.clearCreatureVisuals();
            
        }
        this.creatureImages = {};
    }

    //Create a new simulation
    newSimulation(){
        //Clear any information of an old simulation
        this.clearSimulation();
        console.log("Creating new Grid");
        //Create GET request for new simluation information
        fetch('/new_grid')
        .then((response) => response.json())
        //Request SUCCESS
        .then((packet) => {
           
            for(let data of packet){
                this.handleInitialData(data);
            }
            console.log("Created new Grid!");
            
        })
        //Request FAILURE
        .catch((error) =>{
            console.error('Error:', error);
        });
    }
    
    /**
     * Update front-end elements based on information received from the back-end
     * @param {JSON} data Information from back-end simulation 
     */
    handleInitialData(data){
        // Extract information
        var position = data["position"];
        var numConsumer = data["consumerCount"];
        var numProducer = data["producerCount"];
        var isWall = data["isWall"];
        var temp = data["temperature"];
        var lightLevel = data["light"];
        var creatureImages = data["creatureImages"];
        var cell = this.cells[this.width * position[0] + position[1]];
        // Create image dictionary and add visual to Cell
        for(var creatureImage of creatureImages){
           var refId = creatureImage[0];
           var imageData = creatureImage[1];
           this.createCreatureImage(refId, imageData);
           cell.addCreatureVisual(this.creatureImages[creatureImage[0]]);
        }
        // Update Cell based on extracted information
        cell.updateProperties(numConsumer, numProducer, isWall, temp, lightLevel);
   }

   /**
    * Create a <canvas> element based on imageData, then add it to the simulation grid's image dictionary
    * using (refId, imageData) format
    * @param {string} refId The key associated with <canvas> element
    * @param {number[][]} imageData RGB data required to create a <canvas> element
    */
   createCreatureImage(refId, imageData){
        // Create <canvas>
        let creatureImage = document.createElement('canvas');
        var context = creatureImage.getContext('2d');
        var scaleFactor = 2;
        // Set var image dimensions based on the image data
        var rows = imageData.length;
        var cols = imageData.length;
        creatureImage.width = cols * scaleFactor;
        creatureImage.height = rows * scaleFactor;
        // Scale the var image context
        context.scale(scaleFactor, scaleFactor);
        // Iterate through the image data and draw pixels on the var image
        for (var i = 0; i < rows; i++) {
            for (var j = 0; j < cols; j++) {
                var pixel = imageData[i][j];
                
                var color = `rgb(${pixel[0]}, ${pixel[1]}, ${pixel[2]}, ${pixel[3]})`;

                context.fillStyle = color;
                context.fillRect(j, i, 1, 1);
            }
        }
        creatureImage.style.width = "100%";
        creatureImage.style.height = "100%";
        creatureImage.style.position = 'absolute';
        // Add <canvas> element to image dictionary
        this.creatureImages[refId] = creatureImage;

    }

    /**
     * Update front-end elements based on information received from the back-end
     * @param {JSON} data Information from back-end simulation 
     */
    handleData(data){
        // Extract information
         var position = data["position"];
         var numConsumer = data["consumerCount"];
         var numProducer = data["producerCount"];
         var isWall = data["isWall"];
         var temp = data["temperature"];
         var lightLevel = data["light"];
         var creatureImageReferences = data["creatureImages"];
         var cell = this.cells[this.width * position[0] + position[1]];
         for(var reference of creatureImageReferences){
            cell.addCreatureVisual(this.creatureImages[reference]);
         }
         cell.updateProperties(numConsumer, numProducer, isWall, temp, lightLevel);
    }

    // Request simulation grid data from server every 0.500 seconds
    runSimulation(){
        this.simulationID = setInterval(() => {this.getGridData()}, 550);
    }

    // Stop sending simulation grid data requests
    pauseSimulation(){
        console.log("stopping calls..");
        clearInterval(this.simulationID);
    }

    /**
     * Display specified Overlay for Simulation Grid
     * @param {bool} isDisplayed Display overlay?
     * @param {string} mode overlay mode, heatmap or lightmap
     */
    toggleOverlayDisplay(isDisplayed, mode){
        for(let cell of this.cells){
            cell.toggleCellOverlay(isDisplayed, mode);
        }
    }
    

    //USED FOR DEBUGGING
    print(){
        for(let cell of this.cells){
            cell.print();
        }
    }
}