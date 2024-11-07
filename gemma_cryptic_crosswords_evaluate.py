from typing import List, Dict
import prompts_list
import json
import torch
from transformers import pipeline
from tqdm import tqdm

prompts = prompts_list.cryptic_crosswords_prompts

with open("./naive_random.json", "r") as file:
    dataset = json.load(file)["test"]

pipe = pipeline(
    "text-generation",
    model="google/gemma-2-9b-it",
    model_kwargs={"torch_dtype": torch.bfloat16},
    device="cuda",
)

# Function to evaluate a model with a specific prompt
def evaluate_model_on_prompt(prompt: str, log_file) -> float:
    correct_count = 0
    for item in tqdm(dataset):
        clue = item["clue"]
        correct_answer = item["soln_with_spaces"]
        # Generate the full prompt with the clue
        full_prompt = prompt.format(clue=clue)
        messages = [
            {"role": "user", "content": full_prompt},
	]

        outputs = pipe(messages, max_new_tokens=64)
        model_answer = outputs[0]["generated_text"][-1]["content"].strip()

        log_file.write("Clue: " + clue + "\nAnswer: " + model_answer + "\nCorrect Answer: " + correct_answer + "\n")

        # Check if the model's answer matches the correct answer
        if correct_answer.lower() in model_answer.lower():
            correct_count += 1

    # Calculate accuracy for this prompt and model
    accuracy = correct_count / len(dataset)
    return accuracy

# Run evaluation
results: Dict[str, float] = {}
for prompt_name, prompt in prompts.items():
    log_file = open("./logs/gemma" + "_" + prompt_name + ".txt", "w")

    accuracy = evaluate_model_on_prompt(prompt, log_file)
    results[prompt_name] = accuracy
    print(f"Gemma, {prompt_name} prompt, Accuracy: {accuracy:.2%}")

# Display final results
print("\nOverall Results:")
for prompt_name, accuracy in results.items():
    print(f"Gemma with {prompt_name}: {accuracy:.2%}")
