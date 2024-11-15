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

    model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-8x7B-Instruct-v0.1", device_map="balanced_low_0")
    tokenizer = MistralTokenizer.v1()

    correct_count = 0
    clues, correct_answers, predictions = [], [], []

    for batch in tqdm(dataloader):
        batch_clues = batch["input"]
        batch_correct_answers = batch["target"]
        batch_prompts = batch["prompt"]

        tokens = []
        for prompt in batch_prompts:
            completion_request = ChatCompletionRequest(messages=[UserMessage(content=prompt)])
            tokens.append(tokenizer.encode_chat_completion(completion_request).tokens)
        
        tokens = torch.cat(tokens)

        batch_predictions = model.generate(tokens, max_new_tokens=500, do_sample=False)
        text_predictions = []

        for clue, prediction, correct_answer in zip(batch_clues, batch_predictions, batch_correct_answers):
            model_prediction = tokenizer.decode(prediction[0].tolist()).lower().strip()
            text_predictions.append(model_prediction)

            if correct_answer.lower() in model_prediction:
                correct_count += 1

        clues.extend(batch_clues)
        correct_answers.extend(batch_correct_answers)
        predictions.extend(text_predictions)

    accuracy = correct_count / dataset_length

    log_file = open("./logs/" + args.run_name + ".txt", "w")
    log_file.write(args.prompt_name + " prompt; model: mistralai/Mixtral-8x7B-Instruct-v0.1; accuracy: " + str(accuracy) + "\n")

    for clue, correct_answer, prediction in zip(clues, correct_answers, predictions):
        log_file.write("Clue: " + clue + "\nPrediction: " + prediction + "\nCorrect Answer: " + correct_answer + "\n")

