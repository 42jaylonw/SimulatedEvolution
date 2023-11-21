let myDict = {};
var scaleFactor = 5;
// Your image data
var imageData = [[[137, 83, 78], [137, 83, 78], [0, 0, 0], [137, 83, 78], [137, 83, 78]],
 [[0, 0, 0], [141, 83, 81], [137, 83, 78], [141, 83, 81], [0, 0, 0]], 
 [[137, 83, 78], [141, 83, 81], [141, 83, 81], [141, 83, 81], [137, 83, 78]], 
 [[0, 0, 0], [137, 83, 78], [72, 58, 170], [137, 83, 78], [0, 0, 0]], 
 [[196, 100, 52], [0, 0, 0], [0, 0, 0], [0, 0, 0], [196, 100, 52]]];

var mask = [[1, 1, 0, 1, 1],
[0, 1, 1, 1, 0],
[1, 1, 1, 1, 1],
[0, 1, 1, 1, 0],
[1, 0, 0, 0, 1]];
// Create a canvas element
var canvas = document.createElement('canvas');
var context = canvas.getContext('2d');

// Set canvas dimensions based on the image data
var rows = imageData.length;
var cols = imageData[0].length;
canvas.width = cols * scaleFactor;
canvas.height = rows * scaleFactor;
// Scale the canvas context
context.scale(scaleFactor, scaleFactor);
// Iterate through the image data and draw pixels on the canvas
for (var i = 0; i < rows; i++) {
    for (var j = 0; j < cols; j++) {
        var pixel = imageData[i][j];
        var maskValue = mask[i][j];
        // Check the mask value
        if (maskValue === 1) {
            // Apply the original pixel color
            var color = 'rgb(' + pixel[0] + ',' + pixel[1] + ',' + pixel[2] + ')';
        } else {
            // Set a specific color for masked pixels (e.g., black)
            var color = 'rgb(0, 0, 0, 0)';
        }
        // var color = 'rgb(' + pixel[0] + ',' + pixel[1] + ',' + pixel[2] + ')';

        context.fillStyle = color;
        context.fillRect(j, i, 1, 1);
    }
}
myDict["A"] = canvas;
myDict["B"] = canvas;

function addToBody(elt){
    document.body.appendChild(myDict[elt]);
    document.body.appendChild(myDict["B"]);
}

function removeFromBody(elt){
    document.body.removeChild(myDict[elt]);
}
// Append the canvas to the document body




