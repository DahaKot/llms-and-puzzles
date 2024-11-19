from typing import Dict
import prompts_list
import torch
import json
from transformers import pipeline
from tqdm import tqdm
from utils import get_dataset_with_prompts, get_rosetta_stone_dataset_with_prompts

from torch.utils.data import DataLoader
from args_parser import get_args
from vllm import LLM, SamplingParams

from rosetta_stone_prompting import PromptBuilder

if __name__ == "__main__":
    args = get_args()

    dataset = get_rosetta_stone_dataset_with_prompts("./data/rosetta_stone/ModeLing_v2.json", args.prompt_name)
    dataset_length = len(dataset)
    dataloader = DataLoader(dataset, batch_size=args.batch_size)

    model = LLM(
        model="meta-llama/Llama-3.1-8B-Instruct",
        # max_model_len=256,
        dtype="float16",
        # tensor_parallel_size=2
    )
    tokenizer = model.get_tokenizer()

    sampling_params = SamplingParams(
        temperature=0.0, max_tokens=512,
        stop_token_ids=[tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids("<|eot_id|>")]
    )

    correct_count = 0
    clues, correct_answers, predictions = [], [], []

    for batch in tqdm(dataloader):
        batch_clues = batch["input"]
        batch_correct_answers = batch["target"]
        batch_prompts = batch["prompt"]

        batch_predictions = model.generate(batch_prompts, sampling_params, use_tqdm=False)
        text_predictions = []

        for clue, prediction, correct_answer in zip(batch_clues, batch_predictions, batch_correct_answers):
            # print("outputs: ", prediction.outputs)
            # model_prediction = "\n".join([line.text.lower().strip() for line in prediction.outputs])
            model_prediction = prediction.outputs[0].text.lower().strip()
            text_predictions.append(model_prediction)

            if correct_answer.lower() in model_prediction:
                correct_count += 1

        clues.extend(batch_clues)
        correct_answers.extend(batch_correct_answers)
        predictions.extend(text_predictions)

    accuracy = correct_count / dataset_length

    log_file = open("./logs/" + args.run_name + ".txt", "w")
    log_file.write(args.prompt_name + " prompt; model: meta-llama/Llama-3.1-8B-Instruct; accuracy: " + str(accuracy) + "\n")

    for clue, correct_answer, prediction in zip(clues, correct_answers, predictions):
        log_file.write("Clue: " + clue + "\nPrediction: " + prediction + "\nCorrect Answer: " + correct_answer + "\n")

