from tqdm import tqdm
from utils import get_dataset_with_prompts, exact_match

from torch.utils.data import DataLoader
from args_parser import get_args
from vllm import LLM, SamplingParams
import json
from models_list import models_dict

from openai import OpenAI


if __name__ == "__main__":
    args = get_args()

    dataset = get_dataset_with_prompts(args.dataset, args.prompt_name)
    dataset_length = len(dataset)
    dataloader = DataLoader(dataset, batch_size=1)

    client = OpenAI(api_key="sk-d1cbfe42364a4bed9e02903e9c4fd991", base_url="https://api.deepseek.com")

    correct_count = 0
    inputs, correct_answers, predictions = [], [], []

    for sample in tqdm(dataloader):
        inpupt = sample["input"][0]
        correct_answer = sample["target"][0]
        prompt = sample["prompt"][0]

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.0
        )
        prediction = response.choices[0].message.content.lower()

        if exact_match(prediction, correct_answer,
                       multiple_answers=(args.dataset == "rosetta_stone")):
            correct_count += 1

        inputs.append(prompt)
        correct_answers.append(correct_answer)
        predictions.append(prediction)

        if len(inputs) > 100:
            break

    accuracy = correct_count / 100

    log_file = open("./logs/" + args.run_name + ".txt", "w")

    log_file.write(json.dumps(vars(args), indent=4, sort_keys=True))
    log_file.write("\nAccuracy: " + str(accuracy) + "\n")

    for input, correct_answer, prediction in zip(
            inputs, correct_answers, predictions):
        log_file.write(
            "\nInput: " + input + "\nPrediction: " + prediction
            + "\nCorrect Answer: " + correct_answer
            + "\nCounted?" + str(exact_match(prediction, correct_answer, multiple_answers=(args.dataset == "rosetta_stone")))
        )
