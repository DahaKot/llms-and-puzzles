#!/bin/bash

#SBATCH --job-name=rosetta_stone_llama8b_base # Job name
#SBATCH --error=logs/%j%x.err # error file
#SBATCH --output=logs/%j%x.out # output log file
#SBATCH --nodes=1                   # Run all processes on a single node    
#SBATCH --ntasks=1                  # Run on a single CPU
#SBATCH --mem=40G                   # Total RAM to be used
#SBATCH --cpus-per-task=8          # Number of CPU cores
#SBATCH -p cscc-gpu-p
#SBATCH -q cscc-gpu-qos
#SBATCH --gres=gpu:1                # Number of GPUs (per node)
#SBATCH --time=12:00:00             # Specify the time needed for your experiment

echo "starting Evaluation......................."

python llama8b_rosetta_stone_evaluate.py --run_name="llama8b_rosetta_stone_base_outout0" --prompt_name="base" --batch_size=8

echo " ending " 
