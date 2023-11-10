from flask import Blueprint, render_template, jsonify, request
import games.sprint_0_random.random_moving as random_moving
import random

views = Blueprint('views', __name__)



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

# Create a simulation and send the state to the webpage
@views.route('/setup_grid', methods=["GET"])
def set_grid():
    # initialize Simulator if one has not been made
    global simulator
    if simulator is None:
        simulator = random_moving.generate_sim(0, 10)
    # return the starting state of the simulator
    return jsonify(random_moving.get_initial_positions(simulator))

@views.route('/new_grid', methods=["GET"])
def new_grid():
    global simulator
    simulator = random_moving.generate_sim(0, 10)
    return jsonify(random_moving.get_initial_positions(simulator))


# Update the state of the simulation grid and send it to the webpage
@views.route('/get_grid_data', methods=["GET"])
def get_grid_data():
    global simulator
    # return the updated position of creatures
    return jsonify(random_moving.get_updated_positions(simulator))

@views.route('/get_cell_data', methods=["POST"])
def get_cell_data():
    global simulator

    cell_location = request.json["position"]
    cell_info = random_moving.get_location_info(simulator)
    layers_at_cell = cell_info[:, cell_location[0], cell_location[1]].tolist()
    if(layers_at_cell[2] == 1):
        print(type(layers_at_cell[2]))
    return jsonify(layers_at_cell)

@views.route('/generate_mock_climate')
def get_climate_data():
    temperatures = [random.random() for _ in range(2500)]
    return jsonify(temperatures)