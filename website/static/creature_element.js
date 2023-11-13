class CreatureElement{
    constructor(position, color){
        this.position = position;
        this.color = color;
        this.cellId = 'cell-' + position[0] + '-' + position[1];
        this.element = document.createElement('div');
        this.element.classList.add('creature');
        this.element.style.backgroundColor = `rgb(${(color[0] *255)}, ${(color[1] * 255)}, ${(color[2] * 255)})`;
        //Add listener
        this.element.onclick = () => {this.displayInfo()};
    }

    displayInfo(){
        console.log(`${this.cellId} with properties: \nColor: ${this.color}\nEnd`);
        this.idk();
    }

    idk()
    {
        console.log('idk');
    }
}