#!/bin/bash

#SBATCH --job-name=logic_puzzles_llama_base # Job name
#SBATCH --error=logs/%j%x.err # error file
#SBATCH --output=logs/%j%x.out # output log file
#SBATCH --nodes=1                   # Run all processes on a single node    
#SBATCH --ntasks=1                  # Run on a single CPU
#SBATCH --mem=64G                   # Total RAM to be used
#SBATCH --cpus-per-task=8          # Number of CPU cores
#SBATCH -p cscc-gpu-p
#SBATCH -q cscc-gpu-qos
#SBATCH --gres=gpu:1                # Number of GPUs (per node)
#SBATCH --time=02:00:00             # Specify the time needed for your experiment

echo "starting Evaluation......................."

nvidia-smi

dataset_name="logic_puzzles"
batch_size=64
max_tokens=256

echo "logic puzzles advanced llama8b"

python inference.py --run_name="logic_puzzles_llama_advanced" \
    --batch_size=$batch_size --dataset=$dataset_name --model="llama8b" \
    --prompt_name="advanced" --n_gpus=1 --max_tokens=$max_tokens

echo "logic puzzles cot llama"

python inference.py --run_name="logic_puzzles_llama_zero_shot_chain_of_thought" \
    --batch_size=$batch_size --dataset=$dataset_name --model="llama8b" \
    --prompt_name="zero_shot_chain_of_thought" --n_gpus=1 --max_tokens=$max_tokens

echo "logic puzzles base qwen"

python inference.py --run_name="logic_puzzles_qwen_base" \
    --batch_size=$batch_size --dataset=$dataset_name --model="qwen" \
    --prompt_name="base" --n_gpus=1 --max_tokens=$max_tokens

echo "logic puzzles advanced qwen"

python inference.py --run_name="logic_puzzles_qwen_advanced" \
    --batch_size=$batch_size --dataset=$dataset_name --model="qwen" \
    --prompt_name="advanced" --n_gpus=1 --max_tokens=$max_tokens

echo "logic puzzles cot qwen"

python inference.py --run_name="logic_puzzles_qwen_zero_shot_chain_of_thought" \
	--batch_size=$batch_size --dataset=$dataset_name --model="qwen" \
	--prompt_name="zero_shot_chain_of_thought" --n_gpus=1 --max_tokens=$max_tokens

echo " ending " 
