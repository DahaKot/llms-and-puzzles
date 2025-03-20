import re

from datasets import load_dataset  # type: ignore
import yaml  # type: ignore

from dataset_preparation import BaseDataset


class CrypticCrosswords(BaseDataset):
    def __init__(
            self, prompt_name, similarity="random", ranking="random",
            n_shots=0, random_seed=42):
        self.dataset = load_dataset("boda/guardian_naive_random", split="test")
        # self.dataset = self.dataset.select(range(100))
        self.embedding_field = "input"

        super().__init__(
            "cryptic_crosswords", prompt_name, similarity, ranking, n_shots,
            random_seed
        )

        with open("cryptic_crosswords_prompts.yaml", "r") as file:
            self.prompts = yaml.safe_load(file)

        self.mapped_dataset = self.dataset.map(
            self.generate_prompt,
            fn_kwargs={"prompt_name": prompt_name},
            load_from_cache_file=False,
            with_indices=True
        )

    def generate_prompt(self, example, index, prompt_name):
        clue = example['input']
        prompt = self.prompts[prompt_name]

        if self.n_shots:
            few_shot_examples = self.similarity(example, index)
            example["prompt"] = prompt.format(clue=clue, **few_shot_examples)
        elif prompt_name == "generate_solution":
            example["prompt"] = prompt.format(
                clue=clue, answer=example["target"]
            )
        else:
            example["prompt"] = prompt.format(clue=clue)

        return example

    def _too_similar(self, example1, example2, examples):
        return example1["target"] in example2["target"] \
               or example2["target"] in example1["target"] \
               or example1 in examples

    def _map_examples_to_dict(self, examples):
        data = {}

        for i, example in enumerate(examples):
            data["clue" + str(i + 1)] = example["input"]
            data["answer" + str(i + 1)] = example["target"]

        return data

    def check_answer_against_correct(self, prediction, correct_answer):
        pattern = rf'\b{re.escape(correct_answer.lower())}\b'
        return bool(re.search(pattern, prediction.lower()))


class CrypticCrosswordsTypes(CrypticCrosswords):
    def __init__(
            self, prompt_name, similarity="random", ranking="random",
            n_shots=0, random_seed=42):
        self.dataset = load_dataset(
            # "csv", data_files="data/cryptic_crosswords/extended_dataset.csv"
            "csv", data_files="data/cryptic_crosswords/"
                              + "cleaned_dataset_with_solutions.csv"
        )["train"]
        self.embedding_field = "input"

        with open("cryptic_crosswords_prompts.yaml", "r") as file:
            self.prompts = yaml.safe_load(file)

        BaseDataset.__init__(
            self, "cryptic_crosswords", prompt_name, similarity, ranking,
            n_shots, random_seed
        )

        self.mapped_dataset = self.dataset.map(
            self.generate_prompt,
            fn_kwargs={"prompt_name": prompt_name},
            load_from_cache_file=False,
            with_indices=True
        )

    def generate_prompt(self, example, index, prompt_name):
        clue = example['input']

        if prompt_name == "deepseek_types":
            example_type = None
            for t in self.type_dict:
                if index in self.type_dict[t]:
                    example_type = t

            if example_type:
                prompt_name = "deepseek_short_" + example_type
                prompt = self.prompts[prompt_name]
                example["prompt"] = prompt.format(clue=clue)
            else:
                raise TypeError(
                    "coudnt find type of this example"
                )

            return example

        prompt = self.prompts[prompt_name]

        if self.n_shots:
            few_shot_examples = self.similarity(example, index)
            example["prompt"] = prompt.format(clue=clue, **few_shot_examples)
        elif prompt_name == "generate_solution":
            example["prompt"] = prompt.format(
                clue=clue, answer=example["target"]
            )
        else:
            example["prompt"] = prompt.format(clue=clue)

        return example

    def _map_examples_to_dict(self, examples):
        data = {}

        for i, example in enumerate(examples):
            data["clue" + str(i + 1)] = example["input"]
            data["answer" + str(i + 1)] = example["target"]
            data["solution" + str(i + 1)] = example["solution"]

        return data
