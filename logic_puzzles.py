import re

import pandas as pd
from datasets import load_dataset  # type: ignore
import yaml  # type: ignore

from dataset_preparation import BaseDataset


class LogicPuzzles(BaseDataset):
    def __init__(
            self, prompt_name, similarity="random", ranking="random",
            n_shots=0, random_seed=42):
        with open("logic_puzzles_prompts.yaml", "r") as file:
            self.prompts = yaml.safe_load(file)

        self.dataset = load_dataset(
            'json', split="train",
            data_files='./data/puzzle_ben/PuzzleBen_testset_updated.json'
        )
        self.dataset = self.dataset.rename_column(
            "task", "type"
        )
        self.embedding_field = "problem"

        solutions_dataset = pd.read_csv(
            "./data/puzzle_ben/dataset_with_solutions.csv"
        )
        solutions_column = solutions_dataset["solution"].to_list()
        self.dataset = self.dataset.add_column("solution", solutions_column)

        super().__init__(
            "logic_puzzles", prompt_name, similarity, ranking, n_shots,
            random_seed
        )

        self.mapped_dataset = self.dataset.map(
            self.generate_prompt,
            fn_kwargs={
                "prompt_name": prompt_name
            },
            load_from_cache_file=False,
            with_indices=True
        )

        self.mapped_dataset = self.mapped_dataset.rename_column(
            "problem", "input"
        )
        self.mapped_dataset = self.mapped_dataset.remove_columns(["options"])

    def _generate_options_string(self, example):
        number_options = [
            "Option1", "Option2", "Option3", "Option4", "Option5"
        ]
        letter_options = ["A", "B", "C", "D", "E"]

        options = []
        for i, option in enumerate(example["options"]):
            option = option.replace(number_options[i], letter_options[i])
            options.append(option)
        options = "\n".join(options)

        return options

    def generate_prompt(self, example, index, prompt_name):
        problem = example["problem"]

        example["possible_answers_string"] = self._generate_options_string(
            example
        )

        letter_options = ["A", "B", "C", "D", "E"]
        example["target"] = letter_options[example["answer"] - 1]

        if "types" in prompt_name:
            example_type = example["type"]
            # for t in self.type_dict:
            #     if index in self.type_dict[t]:
            #         example_type = t

            if example_type:
                if "short" in prompt_name:
                    prompt_name = "deepseek_short_" + example_type
                else:
                    prompt_name = "deepseek_" + example_type

                if "mixtral_instruct" in prompt_name:
                    prompt_name += "_mixtral_instruct"

                prompt = self.prompts[prompt_name]
                example["prompt"] = prompt.format(
                    problem=problem, options=example["possible_answers_string"]
                )
            else:
                raise TypeError(
                    "coudnt find type of this example"
                )

            return example

        prompt = self.prompts[prompt_name]

        if self.n_shots:
            few_shot_examples = self.similarity(example, index)
            example["prompt"] = prompt.format(
                problem=problem,
                options=example["possible_answers_string"], **few_shot_examples
            )
        elif prompt_name == "generate_solution":
            example["prompt"] = prompt.format(
                problem=problem, options=example["possible_answers_string"],
                answer=example["target"]
            )
        else:
            example["prompt"] = prompt.format(
                problem=problem, options=example["possible_answers_string"]
            )

        return example

    def _too_similar(self, example1, example2, examples):
        return example1["problem"] == example2["problem"] \
                # or example1 in examples

    def _map_examples_to_dict(self, examples):
        letter_options = ["A", "B", "C", "D", "E"]
        data = {}

        for i, sample in enumerate(examples):
            data["problem" + str(i + 1)] = sample["problem"]
            data["answer" + str(i + 1)] = letter_options[sample["answer"] - 1]
            data["options" + str(i + 1)] = self._generate_options_string(
                sample
            )
            data["solution" + str(i + 1)] = sample["solution"]

        return data

    def check_answer_against_correct(self, prediction, correct_answer):
        prediction = prediction.replace("[", "").lower()

        match = re.search(r"answer:\s*(\S)", prediction)
        if not match:
            return False
        answer = match.group(1)
        return answer.lower() == correct_answer.lower()
