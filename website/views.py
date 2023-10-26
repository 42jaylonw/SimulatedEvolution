from flask import Blueprint, render_template, jsonify, request
import games.sprint_0_random.random_moving as random_moving
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
        simulator = random_moving.generate_sim(1000, 50)
    # return the starting state of the simulator
    return jsonify(random_moving.get_initial_positions(simulator))

# Update the state of the simulation grid and send it to the webpage
@views.route('/get_grid_data', methods=["GET"])
def get_grid_data():
    global simulator
    # return the updated position of creatures
    return jsonify(random_moving.get_updated_positions(simulator))