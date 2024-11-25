#!/bin/bash

#SBATCH --job-name=debug # Job name
#SBATCH --error=logs/%j%x.err # error file
#SBATCH --output=logs/%j%x.out # output log file
#SBATCH --nodes=1                   # Run all processes on a single node    
#SBATCH --ntasks=1                  # Run on a single CPU
#SBATCH --mem=40G                   # Total RAM to be used
#SBATCH --cpus-per-task=8          # Number of CPU cores
#SBATCH -p cscc-gpu-p
#SBATCH -q cscc-gpu-qos
#SBATCH --gres=gpu:1                # Number of GPUs (per node)
#SBATCH --time=00:30:00             # Specify the time needed for your experiment

echo "starting Evaluation......................."

nvidia-smi

python llama8b_cryptic_crosswords_evaluate.py --batch_size=8 --run_name="debug"

echo " ending " 
