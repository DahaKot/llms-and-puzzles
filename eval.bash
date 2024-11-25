#!/bin/bash

#SBATCH --job-name=cryptic_crosswords_mixtral_instruct_base # Job name
#SBATCH --error=logs/%j%x.err # error file
#SBATCH --output=logs/%j%x.out # output log file
#SBATCH --nodes=1                   # Run all processes on a single node    
#SBATCH --ntasks=1                  # Run on a single CPU
#SBATCH --mem=64G                   # Total RAM to be used
#SBATCH --cpus-per-task=8          # Number of CPU cores
#SBATCH -p cscc-gpu-p
#SBATCH -q cscc-gpu-qos
#SBATCH --gres=gpu:4                # Number of GPUs (per node)
#SBATCH --time=12:00:00             # Specify the time needed for your experiment

echo "starting Evaluation......................."

# python mixtral_cryptic_crosswords_evaluate_vllm.py --run_name="mixtral_cryptic_crosswords_base_mixtral_instruct" --prompt_name="base_mixtral_instruct" --batch_size=8

python inference.py --run_name="llama8b_cryptic_crosswords_base" \
    --batch_size=8 --dataset="cryptic_crosswords" --model="llama8b" \
    --prompt_name="base"

echo " ending " 
