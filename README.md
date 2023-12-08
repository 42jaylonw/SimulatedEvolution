# Evolution Simulator

---

**Evolution Simulator** is an innovative neural-network based software designed to visually simulate the process of evolution. This software provides a unique front-end display where users can observe virtual creatures adapting over time within user-defined environments. With a range of tools available, users can craft diverse environments and populate them with organisms, then watch as these organisms evolve and adapt to their surroundings.

# Getting Started

### Prerequisites

1. Install python tutorial [here](https://kinsta.com/knowledgebase/install-python/).
2. Install Python dependencies
    
    ```jsx
    pip install -r requirements.txt
    ```
3. run example internal evolution training. This will show some of the training process that occurs behind the scenes. 
   ```commandline
   python -m games.survival.survival
   ```
   press `q` to quit the simulation

<p align="center">
  <img src="./docs/train_result/train_Gen0_SurvivalRate0.15.gif" alt="Generation 0" width="30%" />
  <img src="./docs/train_result/train_Gen2_SurvivalRate0.25.gif" alt="Generation 2" width="30%" />
  <img src="./docs/train_result/train_Gen5_SurvivalRate0.825.gif" alt="Generation 5" width="30%" />
</p>
<p align="center">
  <em>Generation 0</em> | <em>Generation 1</em> | <em>Generation 5</em>
</p>

### Running the application

Once the necessary dependencies have been installed, run main.py. This can be achieved in terminal by calling the following command.

```python
python -m main
```

> If you encounter an error with dependencies after installing *requirements.txt*, run the commands in **Known Bugs.**
> 

After running main you will see:

```jsx
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

Visiting the displayed address will take you to the local webpage where you can use the Evolution Simulator.

# Documentation

[Here](https://lumbar-haddock-2e2.notion.site/Evolution-Simulation-e12f50a180fe490a842e340b1ee03c76) is the documentation.

### Known Bugs

If you have trouble installing the program after installing *requirements.txt*, the following commands are a known fix.

```python
pip install flask
pip install toml
pip install opencv-python
sudo apt-get update
sudo apt-get install libgl1-mesa-glx
```