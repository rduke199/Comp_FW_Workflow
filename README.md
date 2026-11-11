# D<sup>3</sup>TaLES High-throughput Workflow Management
This repository contains [Fireworks](https://materialsproject.github.io/fireworks/)-based code for implementing 
high-throughput calculations for the [D<sup>3</sup>TaLES database](https://d3tales.as.uky.edu/database/). The
contents of this repository include

- `config`: Directory containing example [Fireworks](https://materialsproject.github.io/fireworks/) 
configuration files. 

- `populate_workflows`: Directory containing scripts for workflow management including the `populate_lpad` files 
for launching high-throughput quantum chemical workflows

- `parameters`: Directory containing parameter files that set the parameters (e.g., functional, basis set, etc.)
for high-throughput calculations 


Most of the most useful code in this repository will be found in the `workflows` directory. 


## Clone this Repo

Clone this repository to use the scripts. 
```bash
git clone git@github.com:rduke199/Comp_FW_Workflow.git
```

## Environment
The primary package this repo requires is the [D<sup>3</sup>TaLES API](https://github.com/D3TaLES/d3tales_api). 
It is recommended that you create an environment to host the required packages. 

Note that you must set the fireworks variable `FW_CONFIG_FILE` (see the [Fireworks website](https://materialsproject.github.io/fireworks/) 
for more details) and a `PYTHONPATH`. For example, a user might set the environment variables as follows: 
```bash
conda env create workflows
conda activate workflows
pip install d3tales_api
export PYTHONPATH='C:/Users/Lab/Comp_FW_Workflow'
export FW_CONFIG_FILE='C:/Users/Lab/d3tales_fw/Comp_FW_Workflow/config.yaml'
```


## Running and Viewing Jobs

To view jobs run: 
```bash
lpad webgui
```

To launch a workflow or a series of  workflows for given molecule(s), use a 
`populate_workflows/populate_*_lpad.py` script. 