#!/bin/bash

#SBATCH --job-name=small_cryptic_qwen_all # Job name
#SBATCH --error=logs/%j%x.err # error file
#SBATCH --output=logs/%j%x.out # output log file
#SBATCH --nodes=1                   # Run all processes on a single node    
#SBATCH --ntasks=1                  # Run on a single CPU
#SBATCH --mem=64G                   # Total RAM to be used
#SBATCH --cpus-per-task=8          # Number of CPU cores
#SBATCH -p cscc-gpu-p
#SBATCH -q cscc-gpu-qos
#SBATCH --gres=gpu:1              # Number of GPUs (per node)
#SBATCH --time=05:00:00             # Specify the time needed for your experiment

echo "starting Evaluation......................."

nvidia-smi

dataset_name="cryptic_crosswords_types"
batch_size=64
max_tokens=256
model="qwen"
similarity="semantic"

python inference.py --run_name="small_cryptic_qwen_base" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="base" --n_gpus=1 --max_tokens=$max_tokens \
    # --similarity=$similarity --ranking="random" --random_seed=1024

python inference.py --run_name="small_cryptic_qwen_advanced" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="advanced" --n_gpus=1 --max_tokens=$max_tokens \
    #--similarity=$similarity --ranking="random" --random_seed=512

python inference.py --run_name="small_cryptic_qwen_zero_shot_chain_of_thought" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="zero_shot_chain_of_thought" --n_gpus=1 --max_tokens=$max_tokens \
    #--similarity=$similarity --ranking="random" --random_seed=64


python inference.py --run_name="small_cryptic_qwen_semantic_random1" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=512

python inference.py --run_name="small_cryptic_qwen_semantic_random2" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=1024

python inference.py --run_name="small_cryptic_qwen_semantic_random3" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=64

python inference.py --run_name="small_cryptic_qwen_semantic_top_to_bottom" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="semantic_top_to_bottom" --random_seed=512

python inference.py --run_name="small_cryptic_qwen_semantic_bottom_to_top" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="semantic_bottom_to_top" --random_seed=512


similarity="thematic"
python inference.py --run_name="small_cryptic_qwen_thematic_random1" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=512

python inference.py --run_name="small_cryptic_qwen_thematic_random2" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=1024

python inference.py --run_name="small_cryptic_qwen_thematic_random3" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=64

python inference.py --run_name="small_cryptic_qwen_thematic_top_to_bottom" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="semantic_top_to_bottom" --random_seed=512

python inference.py --run_name="small_cryptic_qwen_thematic_bottom_to_top" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="semantic_bottom_to_top" --random_seed=512


#python inference.py --run_name="rosetta_stone_mixtral_random_shots2" \
#    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
#    --prompt_name="5_shot" --n_gpus=4 --max_tokens=$max_tokens

#python inference.py --run_name="rosetta_stone_mixtral_random_shots3" \
#    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
#    --prompt_name="5_shot" --n_gpus=4 --max_tokens=$max_tokens

#python inference.py --run_name="rosetta_stone_mixtral_random_shots4" \
#    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
#    --prompt_name="5_shot" --n_gpus=4 --max_tokens=$max_tokens

#python inference.py --run_name="rosetta_stone_mixtral_random_shots5" \
#    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
#    --prompt_name="5_shot" --n_gpus=4 --max_tokens=$max_tokens

echo " ending " 
