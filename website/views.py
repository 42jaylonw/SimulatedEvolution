from flask import Blueprint, render_template, jsonify, request
import games.sprint_0_random.random_moving as random_moving
import random
import json
#TEMP
import temp_sim_to_frontend as sim_to_front
#END TEMP
views = Blueprint('views', __name__)

NUMCONSUMERS = 5
NUMPRODUCERS = 3
# NOTE: Currently, Changing GRIDSIZE also requires change at line 2 of frontend-main.js
GRIDSIZE = 50
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
    """Initialize SimSpace"""
     # initialize Simulator if one has not been made
    global simulator
    if simulator is None:
        # Should use post request data to create simulation
        # request.json["position"]
        simulator = sim_to_front.create_sim(NUMPRODUCERS, NUMCONSUMERS, GRIDSIZE)
    return sim_to_front.get_sim_state(simulator)



@views.route('/new_grid', methods=["GET"])
def new_grid():
    """Create a new grid on backend then send it to front"""
    global simulator
    simulator = sim_to_front.create_sim(NUMPRODUCERS, NUMCONSUMERS, GRIDSIZE)
    return sim_to_front.get_sim_state(simulator)


# Update the state of the simulation grid and send it to the webpage
@views.route('/get_grid_data', methods=["GET"])
def get_grid_data():
    """Perform SimSpace Step then update front-end"""
    global simulator
    simulator.step()
    return sim_to_front.get_sim_state(simulator)

@views.route('/get_creatures_at_grid_space', methods=["POST"])
def get_creatures_at_grid_space():
    position = json.loads(request.data)["position"]
    global simulator
    return sim_to_front.get_creatures_wrapper(simulator, position)
    # return {"genome": "28ue93hw", "size": 2, "energy" : 95}