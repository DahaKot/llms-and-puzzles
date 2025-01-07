#!/bin/bash

#SBATCH --job-name=logic_puzzles_llama_advanced # Job name
#SBATCH --error=logs/%j%x.err # error file
#SBATCH --output=logs/%j%x.out # output log file
#SBATCH --nodes=1                   # Run all processes on a single node    
#SBATCH --ntasks=1                  # Run on a single CPU
#SBATCH --mem=64G                   # Total RAM to be used
#SBATCH --cpus-per-task=8          # Number of CPU cores
#SBATCH -p cscc-gpu-p
#SBATCH -q cscc-gpu-qos
#SBATCH --gres=gpu:1                # Number of GPUs (per node)
#SBATCH --time=03:00:00             # Specify the time needed for your experiment

echo "starting Evaluation......................."

nvidia-smi

dataset_name="logic_puzzles"
batch_size=256
max_tokens=256

echo "llama base"

python inference.py --run_name="updated_prompt_logic_puzzles_llama_base" \
    --batch_size=$batch_size --dataset=$dataset_name --model="llama8b" \
    --prompt_name="base" --n_gpus=1 --max_tokens=$max_tokens --log_probs=512

echo "llama advanced"

#python inference.py --run_name="updated_prompt_rosetta_stone_llama_advanced_max_tokens_512_inter_prompt" \
#    --batch_size=$batch_size --dataset=$dataset_name --model="llama8b" \
#    --prompt_name="advanced" --n_gpus=1 --max_tokens=$max_tokens

echo "qwen base"

#python inference.py --run_name="updated_prompt_rosetta_stone_qwen_base_max_tokens_512_inter_prompt" \
#    --batch_size=$batch_size --dataset=$dataset_name --model="qwen" \
#    --prompt_name="base" --n_gpus=1 --max_tokens=$max_tokens

echo "qwen advanced"

#python inference.py --run_name="updated_prompt_rosetta_stone_qwen_advanced_max_tokens_512_inter_prompt" \
#    --batch_size=$batch_size --dataset=$dataset_name --model="qwen" \
#    --prompt_name="advanced" --n_gpus=1 --max_tokens=$max_tokens

echo " ending " 
