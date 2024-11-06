import replicate
from typing import List, Dict
import prompts_list
import json

# Define models and prompts
models = {
    "gemma2-9b": "google-deepmind/gemma2-9b-it:24464993111a1b52b2ebcb2a88c76090a705950644dca3a3955ee40d80909f2d",
    "llama3.1-405b": "meta/meta-llama-3.1-405b-instruct",
    "mixtral-8x7b": "nateraw/mixtral-8x7b-32kseqlen:defd13a450b135eab8f24e23f9659c71eed07b8de1b0dde9503a6e8a961d5510"
}
files = ["gemma", "llama", "mixtral"]
prompts = prompts_list.cryptic_crosswords_prompts

# Load your dataset of cryptic crossword clues and answers
# Example format: dataset = [{"clue": "Sample clue", "answer": "Correct answer"}, ...]
with open("./naive_random.json", "r") as file:
    dataset = json.load(file)["test"][:5]


# Function to evaluate a model with a specific prompt
def evaluate_model_on_prompt(model_id: str, prompt: str, log_file) -> float:
    correct_count = 0
    for item in dataset:
        clue = item["clue"]
        correct_answer = item["soln_with_spaces"]
        # Generate the full prompt with the clue
        full_prompt = prompt.format(clue=clue)

        # Get the model prediction
        output = replicate.run(model_id, input={"prompt": full_prompt, "temperature": 0.1, "max_new_tokens": 50})
        
        model_answer = ""
        for item in output:
            model_answer += item

        log_file.write("Clue: " + clue + "\nAnswer: " + model_answer + "\n")

        # Check if the model's answer matches the correct answer
        if correct_answer.lower() in model_answer.lower():
            correct_count += 1

    # Calculate accuracy for this prompt and model
    accuracy = correct_count / len(dataset)
    return accuracy

# Run evaluation
results: Dict[str, Dict[str, float]] = {}
for model_name, model_id in models.items():
    results[model_name] = {}
    for prompt_name, prompt in prompts.items():
        log_file = open("./logs/" + model_name + "_" + prompt_name + ".txt", "w")

        accuracy = evaluate_model_on_prompt(model_id, prompt, log_file)
        results[model_name][prompt_name] = accuracy
        print(f"Model: {model_name}, {prompt_name} prompt, Accuracy: {accuracy:.2%}")

# Display final results
print("\nOverall Results:")
for model_name, prompt_results in results.items():
    for prompt_name, accuracy in prompt_results.items():
        print(f"{model_name} with {prompt_name}: {accuracy:.2%}")
