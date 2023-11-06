class Cell
{
    constructor(id)
    {
     
        this.element = document.createElement('div');
        // Cell id is 'cell-<row>-<col>'
        this.element.id = id;
        //Add style classification for cell
        this.element.classList.add('grid-item');
        this.element.style.backgroundColor = "white";
        //Add event listeners to each cell
        this.element.onmouseenter = () => {this.showCellBorder()};
        this.element.onmouseleave = () => {this.hideCellBorder()};
        this.element.onclick = () => {this.displayCellInfo()};
    }

    //Create an outline for each cell that the mouse hovers over
    showCellBorder()
    {
        // cell.style.border = "3px solid black";
        this.element.style.opacity = 0.5;
    }

    //Remove outline when mouse leaves cell
    hideCellBorder()
    {
        // cell.style.border = "none";
        this.element.style.opacity = 1;
    }

    displayCellInfo()
    {
        console.log(this);
    }
}