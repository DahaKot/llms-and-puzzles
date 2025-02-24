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

dataset_name="cryptic_crosswords_types"
batch_size=256
max_tokens=256
model="llama"
similarity="semantic"

python inference.py --run_name="small_cryptic_crosswords_llama_base" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="base" --n_gpus=1 --max_tokens=$max_tokens \
    #--similarity=$similarity --ranking="random" --random_seed=16

python inference.py --run_name="small_cryptic_crossword_llama_advanced" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="advanced" --n_gpus=1 --max_tokens=$max_tokens \
    #--similarity=$similarity --ranking="random" --random_seed=20

python inference.py --run_name="small_cryptic_crosswords_llama_zero_shot_chain_of_thought" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="zero_shot_chain_of_thought" --n_gpus=1 --max_tokens=$max_tokens \
    #--similarity=$similarity --ranking="random" --random_seed=2048


python inference.py --run_name="small_cryptic_crosswords_llama_semantic_bottom_to_top" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="semantic_bottom_to_top" --random_seed=2048

python inference.py --run_name="small_cryptic_crosswords_llama_semantic_top_to_bottom" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="semantic_top_to_bottom" --random_seed=2048

python inference.py --run_name="small_cryptic_crosswords_llama_semantic_random1" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=2048

python inference.py --run_name="small_cryptic_crosswords_llama_semantic_random2" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=512

python inference.py --run_name="small_cryptic_crosswords_llama_semantic_random3" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity=$similarity --ranking="random" --random_seed=256


python inference.py --run_name="small_cryptic_crosswords_llama_random1" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity="random" --ranking="random" --random_seed=2048

python inference.py --run_name="small_cryptic_crosswords_llama_random2" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity="random" --ranking="random" --random_seed=128

python inference.py --run_name="small_cryptic_crosswords_llama_random3" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity="random" --ranking="random" --random_seed=20

python inference.py --run_name="small_cryptic_crosswords_llama_random4" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity="random" --ranking="random" --random_seed=8

python inference.py --run_name="small_cryptic_crosswords_llama_random5" \
    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
    --similarity="random" --ranking="random" --random_seed=256

runpodctl stop pod 6xi4x8gjj5cbww
#dataset_name="rosetta_stone_types"
#batch_size=8
#max_tokens=512

#python inference.py --run_name="rosetta_stone_llama_thematic_random1" \
#    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
 #   --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
#    --similarity=$similarity --ranking="random" --random_seed=1024

#python inference.py --run_name="rosetta_stone_llama_thematic_random2" \
#    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
#    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
#    --similarity=$similarity --ranking="random" --random_seed=512

#python inference.py --run_name="rosetta_stone_llama_thematic_random3" \
#    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
#    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
#    --similarity=$similarity --ranking="random" --random_seed=2048

#python inference.py --run_name="logic_puzzles_llama_semantic_random2" \
#    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
#    --prompt_name="5_shot" --n_gpus=1 --max_tokens=$max_tokens \
#    --similarity="random" --ranking="random" --random_seed=256

#python inference.py --run_name="logic_puzzles_llama_semantic_random3" \
#    --batch_size=8 --dataset="rosetta_stone" --model=$model \
#    --prompt_name="5_shot" --n_gpus=1 --max_tokens=512 \
#    --similarity="random" --ranking="random" --random_seed=1024

#python inference.py --run_name="rosetta_stone_llama_random_shots3" \
#    --batch_size=8 --dataset="rosetta_stone" --model=$model \
#    --prompt_name="5_shot" --n_gpus=1 --max_tokens=512 \
#    --similarity="random" --ranking="random" --random_seed=256

#python inference.py --run_name="cryptic_crosswords_mixtral_random_shots5" \
#    --batch_size=$batch_size --dataset=$dataset_name --model=$model \
#    --prompt_name="5_shot" --n_gpus=4 --max_tokens=$max_tokens \
#    --similarity="random" --ranking="random" --random_seed=5


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
