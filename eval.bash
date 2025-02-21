#!/bin/bash

#SBATCH --job-name=cryptic_crosswords_mixtral_random_shots # Job name
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

dataset_name="cryptic_crosswords"
batch_size=256
max_tokens=256
model="mixtral"

python inference.py --run_name="logic_puzzles_llama_random_shots4" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens

python inference.py --run_name="logic_puzzles_qwen_random_shots4" \
     --batch_size=$batch_size --dataset=$dataset_name --model="qwen" \
     --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens

python inference.py --run_name="rosetta_stone_llama_random_shots4" \
     --batch_size=8 --dataset="rosetta_stone" --model=$model \
     --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens

python inference.py --run_name="rosetta_stone_qwen_random_shots4" \
     --batch_size=8 --dataset="rosetta_stone" --model="qwen" \
     --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens

python inference.py --run_name="cryptic_crosswords_llama_random_shots4" \
    --batch_size=256 --dataset="cryptic_crosswords" --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=256

python inference.py --run_name="cryptic_crosswords_qwen_random_shots4" \
	--batch_size=256 --dataset="cryptic_crosswords" --model="qwen" \
	--prompt_name="5_shot" --n_gpus=1 --max_tokens=256

echo " ending " 
