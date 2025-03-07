#!/bin/bash

#SBATCH --job-name=rosetta_stone_mixtral_icl_test # Job name
#SBATCH --error=logs/%j%x.err # error file
#SBATCH --output=logs/%j%x.out # output log file
#SBATCH --nodes=1                   # Run all processes on a single node    
#SBATCH --ntasks=1                  # Run on a single CPU
#SBATCH --mem=64G                   # Total RAM to be used
#SBATCH --cpus-per-task=8          # Number of CPU cores
#SBATCH -p cscc-gpu-p
#SBATCH -q cscc-gpu-qos
#SBATCH --gres=gpu:4              # Number of GPUs (per node)
#SBATCH --time=06:00:00             # Specify the time needed for your experiment

echo "starting Evaluation......................."

nvidia-smi

dataset_name="cryptic_crosswords_types"
batch_size=256
max_tokens=512
model="qwen"
similarity="thematic"

python inference.py --run_name="small_cryptic_crosswords_qwen_solutions_thematic_bottom_to_top" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot_solutions" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="semantic_bottom_to_top" --random_seed=32

echo " ending " 
