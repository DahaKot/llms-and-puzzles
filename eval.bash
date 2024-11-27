#!/bin/bash

#SBATCH --job-name=rosetta_stone_llama8b_base_batch256 # Job name
#SBATCH --error=logs/%j%x.err # error file
#SBATCH --output=logs/%j%x.out # output log file
#SBATCH --nodes=1                   # Run all processes on a single node    
#SBATCH --ntasks=1                  # Run on a single CPU
#SBATCH --mem=64G                   # Total RAM to be used
#SBATCH --cpus-per-task=8          # Number of CPU cores
#SBATCH -p cscc-gpu-p
#SBATCH -q cscc-gpu-qos
#SBATCH --gres=gpu:1                # Number of GPUs (per node)
#SBATCH --time=00:30:00             # Specify the time needed for your experiment

echo "starting Evaluation......................."

nvidia-smi

python inference.py --run_name="rosetta_stone_base_llama8b_batch32" \
    --batch_size=32 --dataset="rosetta_stone" --model="llama8b" \
    --prompt_name="base" --n_gpus=1

echo " ending " 
