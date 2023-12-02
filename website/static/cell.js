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
        // document.addEventListener("DOMContentLoaded", () =>{
        this.analysisContainer = document.querySelector('.analysis-container');
        // });
        
        //Create HTML elements associated with Cell object
        this.createCellElement(position);
        this.createInfoDisplay();     
        this.createCellOverlay();   
    }
  
    /**
     * Create HTMl Element for Cell object
     * @param {int} position [X,Y] position in SimulationGrid (refer to simulation-grid.js)
     * @property {Element} Cell.element HTML element associated with Cell
     * @property {int} Cell.position [X,Y] position of Cell
     */
    createCellElement(position){
        //Create html element
        this.element = document.createElement('div');
        this.position = position;
        this.creatureList = Array();
        // Cell element id is 'cell-<row>-<col>'
        this.element.id = 'cell-' + this.position[0] + '-' + this.position[1];
        //Add style classification for cell
        this.element.classList.add('cell-item');
        this.element.style.backgroundColor = "white";
        //Add event listeners
        //Mark cell when user hovers over it
        this.element.onmouseenter = () => {this.decreaseCellOpacity()};
        //Unmark cell when user no longer hovers over it
        this.element.onmouseleave = () => {this.restoreCellOpactiy()};
        //Display detailed information about Cell when user clicks on it
        // this.element.onclick = () => {this.displayCellInfo()};
    }

    addDisplayCellInfo(){
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
        //Format cell position to send to Python backend
        const data = {position: this.position};
        //Make the POST request
        fetch('/get_creatures_at_grid_space', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)})
        .then((response) => response.json())
        //Post Request SUCCESS, Perform operations on response(cellLayerData)
        .then((payload) => {
            var producers = payload["producers"];
            var consumers = payload["consumers"];
            this.analysisContainer.innerHTML =   `<h2 class="text-center" class="details-text">Information at ${this.position}</h2> ` + 
                this.generateCreatureText("CONSUMERS", consumers) + "<br>" + this.generateCreatureText("PRODUCERS", producers);
        })
        //POST Request FAILED
        .catch((error) =>{
            console.error('Error:', error);
        });
    }

    /**
     * 
     * @param {string} creatureClass name of type of creature 
     * @param {*} creatures Creature along with its properties
     * @returns {string} formatted string that contains a creature's properties
     */
    generateCreatureText(creatureClass, creatures){
        var creatureText = creatureClass
        for(let creature of creatures){
            creatureText += `<p>Genome: ${creature["genome"]} <br>Size: ${creature["size"]} <br>Energy ${creature["energy"]} </p>`;
        }
        return creatureText
    }
    /**
     * Update Cell properties
     * @param {int} numConsumer Number of consumers to set in Cell
     * @param {int} numProducer Number of producers to set in Cell
     * @param {boolean} isWall set this cell as a Wall?
     * @param {int} temp Temperature to set at this Cell
     * @property {int} Cell.numConsumers Total number of Consumers in this Cell
     * @property {int} Cell.numProducers Total number of Producers in this Cell
     * @property {int | float} Cell.temperature Temperature at this Cell
     * @property {bool} Cell.isWall Is this Cell a wall?
     * @property {Element} Cell.infoDisplay.innerHTML The HTML text associated with the Cell.infoDisplay container
     */
    updateProperties(numConsumer, numProducer, isWall=false, temp=0, lightLevel=0){
        this.numConsumers = numConsumer;
        this.numProducers = numProducer;
        this.temperature = temp;
        this.lightLevel = lightLevel;
        this.isWall = isWall;
        if(this.numConsumers <= 0){
            this.clearCreatureVisuals();
        }
        //Display different based on whether the Cell is a Wall
        if(this.isWall){
            this.infoDisplay.innerHTML = "Wall";
            this.setCellColor(`rgb(${(0)}, ${(0)}, ${(0)})`);
            // this.clearCreatureVisuals();
            return;
        }
        //No Creatures present
        if(this.numConsumers <= 0 && this.numProducers <= 0){
            this.setCellColor("white");
            // this.clearCreatureVisuals();
        }
        //Set color to Producer
        if(this.numProducers > 0){
            this.setCellColor(`rgb(${(0.5*255)}, ${(0.96 * 255)}, ${(0)})`);
        }
        //Update display information for this cell
        this.infoDisplay.innerHTML = `Temperature: ${this.temperature}<br>Light-level ${this.lightLevel}` + '<br>' + `Consumers: ${this.numConsumers}` + 
            '<br>' + `Producers: ${this.numProducers}` +  
            '<p class="text-center" class="details-text">click for details</p>';
        
        //Update the overlay at this Cell
        // this.updateCellOverlay(); 
    }

    /**
     * Add Creature Visual to Cell 
     * @param {Canvas} creature <canvas> element containing 8-bit visual of a creature 
     */
    addCreatureVisual(creature){
        if(creature === undefined){
            return;
        }
        // Add element to Cell and store it in a list
        this.element.append(creature);
        this.creatureList.push(creature);
    }
   
    /**
     * Clear local list of Creature visuals(8-bit images)
     * And remove their associated <canvas> elements from Cell
     */
    clearCreatureVisuals(){
        // Remove elements
        for(var elt of this.creatureList){
            if(this.element.contains(elt)){
                this.element.removeChild(elt);
            }
            
        }
        // Clear local list
        this.creatureList = Array();
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
     * a color associated with its properties such as temperature or light-level
     * @property {Element} this.overlay  HTML container that displays general Cell information
     */
    createCellOverlay(){
        this.overlay = document.createElement('div');
        this.overlay.classList.add('cell-overlay');
        this.overlay.id = "cell-overlay";
        this.element.appendChild(this.overlay);
        this.toggleCellOverlay(false);
    }

    /**
     * Display Cell overlay
     * @property {Element} this.overlay  HTML container that displays general Cell information
     */
    toggleCellOverlay(showOverlay, mode){
        this.updateCellOverlay(mode);
        if(showOverlay){
            this.overlay.style.display = 'block';
        }
        else{
            this.overlay.style.display = 'none';    
        }
        
    }

     /**
     * Change Cell overlay based on mode
     * @property {Element} this.overlay  HTML container that displays general Cell information
     * @property {int | float} this.temperature Temperature at Cell
     */
    updateCellOverlay(mode){
        let color;
        if(mode == "lightmap" || mode == "/add_lightsource"){
            color = `rgb(0,0,0, ${(100 - this.lightLevel) / 100})`; // WIP - magic numbers should be replaced later
            this.overlay.style.backgroundColor = color;
            return;
        }

        if (this.temperature < 20) 
        {
            color = `rgb(0,0,255, 0.3)`;
        } 
        else if (this.temperature < 40) 
        {
            color = `rgb(0,255,255, 0.3)`;
        } 
        else if (this.temperature < 60) 
        {
            color = `rgb(0,255,0, 0.3)`;
        } 
        else if (this.temperature < 80) 
        {
            color = `rgb(255,255,0, 0.3)`;
        } 
        else 
        {
            color = `rgb(255,0,0, 0.3)`;
        }
       
        this.overlay.style.backgroundColor = color;
    }

    //USED FOR DEBUGGING
    print(){
        console.log("CONSUMERS:" + this.numConsumers + " PRODUCERS: " + this.numProducers + " At position: " + this.position);
    }
}

