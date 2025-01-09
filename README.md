# CorrJoin in Python

## Overview
This repository contains the codebase for my bachelor's thesis. Follow the instructions below to set up and run the program.

## Prerequisites
- [Anaconda](https://docs.anaconda.com/anaconda/install/#basic-install-instructions)

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/felixmerz00/bachelor-thesis.git
   cd bachelor-thesis
   ```

2. [**Set Up the Conda Environment**](#create_conda_env)

<a id="run_main"></a>

3. **Run the Program**
   Start the program by executing the main script:
   ```bash
   python src/corr_join/main.py
   ```

4. **Generate Plots**
   To generate plots, run the following command:
   ```bash
   python3 src/corr_join/plot.py
   ```

## Customization

- **Change Run Parameters**: You can inspect or modify the configuration of the program in the file [main.py](https://github.com/felixmerz00/bachelor-thesis/blob/main/src/corr_join/main.py) and the configuration of the parameters in the file [util.py](https://github.com/felixmerz00/bachelor-thesis/blob/main/src/corr_join/util.py).

- **Customize Plots**: To edit the plotting logic, modify the file [plot.py](https://github.com/felixmerz00/bachelor-thesis/blob/main/src/corr_join/plot.py).


<a id="create_conda_env"></a>
## Create Conda Environment

### Method 1: Using the Environment File

**Set Up the Conda Environment**
   Create a Conda environment using the provided environment file:
   ```bash
   conda env create -f environment.yml
   conda activate conda-env-ba
   ```
   For more information see [Creating an environment from an environment.yml file](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).

### Method 2: Manual Installation

1. [**Create a Conda Environment with commands**](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)
   ```bash
   conda create --name conda-env-ba
   conda activate conda-env-ba
   ```

2. **Install Dependencies Manually**
   [Run the main program](#run_main), and install any missing modules via conda as they appear. If a module is not available via Conda install it using pip.

3. **Repeat Step 2** until all dependencies are installed and the program runs successfully.
