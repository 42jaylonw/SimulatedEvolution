from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
import games.sprint_0_random.random_moving as random_moving
import random
import json
from website import validation
import numpy as np
#TEMP
import temp_sim_to_frontend as sim_to_front
#END TEMP
views = Blueprint('views', __name__)


# simulator information for user session
# TODO: make mini class to remove use of 'global' keyword
simulator = None
isSetup = False
isActive = False
size = None
NUMCONSUMERS = 1
NUMPRODUCERS = 1
# {#  (1)InitialSimulationParameters (2-3)simulationSetup, (4)ActiveSimulation #}
# Home Page
@views.route('/', methods=["GET", "POST"])
def home_page():
    global simulator
    global size
    global isSetup
    global isActive
    global NUMCONSUMERS
    global NUMPRODUCERS
    # Received user input
    if request.method == "POST":
        if isSetup:
            isActive = True
            isSetup = False
            return render_template("home.html", grid_size=size, initSimParameters=simulator, simulationSetup=isSetup, activeSimulation=isActive)
        isSetup = True
        isActive = False
        user_size = request.form.get("gridSize")
        user_consumers = request.form.get("numConsumers")
        user_producers = request.form.get("numProducers")
        # validate the input
        res = validation.validateSimulationParameters(user_size, user_consumers, user_producers)
        # Create simulation if user entered valid input
        if res == 'OK':
            NUMCONSUMERS = 3#int(user_consumers)
            NUMPRODUCERS = 1#int(user_producers)
            size = int(user_size)
            return render_template("home.html", grid_size=size, initSimParameters=True, simulationSetup=isSetup, activeSimulation=isActive)
        # otherwise flash error message
        else:
            flash(res, category="error")
    # display the current state of the grid every time the user visits home page
    return render_template("home.html", grid_size=size, initSimParameters=simulator, simulationSetup=isSetup, activeSimulation=isActive)  



# About Page
@views.route('about')
def about_page():
    return render_template("about.html")

# Create a simulation based on specified parameters
@views.route('/new_setup_grid', methods=["POST"])
def new_set_grid():
    """Initialize SimSpace"""
     # initialize Simulator if one has not been made
    global simulator
    gridSize = json.loads(request.data)["size"]
    if simulator is None:
        simulator = sim_to_front.create_sim(NUMPRODUCERS, NUMCONSUMERS, gridSize)
    return sim_to_front.get_sim_state(simulator, includeImageData=True)


# Create a new simulation with the same parameters
@views.route('/new_grid', methods=["GET"])
def new_grid():
    """Create a new grid on backend then send it to front"""
    global simulator
    global size
    # make a clone function that takes the information from the old sim then builds a new sim using the same information
    simulator = sim_to_front.create_sim(NUMPRODUCERS, NUMCONSUMERS, size)
    return sim_to_front.get_sim_state(simulator, includeImageData=True)


# Update the state of the simulation grid and send it to the webpage
@views.route('/get_grid_data', methods=["GET"])
def get_grid_data():
    """Perform SimSpace Step then update front-end"""
    simulator.step()
    # print("number of creatures: ", len(simulator.creatures))
    return sim_to_front.get_sim_state(simulator, includeImageData=True)

# Retrieve detailed information at specified grid space
@views.route('/get_creatures_at_grid_space', methods=["POST"])
def get_creatures_at_grid_space():
    position = json.loads(request.data)["position"]
    return sim_to_front.get_creatures_wrapper(simulator, position)

# Create a new simulation with different properties
@views.route('/reset_simulator', methods=["POST"])
def test():
    global size
    global simulator
    global isActive
    global isSetup
    simulator = None
    size = None
    isSetup = False
    isActive = False
    return redirect('/')

@views.route('/add_wall', methods=["POST"])
def add_wall():
    position = json.loads(request.data)["position"]
    position = np.array(position)
    sim_to_front.user_place_wall(simulator, position)
    
    return sim_to_front.get_gridspace_state(simulator, position)
@views.route('/erase_space', methods=["POST"])
def erase_space():
    position = json.loads(request.data)["position"]
    position = np.array(position)
    sim_to_front.user_erase_space(simulator, position)
    return sim_to_front.get_gridspace_state(simulator, position)

@views.route('/add_creature_consumer', methods=["POST"])
def add_consumer():
    global NUMCONSUMERS
    # NUMCONSUMERS += 1
    position = json.loads(request.data)["position"]
    position = np.array(position)
    preset_id = json.loads(request.data)["preset-id"]
    sim_to_front.user_place_consumer(simulator, position, preset_id)
    return sim_to_front.get_gridspace_state(simulator, position)

@views.route('/add_creature_producer', methods=["POST"])
def add_producer():
    global NUMPRODUCERS
    # NUMPRODUCERS += 1
    position = json.loads(request.data)["position"]
    position = np.array(position)
    sim_to_front.user_place_producer(simulator, position)
    return sim_to_front.get_gridspace_state(simulator, position)

@views.route('/add_lightsource', methods=["POST"])
def add_lightsource():
    position = json.loads(request.data)["position"]
    position = np.array(position)
    emit_range = json.loads(request.data)["emit_range"]
    emit_strength = json.loads(request.data)["emit_strength"]

    sim_to_front.user_place_lightsource(simulator, position, emit_range, emit_strength)
    return sim_to_front.get_sim_state(simulator)
    #return sim_to_front.get_gridspace_state(simulator, position)

@views.route('/add_heatsource', methods=["POST"])
def add_heatsource():
    position = json.loads(request.data)["position"]
    position = np.array(position)
    emit_range = json.loads(request.data)["emit_range"]
    emit_strength = json.loads(request.data)["emit_strength"]

    sim_to_front.user_place_heatsource(simulator, position, emit_range, emit_strength)
    return sim_to_front.get_sim_state(simulator)

@views.route('/visual_update', methods=["GET"])
def visual_update():
    return sim_to_front.get_gridspace_state(simulator)
