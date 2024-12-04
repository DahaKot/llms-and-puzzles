#!/bin/bash

#SBATCH --job-name=logic_puzzles_mixtral_base_batch16 # Job name
#SBATCH --error=logs/%j%x.err # error file
#SBATCH --output=logs/%j%x.out # output log file
#SBATCH --nodes=1                   # Run all processes on a single node    
#SBATCH --ntasks=1                  # Run on a single CPU
#SBATCH --mem=64G                   # Total RAM to be used
#SBATCH --cpus-per-task=8          # Number of CPU cores
#SBATCH -p cscc-gpu-p
#SBATCH -q cscc-gpu-qos
#SBATCH --gres=gpu:4                # Number of GPUs (per node)
#SBATCH --time=03:00:00             # Specify the time needed for your experiment

echo "starting Evaluation......................."

nvidia-smi

python inference.py --run_name="logic_puzzles_base_mixtral_batch16" \
    --batch_size=16 --dataset="logic_puzzles" --model="mixtral7x8b" \
    --prompt_name="base" --n_gpus=4 --max_tokens=1

echo " ending " 
