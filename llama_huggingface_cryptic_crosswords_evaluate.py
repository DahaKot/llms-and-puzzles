from typing import Dict
import prompts_list
import torch
from transformers import pipeline
from tqdm import tqdm
from utils import get_dataset_with_prompts

from torch.utils.data import DataLoader
from args_parser import get_args
from vllm import LLM, SamplingParams

from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest

from transformers import AutoModelForCausalLM, AutoTokenizer

if __name__ == "__main__":
    args = get_args()

    prompt = prompts_list.cryptic_crosswords_prompts[args.prompt_name]

    dataset = get_dataset_with_prompts("boda/guardian_naive_random", args.prompt_name)
    dataset_length = len(dataset)
    dataloader = DataLoader(dataset, batch_size=args.batch_size)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Device: ", device)

    model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B-Instruct", torch_dtype=torch.float16, device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct", padding_side="left")
    tokenizer.pad_token = tokenizer.eos_token
    model.generation_config.pad_token_id = tokenizer.eos_token_id

    print("model device: ", model.device)

    correct_count = 0
    clues, correct_answers, predictions = [], [], []

    for batch in tqdm(dataloader):
        batch_clues = batch["input"]
        batch_correct_answers = batch["target"]
        batch_prompts = batch["prompt"]

        encoded_inputs = tokenizer(batch_prompts, padding=True, truncation=True, return_tensors="pt")
        input_ids = encoded_inputs["input_ids"].to(device)
        attention_mask = encoded_inputs["attention_mask"].to(device)
        
        print("before generation")

        batch_predictions = model.generate(
            input_ids=input_ids, attention_mask=attention_mask, max_new_tokens=512,
            do_sample=False, top_p=1.0
        )
        text_predictions = []

        # prediction = tokenizer.batch_decode(batch_predictions, skip_special_tokens=True)

        # for clue, prediction, correct_answer in zip(batch_clues, batch_predictions, batch_correct_answers):
        #    model_prediction = tokenizer.decode(prediction[0].tolist(), skip_special_tokens=True).lower().strip()
        #    text_predictions.append(model_prediction)

        #    if correct_answer.lower() in model_prediction:
        #        correct_count += 1

        clues.extend(batch_clues)
        correct_answers.extend(batch_correct_answers)
        predictions.append(batch_predictions)

    accuracy = correct_count / dataset_length

    log_file = open("./logs/" + args.run_name + ".txt", "w")
    log_file.write(args.prompt_name + " prompt; model: mistralai/Mixtral-8x7B-Instruct-v0.1; accuracy: " + str(accuracy) + "\n")

    for clue, correct_answer, prediction in zip(clues, correct_answers, predictions):
        log_file.write("Clue: " + clue + "\nPrediction: " + prediction + "\nCorrect Answer: " + correct_answer + "\n")

