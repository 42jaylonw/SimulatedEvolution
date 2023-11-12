from flask import Blueprint, render_template, jsonify, request
import games.sprint_0_random.random_moving as random_moving
import random

views = Blueprint('views', __name__)

NUMCONSUMERS = 1
NUMPRODUCERS = 0
GRIDSIZE = 2
# simulator for user session
simulator = None

# Home Page
@views.route('/', methods=["GET", "POST"])
def home_page():
    return render_template("home.html")  

# About Page
@views.route('about')
def about_page():
    return render_template("about.html")

@views.route('/new_setup_grid')
def new_set_grid():
     # initialize Simulator if one has not been made
    global simulator
    if simulator is None:
        simulator = random_moving.generate_sim(NUMPRODUCERS, NUMCONSUMERS)

    gridspacesInformation = []
    for i in range(GRIDSIZE):
        for j in range(GRIDSIZE):
           #[(a,b,b,c)]
           gridspacesInformation.append(simulator.layer_system.get_gridspace([i,j]).get_properties())
    print("NEW_SETUP_GRID",gridspacesInformation)
    return jsonify(gridspacesInformation)




# Create a simulation and send the state to the webpage
@views.route('/setup_grid', methods=["GET"])
def set_grid():
    # initialize Simulator if one has not been made
    global simulator
    if simulator is None:
        simulator = random_moving.generate_sim(NUMPRODUCERS, NUMCONSUMERS)
 
    # return the starting state of the simulator
    creaturePositions = [(creature.grid_pos, creature.rgb) for creature in simulator.creatures]
    wallPositions = [wall.position.tolist() for wall in simulator.walls]
    idk = []
    for i in range(GRIDSIZE):
        for j in range(GRIDSIZE):
           curGridSpace = simulator.layer_system.get_gridspace([i,j])
           # (position, layerinformation)
           idk.append(([i,j], simulator.layers[:, i, j].tolist()))
    return jsonify([creaturePositions, wallPositions, idk])


@views.route('/new_grid', methods=["GET"])
def new_grid():
    global simulator
    simulator = random_moving.generate_sim(NUMPRODUCERS, NUMCONSUMERS)
    creaturePositions = [(creature.grid_pos, creature.rgb) for creature in simulator.creatures]
    wallPositions = [wall.creaturePositionsion.tolist() for wall in simulator.walls]
    return jsonify([wallPositions])


# Update the state of the simulation grid and send it to the webpage
@views.route('/get_grid_data', methods=["GET"])
def get_grid_data():
    global simulator
    simulator.step()
    gridspacesInformation = []
    for i in range(GRIDSIZE):
        for j in range(GRIDSIZE):
           #[(a,b,b,c)]
           gridspacesInformation.append(simulator.layer_system.get_gridspace([i,j]).get_properties())
    return jsonify(gridspacesInformation)
    # return the updated position of creatures
    # return jsonify(random_moving.get_updated_positions(simulator))

@views.route('/get_cell_data', methods=["POST"])
def get_cell_data():
    global simulator

    cell_location = request.json["position"]
    # get Sim Layers
    cell_info = random_moving.get_location_info(simulator)
    # cell_info = [1,2]
    layers_at_cell = cell_info[:, cell_location[0], cell_location[1]].tolist()
    return jsonify(layers_at_cell)
