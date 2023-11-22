from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
import games.sprint_0_random.random_moving as random_moving
import random
import json
from website import validation

#TEMP
import temp_sim_to_frontend as sim_to_front
#END TEMP
views = Blueprint('views', __name__)


# simulator information for user session
# TODO: make mini class to remove use of 'global' keyword
simulator = None
size = None
NUMCONSUMERS = 1
NUMPRODUCERS = 1
# Home Page
@views.route('/', methods=["GET", "POST"])
def home_page():
    global simulator
    global size
    global NUMCONSUMERS
    global NUMPRODUCERS
    # Received user input
    if request.method == "POST":
        user_size = request.form.get("gridSize")
        user_consumers = request.form.get("numConsumers")
        user_producers = request.form.get("numProducers")
        # validate the input
        res = validation.validateSimulationParameters(user_size, user_consumers, user_producers)
        # Create simulation if user entered valid input
        if res == 'OK':
            NUMCONSUMERS = int(user_consumers)
            NUMPRODUCERS = int(user_producers)
            size = int(user_size)
            return render_template("home.html", grid_size=size, simulator=True)
        # otherwise flash error message
        else:
            flash(res, category="error")
    # display the current state of the grid every time the user visits home page
    return render_template("home.html", grid_size=size, simulator=simulator)  



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
        print("creating grid")
        simulator = sim_to_front.create_sim(NUMPRODUCERS, NUMCONSUMERS, gridSize)
    return sim_to_front.get_sim_state(simulator, includeImageData=True)


# Create a new simulation with the same parameters
@views.route('/new_grid', methods=["GET"])
def new_grid():
    """Create a new grid on backend then send it to front"""
    global simulator
    global size
    simulator = sim_to_front.create_sim(NUMPRODUCERS, NUMCONSUMERS, size)
    return sim_to_front.get_sim_state(simulator, includeImageData=True)


# Update the state of the simulation grid and send it to the webpage
@views.route('/get_grid_data', methods=["GET"])
def get_grid_data():
    """Perform SimSpace Step then update front-end"""
    simulator.step()
    return sim_to_front.get_sim_state(simulator)

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
    simulator = None
    size = None
    return redirect('/')