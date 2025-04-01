# Cancer-sim_python
A agent based model of cancer 

# **Simulation Pipeline Overview**

## **Overview**
This project provides a pipeline for running and analyzing cellular model simulations. The pipeline includes several modules that handle different parts of the process: converting simulation data to images, generating simulations, writing simulation parameters, running simulations over a range of parameters, and visualizing the results with graphs.

## **Modules**

### 1. **`imageConverter.py`** – **Converting 2D Arrays to Images**
- **Purpose**: This module provides functions to convert 2D arrays (typically simulation data representing cell states) into image format. The data can be visualized as images to better understand the simulation output at each time step.
- **Key Functionality**: 
    - Converts 2D arrays to image files (e.g., PNG, JPEG) for visualization.
    - Useful for visualizing the state of a simulation at a specific time point.
- **Use Case**: This is primarily used for visualizing the spatial distribution of cells during the simulation.

### 2. **`timeStep.py`** – **Simulation Engine**
- **Purpose**: This file serves as the "engine" for running simulations. It generates a simulation for each time step based on provided parameters, performing calculations and updating the simulation state.
- **Key Functionality**:
    - Generates simulations step by step (time steps).
    - Can model cell population dynamics (e.g., growth, resistance, death).
- **Use Case**: This file is responsible for carrying out the core computations of the simulation, iterating over time and applying rules based on the model.

### 3. **`writeParams.py`** – **Writing Simulation Parameters**
- **Purpose**: This module contains a function that writes simulation parameters to a file, ensuring that all relevant parameters for the simulation are recorded and can be easily reused or adjusted.
- **Key Functionality**:
    - Writes the parameters for the simulation to a file (e.g., a text file or JSON).
    - Useful for reproducibility and keeping track of simulation configurations.
- **Use Case**: Use this to save the parameters you plan to use for the simulation, ensuring consistent and transparent experimental setups.

### 4. **`CM_simulation.py`** – **Running Simulations Over Multiple Parameters**
- **Purpose**: This file allows running simulations over a wide range of parameters. It can iterate over various input parameters to explore different simulation outcomes, helping in the search for the optimal or most interesting configurations.
- **Key Functionality**:
    - Handles running simulations with different sets of parameters.
    - Can be used to evaluate the effect of changing input parameters on the simulation results.
- **Use Case**: This file is essential when testing multiple configurations or optimizing the simulation by varying input parameters.

### 5. **`convert_to_graphs.py`** – **Generating Graphs from Simulation Data**
- **Purpose**: After running the simulations, this module takes the resulting data and generates informative graphs (e.g., population trends, death rates) to analyze and visualize the results.
- **Key Functionality**:
    - Reads simulation output data.
    - Generates various types of graphs and plots to visualize the behavior of the simulated system over time.
- **Use Case**: This is the final step in the pipeline where data from the simulation is analyzed visually through graphs to derive insights from the simulation.

## **Workflow**
1. **Running the Simulation**:
   - First, parameters for the simulation are written and configured using `writeParams.py`.
   - Then, the simulation is generated step-by-step using `timeStep.py`, which performs the core computations.
   - For multiple configurations, `CM_simulation.py` can run simulations over a broad range of parameter sets to explore different scenarios.
   
2. **Converting Data**:
   - Once the simulation runs, the results (2D arrays) can be converted into image format using `imageConverter.py` for visual representation at each time step.

3. **Analyzing Results**:
   - Finally, `convert_to_graphs.py` takes the output from the simulation, processes it, and generates insightful graphs and charts that help in analyzing the trends and behaviors of the simulated system.

## **Conclusion**
This project pipeline allows you to set up, run, and analyze complex cellular simulations. By breaking down the tasks into modules—parameter setup, simulation execution, image conversion, and graph generation—it provides an efficient and modular approach to running and visualizing simulations over different parameter sets. 