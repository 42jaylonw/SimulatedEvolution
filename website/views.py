from flask import Blueprint, render_template, request, flash, redirect
import json
from website import validation
import numpy as np
from games.survival.survival import SurvivalSim
import sim_to_frontend as sim_to_front
views = Blueprint('views', __name__)


# simulator information for user session
simulator = None
isSetup = False
isActive = False
size = None
NUMCONSUMERS = 1
NUMPRODUCERS = 1
GENERATIONS = 1
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
    global GENERATIONS
    # Received user input
    if request.method == "POST":
        # Start simulation
        if isSetup and simulator is not None:
            isActive = True
            isSetup = False
            # Train creatures in simulation by user specified generations
            simulator.train(GENERATIONS)
            return render_template("home.html", grid_size=size, initSimParameters=simulator, simulationSetup=isSetup, activeSimulation=isActive)
        isSetup = True
        isActive = False
        # get user specified simulation grid size
        user_size = request.form.get("gridSize")
        # get user specified generations
        user_generations = request.form.get("numGenerations")
       
        # validate the input
        res = validation.validateSimulationParameters(user_size, user_generations)
        # Create simulation if user entered valid input
        if res == 'OK':
            size = int(user_size)
            GENERATIONS = int(request.form.get("numGenerations"))
        
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
    # initialize Simulator if one has not been made
    global simulator
    gridSize = json.loads(request.data)["size"]
    if simulator is None:
        simulator = sim_to_front.create_sim(NUMPRODUCERS, NUMCONSUMERS, gridSize)
    # return information of the simulator
    return sim_to_front.get_sim_state(simulator, includeImageData=True)


# Create a new simulation with the same parameters
@views.route('/new_grid', methods=["GET"])
def new_grid():
    """Create a new grid on backend then send it to front"""
    global simulator
    global size
    # Create a simulation
    simulator = sim_to_front.create_sim(NUMPRODUCERS, NUMCONSUMERS, size)
    # return the information of the newly created simulation
    return sim_to_front.get_sim_state(simulator, includeImageData=True)


# Update the state of the simulation grid and send it to the webpage
@views.route('/get_grid_data', methods=["GET"])
def get_grid_data():
    """Perform SimSpace Step then update front-end"""
    simulator.step()
    return sim_to_front.get_sim_state(simulator, includeImageData=True)

# Retrieve detailed information at specified grid space
@views.route('/get_creatures_at_grid_space', methods=["POST"])
def get_creatures_at_grid_space():
    position = json.loads(request.data)["position"]
    return sim_to_front.get_creatures_wrapper(simulator, position)

# Create a new simulation with different properties
@views.route('/reset_simulator', methods=["POST"])
def clear_simulation():
    # Clear all values
    global size
    global simulator
    global isActive
    global isSetup
    simulator = None
    size = None
    isSetup = False
    isActive = False
    return redirect('/')

# Add a wall to the back-end SimSpace simulator
@views.route('/add_wall', methods=["POST"])
def add_wall():
    position = json.loads(request.data)["position"]
    position = np.array(position)
    sim_to_front.user_place_wall(simulator, position)
    
    return sim_to_front.get_gridspace_state(simulator, position)

# Remove all objects at a specified location in a SimSpace Simulator
@views.route('/erase_space', methods=["POST"])
def erase_space():
    position = json.loads(request.data)["position"]
    position = np.array(position)
    # Return update Simspace if an emitter is erased
    has_emitter = len(simulator.layer_system.get_gridspace(position).get_emitters()) > 0
    sim_to_front.user_erase_space(simulator, position)
    if has_emitter:
        return sim_to_front.get_sim_state(simulator)
    # Otherwise return updated gridspace(1 tile)
    return sim_to_front.get_gridspace_state(simulator, position)

# Add a consumer to the back-end SimSpace simulator
@views.route('/add_creature_consumer', methods=["POST"])
def add_consumer():
    position = json.loads(request.data)["position"]
    position = np.array(position)
    # Load a genome for a creature if desired
    preset_id = json.loads(request.data)["preset-id"]
    sim_to_front.user_place_consumer(simulator, position, preset_id)
    return sim_to_front.get_gridspace_state(simulator, position)

# Add a producer to the back-end SimSpace simulator
@views.route('/add_creature_producer', methods=["POST"])
def add_producer():
    position = json.loads(request.data)["position"]
    position = np.array(position)
    # Load a genome for a creature if desired
    preset_id = json.loads(request.data)["preset-id"]
    sim_to_front.user_place_producer(simulator, position, preset_id)
    return sim_to_front.get_gridspace_state(simulator, position)

# Add a light emitter to the back-end SimSpace simulator
@views.route('/add_lightsource', methods=["POST"])
def add_lightsource():
    position = json.loads(request.data)["position"]
    position = np.array(position)
    # Load specified emitter range and strength
    emit_range = json.loads(request.data)["emit_range"]
    emit_strength = json.loads(request.data)["emit_strength"]
    sim_to_front.user_place_lightsource(simulator, position, emit_range, emit_strength)
    return sim_to_front.get_sim_state(simulator)

# Add a heat emitter to the back-end SimSpace simulator
@views.route('/add_heatsource', methods=["POST"])
def add_heatsource():
    position = json.loads(request.data)["position"]
    position = np.array(position)
    # Load Specified emitter range and strength
    emit_range = json.loads(request.data)["emit_range"]
    emit_strength = json.loads(request.data)["emit_strength"]
    sim_to_front.user_place_heatsource(simulator, position, emit_range, emit_strength)
    return sim_to_front.get_sim_state(simulator)
