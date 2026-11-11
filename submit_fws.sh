#!/bin/bash
#SBATCH --time=7-00:00:00                        # Time limit for the job (REQUIRED).
#SBATCH --job-name=workflow                      # Job name
#SBATCH --ntasks=1                               # Number of cores for the job. Same as SBATCH -n 1
#SBATCH --cpus-per-task=8
#SBATCH --partition=normal                       # Partition/queue to run the job in. (REQUIRED)
#SBATCH -e slurm_out/workflow-%j.err             # Error file for this job.
#SBATCH -o slurm_out/workflow-%j.out             # Output file for this job.
#SBATCH -A coa_cmri235_uksr                      # Project allocation account name (REQUIRED)

source /home/rdu230/.bashrc;
conda activate /home/rdu230/miniconda3/envs/fw_workflows
module load ccs/gaussian/g16-A03
export PYTHONPATH=$PYTHONPATH:/home/rdu230/d3tales_api/
export FW_CONFIG_FILE=/scratch/rdu230/Comp_FW_Workflow/config/FW_config.yaml

cd /scratch/rdu230/Comp_FW_Workflow/runfiles

rlaunch singleshot

