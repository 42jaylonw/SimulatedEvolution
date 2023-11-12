const Layer ={
    Producer: 1,
    Consumer: 2,
    Wall: 3,
    Elevation: 4,
    List:  5,
    Temperature: 6,
}
/**
 * @class Cell
 * @classdesc A class that creates Cells of a Simulation-grid object to establish
 * user interaction.
 * @prop {Element} Cell.element an HTML element associated with the Cell object
 * @prop {Array[Int]} Cell.position the [X,Y] location of the created Cell object
 */
class Cell{

    /**
     * Create a Cell object based on a given position
     * @param {Array[int]} position [X,Y] location to create a Cell object
     * @property {int} Cell.numConsumers Total number of Consumers in this Cell
     * @property {int} Cell.numProducers Total number of Producers in this Cell
     * @property {int | float} Cell.temperature Temperature at this Cell
     * @property {bool} Cell.isWall Is this Cell a wall?
     */
    constructor(position){
        this.numConsumers = 0;
        this.numProducers = 0;
        this.temperature = 0;
        this.isWall = false;
        //Create HTML elements associated with Cell object
        this.createCellElement(position);
        this.createInfoDisplay();     
        this.createCellOverlay();   
    }

    //Create HTMl Element for Cell object
    createCellElement(position){
        //Create html element
        this.element = document.createElement('div');
        this.position = position;
        // Cell element id is 'cell-<row>-<col>'
        this.element.id = 'cell-' + this.position[0] + '-' + this.position[1];
        //Add style classification for cell
        this.element.classList.add('cell-item');
        this.element.style.backgroundColor = "white";
        //Add event listeners
        this.element.onmouseenter = () => {this.decreaseCellOpacity()};
        this.element.onmouseleave = () => {this.restoreCellOpactiy()};
        this.element.onclick = () => {this.displayCellInfo()};
    }


    /**
     * Sets the background color of a cell element
     * @param {string|RGB} color The color to apply to the Cell.element
     * @property {Element} Cell.element The HTML element associated with a Cell object 
     */
    setCellColor(color){
        this.element.style.backgroundColor = color;
    }


    /**
     * Outline any Cell.element with a black border and display general information
     * such as the number of creatures present and temperature
     * @property {Element} Cell.element The HTML element associated with a Cell object
     * @property {Element} Cell.infoDisplay HTML container that displays general Cell information
     */
    decreaseCellOpacity(){
        this.element.style.border = "solid black";
        //Make information visible by setting opacity to 1
        this.infoDisplay.style.opacity = 1;
    }

     /**
     * Remove black border from Cell.element and hide general information
     * @property {Element} Cell.element The HTML element associated with a Cell object
     * @property {Element} Cell.infoDisplay HTML container that displays general Cell information
     */
    restoreCellOpactiy(){
        this.element.style.border = "none";
        //hide information by setting opacity to 0
        this.infoDisplay.style.opacity = 0;
    }

    /**
     * Method that displays all the layer information at a clicked Cell
     */
    displayCellInfo(){
        //Debug print
        console.log(`Output information of ${this.element.id} at position: ${this.position}`);
        console.log(this);
      
        
        // //Format cell position to send to Python backend
        // const data = {position: this.position};
        // //Make the POST request
        // fetch('/get_cell_data', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)})
        // .then((response) => response.json())
        // //Post Request SUCCESS, Perform operations on response(cellLayerData)
        // .then((cellLayerData) => {

        //    console.log(cellLayerData);
            
        // })
        // //POST Request FAILED
        // .catch((error) =>{
        //     console.error('Error:', error);
        // });
    }

    /**
     * Update Cell properties given an array of layer information
     * @param {Array[int]} layerInfo Information about each layer
     * @property {int} Cell.numConsumers Total number of Consumers in this Cell
     * @property {int} Cell.numProducers Total number of Producers in this Cell
     * @property {int | float} Cell.temperature Temperature at this Cell
     * @property {bool} Cell.isWall Is this Cell a wall?
     * @property {Element} Cell.infoDisplay.innerHTML The HTML text associated with the Cell.infoDisplay container
     */
    

    updateProperties(numConsumer, numProducer, isWall=false, temp=0){
        this.numConsumers = numConsumer;
        this.numProducers = numProducer;
        this.temperature = temp;
        //Check if this Cell is a Wall
        this.isWall = isWall;
        //Display different based on whether the Cell is a Wall
        if(this.isWall){
            this.infoDisplay.innerHTML = "Wall";
            this.setCellColor(`rgb(${(0)}, ${(0)}, ${(0)})`);
            return;
        }
        if(this.numConsumers <= 0 && this.numProducers <= 0){
            this.setCellColor("white");
            return;
        }
        if(this.numProducers > 0){
            this.setCellColor(`rgb(${(0.5*255)}, ${(0.96 * 255)}, ${(0)})`);
        }
        if(this.numConsumers > 0){
            
            this.setCellColor(`rgb(${(0.96 *255)}, ${(0.5 * 255)}, ${(0)})`);
        }
        this.infoDisplay.innerHTML = `Climate: ${this.temperature}` + '<br>' + `Consumers: ${this.numConsumers}` + 
            '<br>' + `Producers: ${this.numProducers}` + 
            '<p class="text-center" class="details-text">click for details</p>';
        
      
        
        this.updateCellOverlay(); 
    }
    updatePropertiesOLD(layerInfo){
        //Update Cell properties
        this.numConsumers = layerInfo[Layer.Consumer];
        this.numProducers = layerInfo[Layer.Producer];
        this.temperature = layerInfo[Layer.Temperature];
        //Check if this Cell is a Wall
        if(layerInfo[Layer.Wall] == 1){
            this.isWall = true;
        }
        //Display different based on whether the Cell is a Wall
        if(this.isWall){
            this.infoDisplay.innerHTML = "Wall";
        }
        else{
            this.infoDisplay.innerHTML = `Climate: ${this.temperature}` + '<br>' + `Consumers: ${this.numConsumers}` + 
                '<br>' + `Producers: ${this.numProducers}` + 
                '<p class="text-center" class="details-text">click for details</p>';
        }
        this.updateCellOverlay(); 
    }

    /**
     * Create HTML container called 'info-display' that displays
     * general information about a Cell when the user hover's over the Cell.
     * @property {Element} this.infoDisplay  HTML container that displays general Cell information
     */
    createInfoDisplay(){
        //Create new element 'info-display'
        this.infoDisplay = document.createElement('div');
        this.infoDisplay.classList.add('info-display');
        this.infoDisplay.style.opacity = 0; 
        this.element.appendChild(this.infoDisplay); 
    }

    /**
     * Create HTML container called 'cell-overlay' that displays
     * a color associated with its temperature property
     * @property {Element} this.overlay  HTML container that displays general Cell information
     */
    createCellOverlay(){
        this.overlay = document.createElement('div');
        this.overlay.classList.add('cell-overlay');
        this.element.appendChild(this.overlay);
        this.hideCellOverlay();
    }

    /**
     * Display Cell overlay
     * @property {Element} this.overlay  HTML container that displays general Cell information
     */
    displayCellOverlay(){
        this.overlay.style.display = 'block';
    }
     /**
     * Hide Cell overlay
     * @property {Element} this.overlay  HTML container that displays general Cell information
     */
    hideCellOverlay(){
        this.overlay.style.display = 'none';
    }

     /**
     * Change Cell overlay based on temperature value
     * @property {Element} this.overlay  HTML container that displays general Cell information
     * @property {int | float} this.temperature Temperature at Cell
     */
    updateCellOverlay(){
        let color;
        if (this.temperature < 20) 
            {
                color = `rgb(0,0,255, 0.25)`;
            } 
            else if (this.temperature < 40) 
            {
                color = `rgb(0,255,255, 0.25)`;
            } 
            else if (this.temperature < 60) 
            {
                color = `rgb(0,255,0, 0.25)`;
            } 
            else if (this.temperature < 80) 
            {
                color = `rgb(255,255,0, 0.25)`;
            } 
            else 
            {
                color = `rgb(255,0,0, 0.25)`;
            }
            this.overlay.style.backgroundColor = color;
        }

        print(){
            console.log("CONSUMERS:" + this.numConsumers + " PRODUCERS: " + this.numProducers + " At position: " + this.position);
        }
}

