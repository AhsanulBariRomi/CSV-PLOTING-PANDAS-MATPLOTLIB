# Simulation Validation: Legacy TCP vs Modern gRPC

This repository contains the validation scripts and data for comparing the macroscopic and microscopic physics output of a Legacy TraCI TCP coupling versus a Modern gRPC coupling in an OMNeT++ and SUMO traffic simulation.

## Data Processing & Visualization Tools

The `plot_validation.py` script leverages the following Python data science libraries to process the simulation data and generate the validation dashboard:

* **Pandas**: Used for loading the heavy CSV datasets, standardizing columns, sorting data chronologically by simulation time and vehicle ID, and performing complex aggregations (like computing the network's average speed, average acceleration, or active vehicle counts per second).
* **Matplotlib**: Used as the visualization engine to take the processed data and render the 3x2 grid validation dashboard, including line plots, legends, and the spatial coordinate map overlay.
* **NumPy**: While not imported directly, NumPy runs under the hood of Pandas to provide the high-performance numerical calculations necessary to process the 54,000+ rows of simulation physics data almost instantaneously.

## How to Run the Script

1. Ensure we have the required libraries installed in our Python environment. we can verify this by running:
   ```bash
   python3 -c "import pandas; import matplotlib.pyplot as plt; print('Libraries are installed and ready')"
   ```

2. Open the terminal (or WSL) and navigate to the project directory: for example:
   ```bash
   cd "/mnt/f/4. Academic(MSc)/Thesis/PLOT"
   ```

3. Run the validation plotting script:
   ```bash
   python3 plot_validation.py
   ```

4. Upon completion, the script will automatically generate and save a high-resolution image named `thesis_validation_dashboard.png` in the same directory.