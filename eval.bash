#!/bin/bash

#SBATCH --job-name=cryptic_crosswords_mixtral # Job name
#SBATCH --error=logs/%j%x.err # error file
#SBATCH --output=logs/%j%x.out # output log file
#SBATCH --nodes=1                   # Run all processes on a single node    
#SBATCH --ntasks=1                  # Run on a single CPU
#SBATCH --mem=64G                   # Total RAM to be used
#SBATCH --cpus-per-task=8          # Number of CPU cores
#SBATCH -p cscc-gpu-p
#SBATCH -q cscc-gpu-qos
#SBATCH --gres=gpu:4               # Number of GPUs (per node)
#SBATCH --time=04:00:00             # Specify the time needed for your experiment

echo "starting Evaluation......................."

nvidia-smi

dataset_name="cryptic_crosswords"
batch_size=256
max_tokens=256
model="mixtral7x8b"

python inference.py --run_name="cryptic_crosswords_mixtral_base" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="base_mixtral_instruct" --n_gpus=4 --max_tokens=$max_tokens

python inference.py --run_name="cryptic_crosswords_mixtral_advanced" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="advanced_mixtral_instruct" --n_gpus=4 --max_tokens=$max_tokens

python inference.py --run_name="cryptic_crosswords_mixtral_zero_shot_chain_of_thought" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="zero_shot_chain_of_thought_mixtral_instruct" --n_gpus=4 --max_tokens=$max_tokens

#echo "logic puzzles advanced qwen"

#python inference.py --run_name="logic_puzzles_qwen_advanced" \
#    --batch_size=$batch_size --dataset=$dataset_name --model="qwen" \
#    --prompt_name="advanced" --n_gpus=1 --max_tokens=$max_tokens

#echo "logic puzzles cot qwen"

#python inference.py --run_name="logic_puzzles_qwen_zero_shot_chain_of_thought" \
#	--batch_size=$batch_size --dataset=$dataset_name --model="qwen" \
#	--prompt_name="zero_shot_chain_of_thought" --n_gpus=1 --max_tokens=$max_tokens

echo " ending " 
