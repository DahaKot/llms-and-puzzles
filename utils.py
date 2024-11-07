import prompts_list
from datasets import load_dataset


def generate_prompt(example, prompt_name="base"):
    clue = example['input']

    prompt = prompts_list.cryptic_crosswords_prompts[prompt_name]
    example["prompt"] = prompt.format(clue=clue)

    return example

def get_dataset_with_prompts(dataset_path, prompt_name="base"):
    dataset = load_dataset(dataset_path, split="test")

    mapped_dataset = dataset.map(
        generate_prompt, fn_kwargs={"prompt_name": prompt_name},
        load_from_cache_file=True
    )
        
    return mapped_dataset