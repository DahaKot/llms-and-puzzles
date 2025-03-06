#!/bin/bash

#SBATCH --job-name=logic_puzzles_qwen_thematic # Job name
#SBATCH --error=logs/%j%x.err # error file
#SBATCH --output=logs/%j%x.out # output log file
#SBATCH --nodes=1                   # Run all processes on a single node    
#SBATCH --ntasks=1                  # Run on a single CPU
#SBATCH --mem=64G                   # Total RAM to be used
#SBATCH --cpus-per-task=8          # Number of CPU cores
#SBATCH -p cscc-gpu-p
#SBATCH -q cscc-gpu-qos
#SBATCH --gres=gpu:1              # Number of GPUs (per node)
#SBATCH --time=06:00:00             # Specify the time needed for your experiment

echo "starting Evaluation......................."

nvidia-smi

dataset_name="logic_puzzles"
batch_size=64
max_tokens=512
model="mixtral"
similarity="random"

python inference.py --run_name="logic_puzzles_mixtral_random1" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot_mixtral_instruct" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=1024

python inference.py --run_name="logic_puzzles_mixtral_random2" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot_mixtral_instruct" --n_gpus=4 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=256

python inference.py --run_name="logic_puzzles_mixtral_random3" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot_mixtral_instruct" --n_gpus=4 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=512

python inference.py --run_name="logic_puzzles_mixtral_random4" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot_mixtral_instruct" --n_gpus=4 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=64

python inference.py --run_name="logic_puzzles_mixtral_random5" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot_mixtral_instruct" --n_gpus=4 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=32

similarity="semantic"
python inference.py --run_name="logic_puzzles_mixtral_semantic_random1" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot_mixtral_instruct" --n_gpus=4 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=1024

python inference.py --run_name="logic_puzzles_mixtral_semantic_random2" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot_mixtral_instruct" --n_gpus=4 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=256

python inference.py --run_name="logic_puzzles_mixtral_semantic_random3" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot_mixtral_instruct" --n_gpus=4 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=512

python inference.py --run_name="logic_puzzles_mixtral_semantic_random4" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot_mixtral_instruct" --n_gpus=4 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=64

python inference.py --run_name="logic_puzzles_mixtral_semantic_random5" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot_mixtral_instruct" --n_gpus=4 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=32

python inference.py --run_name="logic_puzzles_mixtral_semantic_top_to_bottom" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot_mixtral_instruct" --n_gpus=4 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="semantic_top_to_bottom" --random_seed=32

python inference.py --run_name="logic_puzzles_mixtral_semantic_bottom_to_top" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot_mixtral_instruct" --n_gpus=4 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="semantic_bottom_to_top" --random_seed=32









echo " ending " 
