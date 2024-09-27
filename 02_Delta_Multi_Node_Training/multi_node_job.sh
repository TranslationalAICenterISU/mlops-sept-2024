#!/bin/bash
# Copy/paste this job script into a text file and submit with the command:
#    sbatch multi_node_job.sh
#SBATCH --time=1:00:00   # walltime limit (HH:MM:SS)
#SBATCH --nodes=1  # number of nodes
#SBATCH --mem=64g
#SBATCH --account=bcjh-delta-gpu 
#SBATCH --partition=gpuA100x4
#SBATCH --gpus-per-node=4
#SBATCH --ntasks-per-node=4 # 16 processor core(s) per node 
#SBATCH --job-name="multi_node"
#SBATCH --mail-user=baditya@iastate.edu   # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --output="multi_node_op.txt" # job standard output file (%j replaced by job id)
#SBATCH --error="multi_node_error.e" # job standard error file (%j replaced by job id)
# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
module load anaconda3_gpu/23.9.0
source activate mlops
srun python multi_node_delta.py