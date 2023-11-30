
class CreatureVisual{
    constructor(referenceId, imageData){
        this.element = document.createElement('canvas');
        var context = this.element.getContext('2d');
        var scaleFactor = 2;
        // Set this.element dimensions based on the image data
        var rows = imageData.length;
        var cols = imageData[0].length;
        this.element.width = cols * scaleFactor;
        this.element.height = rows * scaleFactor;
        // Scale the this.element context
        context.scale(scaleFactor, scaleFactor);
        // Iterate through the image data and draw pixels on the this.element
        for (var i = 0; i < rows; i++) {
            for (var j = 0; j < cols; j++) {
                var pixel = imageData[i][j];
                //Assign color (including opacity)
                var color = `rgb(${pixel[0]}, ${pixel[1]}, ${pixel[2]}, ${pixel[3]})`;
                //Draw image
                context.fillStyle = color;
                context.fillRect(j, i, 1, 1);
            }
        }
        //Specify style
        this.element.style.width = "100%";
        this.element.style.height = "100%";
        this.element.style.position = 'absolute';
    }
}
//Store visual information of Creatures as a list
class CreatureVisuals{

    constructor(){
       this.visuals = {};
    }

    addCreatureVisual(referenceId, imageData){
       this.visuals[referenceId] = new CreatureVisual(referenceId, imageData);
    }

    getCreatureVisual(referenceId){
        if(this.visuals[referenceId] === undefined){
            throw  `Invalid referenceId: ${referenceId}`;
        }
        return this.visuals[referenceId].element;
    }

}
