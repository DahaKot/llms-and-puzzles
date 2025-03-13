import prompts_list
from datasets import load_dataset, Dataset  # type: ignore
import json
import random
from utils import replace_spans
import re
from sentence_transformers import SentenceTransformer
from torch.nn.functional import cosine_similarity  # type: ignore
import torch
import csv
import pandas as pd


class BaseDataset():
    def __init__(self, dataset_name, prompt_name, similarity="random",
                 ranking="random", n_shots=0, random_seed=42):
        # options for the dataset_name are:
        # cryptic_crosswords, rosetta_stone, logic_puzzles
        self.dataset_name = dataset_name
        self.prompt_name = prompt_name

        self.similarity_functions = {
            "random": self.random_similarity,
            "semantic": self.semantic_similarity,
            "thematic": self.thematic_similarity
        }
        self.similarity = self.similarity_functions[similarity]

        self.ranking_functions = {
            "random": self.random_ranking,
            "semantic_top_to_bottom": self.semantic_ranking_top_to_bottom,
            "semantic_bottom_to_top": self.semantic_ranking_bottom_to_top,
        }
        self.ranking = self.ranking_functions[ranking]

        self.embeddings = None
        if similarity in ["semantic", "thematic"]:
            self.embeddings = self._get_embeddings()

        if self.similarity.__name__.startswith("thematic"):
            self.type_dict = {}
            for i, example in enumerate(self.dataset):
                type = example["type"]
                if type in self.type_dict:
                    self.type_dict[type].append(i)
                else:
                    self.type_dict[type] = [i]

        self.n_shots = n_shots
        random.seed(random_seed)

    def check_answer_against_correct(self, prediction, correct_answer):
        pass

    def _too_similar(self, example1, example2):
        pass

    def _get_embeddings(self):
        model = SentenceTransformer("all-MiniLM-L6-v2")

        clues = [example[self.embedding_field] for example in self.dataset]

        embeddings = model.encode(clues, convert_to_tensor=True)
        return embeddings

    def random_similarity(self, example, index=None):
        examples = []
        while len(examples) < self.n_shots:
            index = random.sample(range(len(self.dataset)), 1)[0]

            if not self._too_similar(self.dataset[index], example, examples):
                examples.append(self.dataset[index])

        return self._map_examples_to_dict(examples)

    def semantic_similarity(self, example, index):
        similarities = cosine_similarity(
            self.embeddings[index].reshape(1, -1), self.embeddings
        )

        indices = torch.argsort(similarities, descending=True)

        examples = []
        i = 0
        while len(examples) < self.n_shots:
            index = int(indices[i])
            if not self._too_similar(self.dataset[index], example, examples):
                examples.append(self.dataset[index])
            i += 1

        examples = self.ranking(examples)

        return self._map_examples_to_dict(examples)

    def thematic_similarity(self, example, index):
        similarities = cosine_similarity(
            self.embeddings[index].reshape(1, -1), self.embeddings
        )

        indices = torch.argsort(similarities, descending=True)

        # # filter indices by type
        device = indices.device
        valid_indices = torch.tensor(
            list(self.type_dict[example["type"]]), device=device
        )
        mask = torch.isin(indices, valid_indices)
        indices = indices[mask]

        # now we have examples of the same type sorted by semantic similarity
        # if we don't shuffle, examples list will be filled with most similar
        if self.ranking.__name__.startswith("random"):
            indices = self.ranking(indices)

        examples = []
        i = 0
        while len(examples) < self.n_shots and i < len(indices):
            index = int(indices[i])
            if not self._too_similar(self.dataset[index], example, examples):
                examples.append(self.dataset[index])
            i += 1

        examples = self.ranking(examples)

        return self._map_examples_to_dict(examples)

    def random_ranking(self, example_list):
        n = len(example_list)
        indexes = list(range(n))
        random.shuffle(indexes)

        permuted_list = [example_list[i] for i in indexes]
        return permuted_list

    def semantic_ranking_top_to_bottom(self, example_list):
        return example_list

    def semantic_ranking_bottom_to_top(self, example_list):
        return example_list[::-1]

    def generate_prompt(self, example, prompt_name, similarity):
        pass


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

        self.mapped_dataset = self.dataset.map(
            self.generate_prompt,
            fn_kwargs={"prompt_name": prompt_name},
            load_from_cache_file=False,
            with_indices=True
        )

    def generate_prompt(self, example, index, prompt_name):
        clue = example['input']
        prompt = prompts_list.cryptic_crosswords_prompts[prompt_name]

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

    def _map_examples_to_dict(self, examples):
        data = {}

        for i, example in enumerate(examples):
            data["clue" + str(i + 1)] = example["input"]
            data["answer" + str(i + 1)] = example["target"]
            data["solution" + str(i + 1)] = example["solution"]

        return data


class RosettaStone(BaseDataset):
    def __init__(
            self, prompt_name, similarity="random", ranking="random",
            n_shots=0, random_seed=42):
        self.embedding_field = "data"

        self.modeling_raw = json.load(open(
            "./data/rosetta_stone/ModeLing_v2.json", "r", encoding="utf8"
        ))
        self.lingoly_raw = json.load(open(
            "./data/rosetta_stone/LingOly_v9.json", "r", encoding="utf8"
        ))

        self.prompt_name = prompt_name

        modeling_data = self._load_modeling_data()
        lingoly_data = self._load_lingoly_data()
        combined_samples = modeling_data + lingoly_data

        self.dataset = Dataset.from_list(combined_samples)

        super().__init__(
            "rosetta_stone", prompt_name, similarity, ranking, n_shots,
            random_seed
        )

        self.mapped_dataset = self.dataset.map(
            self.generate_prompt,
            fn_kwargs={"prompt_name": self.prompt_name},
            load_from_cache_file=False,
            with_indices=True
        )

    def _load_modeling_data(self):
        dataset = json.load(open(
            "./data/rosetta_stone/ModeLing_v2.json", "r", encoding="utf8"
        ))

        prompt_builder = PromptBuilder(self.prompt_name)
        samples = []

        with open(
                './data/rosetta_stone/cleaned_dataset_with_solutions.csv',
                mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            solutions_data = list(reader)

        solutions_index = 1
        for d in dataset:
            data = d["cleaned_data"]["data"]
            qna = d["cleaned_data"]["qna"]
            language = d["name"].split()[0]
            for row in qna:
                train_data, question = prompt_builder.get_data_and_question(
                    data, qna_row=row
                )

                samples.append({
                    "data": train_data,
                    "question": question,
                    "target": json.dumps([row[2][1]]),
                    "input": train_data + "\n\n" + question,
                    "dataset": "ModeLing",
                    "language": language,
                    "type": d["type"][0],
                    "question_number": len(samples),
                    "solution": solutions_data[solutions_index][3]
                })
                solutions_index += 1

        return samples

    def _load_lingoly_data(self):
        dataset = json.load(open(
            "./data/rosetta_stone/LingOly_v9.json", "r", encoding="utf8"
        ))

        prompt_builder = PromptBuilder(self.prompt_name)
        samples = []

        for d in dataset:
            data = d["data"]
            qna = d["qna"]
            language = d["language"]
            for row in qna:
                train_data, question = prompt_builder.get_data_and_question(
                    data, qna_row=row
                )

                target = row[2][1]
                if not isinstance(target, list):
                    target_list = json.dumps([target])
                else:
                    if isinstance(target[0], list):
                        # Flatten nested lists and remove duplicates
                        one_list_target = []
                        for sublist in target:
                            one_list_target.extend(sublist)
                        target = list(set(one_list_target))
                    target_list = json.dumps(target)

                samples.append({
                    "data": train_data,
                    "question": question,
                    "target": target_list,
                    "input": train_data + "\n\n" + question,
                    "dataset": "LingOly",
                    "language": language,
                    "type": "NONE",
                    "question_number": len(samples),
                    "solution": "",
                })

        return samples

    def generate_prompt(self, example, index, prompt_name):
        data = example['data']
        question = example['question']
        prompt = prompts_list.rosetta_stone_prompts[prompt_name]

        if self.n_shots:
            few_shot_examples = self.similarity(example, index)
            example["prompt"] = prompt.format(
                data=data, question=question, **few_shot_examples
            )
        elif prompt_name == "generate_solution":
            example["prompt"] = prompt.format(
                data=data, question=question,
                answer=json.loads(example["target"])[0]
            )
        else:
            example["prompt"] = prompt.format(data=data, question=question)

        return example

    def _too_similar(self, example1, example2, examples):
        return example1["language"] == example2["language"] \
            or example1["language"] in [ex["language"] for ex in examples]

    def _map_examples_to_dict(self, examples):
        data = {}
        for i, sample in enumerate(examples):
            data["data" + str(i + 1)] = sample["data"]
            data["question" + str(i + 1)] = sample["question"]
            one_correct_answer = json.loads(sample["target"])[0]
            data["answer" + str(i + 1)] = one_correct_answer

        return data

    def check_answer_against_correct(self, prediction, correct_answer):
        correct_answers = json.loads(correct_answer)
        return any([a.lower() in prediction.lower() for a in correct_answers])


class RosettaStoneTypes(RosettaStone):
    def __init__(
            self, prompt_name, similarity="random", ranking="random",
            n_shots=0, random_seed=42):
        self.embedding_field = "data"

        self.modeling_raw = json.load(open(
            "./data/rosetta_stone/ModeLing_v2.json", "r", encoding="utf8"
        ))

        self.prompt_name = prompt_name

        modeling_data = self._load_modeling_data()
        self.dataset = Dataset.from_list(modeling_data)

        BaseDataset.__init__(
            self, "rosetta_stone", prompt_name, similarity, ranking, n_shots,
            random_seed
        )

        self.mapped_dataset = self.dataset.map(
            self.generate_prompt,
            fn_kwargs={"prompt_name": self.prompt_name},
            load_from_cache_file=False,
            with_indices=True
        )

    def _too_similar(self, example1, example2, examples):
        # we lift the restriction of not repeating the language in all examples
        # because there is not enough data
        return example1["language"] == example2["language"]

    def _map_examples_to_dict(self, examples):
        data = {}
        for i, sample in enumerate(examples):
            data["data" + str(i + 1)] = sample["data"]
            data["question" + str(i + 1)] = sample["question"]
            one_correct_answer = json.loads(sample["target"])[0]
            data["answer" + str(i + 1)] = one_correct_answer
            data["solution" + str(i + 1)] = sample["solution"]

        return data


class LogicPuzzles(BaseDataset):
    def __init__(
            self, prompt_name, similarity="random", ranking="random",
            n_shots=0, random_seed=42):
        self.dataset = load_dataset(
            'json', split="train",
            data_files='./data/puzzle_ben/PuzzleBen_testset_updated.json'
        )
        self.dataset = self.dataset.rename_column(
            "task", "type"
        )
        self.embedding_field = "problem"

        solutions_dataset = pd.read_csv("./data/puzzle_ben/dataset_with_solutions.csv")
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
        prompt = prompts_list.logic_puzzles_prompts[prompt_name]

        example["possible_answers_string"] = self._generate_options_string(
            example
        )

        letter_options = ["A", "B", "C", "D", "E"]
        example["target"] = letter_options[example["answer"] - 1]

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

        return data

    def check_answer_against_correct(self, prediction, correct_answer):
        prediction = prediction.replace("[", "").lower()

        match = re.search(r"answer:\s*(\S)", prediction)
        if not match:
            return False
        answer = match.group(1)
        return answer.lower() == correct_answer.lower()


def get_dataset_with_prompts(dataset_name, prompt_name="base",
                             similarity="random", ranking="random", n_shots=0,
                             random_seed=42):
    datasets = {
        "cryptic_crosswords": CrypticCrosswords,
        "cryptic_crosswords_types": CrypticCrosswordsTypes,
        "rosetta_stone": RosettaStone,
        "rosetta_stone_types": RosettaStoneTypes, "logic_puzzles": LogicPuzzles
    }

    wrapped_dataset = datasets[dataset_name](
        prompt_name, similarity, ranking, n_shots, random_seed
    )

    return wrapped_dataset


# the code is taken from KV Aditya Srivatsa and Mukund Choudhary
class PromptBuilder:
    def __init__(self, prompt_name):
        self.task_prompt_template = \
            prompts_list.rosetta_stone_prompts[prompt_name]

        self.data_text_template = \
            "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"<<TRG_TEXT>>\"\n"
        self.question_text_template = \
            "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"\""

        self.single_data_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n"
        self.single_question_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\""

    def get_data_and_question(self, data, qna_row):
        # new code from me
        data_text = self.build_data_text(data)
        question_text = self.build_question_text(qna_row)

        return data_text, question_text

    def build_prompt_message(self, data, qna_row, qna_whole, **kwargs):
        task_prompt = self.build_task_prompt(
            data, qna_row, qna_whole, **kwargs
        )
        return task_prompt

    def build_task_prompt(self, data, qna_row, qna_whole=None, language=None):
        data_text = self.build_data_text(data)
        question_text = self.build_question_text(qna_row)

        span_dict = {
            "<<DATA>>": data_text,
            "<<QUESTION>>": question_text
        }
        task_prompt = replace_spans(self.task_prompt_template, span_dict)
        return task_prompt

    def build_data_text(self, data):
        data_text = ""
        for row in data:
            source_lang, source_text = row[1][0], row[1][1]
            target_lang, target_text = row[2][0], row[2][1]
            span_dict = {
                "<<SRC_LANG>>": source_lang,
                "<<SRC_TEXT>>": source_text,
                "<<TRG_LANG>>": target_lang,
                "<<TRG_TEXT>>": target_text,
            }

            if target_lang == "<<BLANK>>" or target_text == "<<BLANK>>":
                data_text += replace_spans(
                    self.single_data_text_template, span_dict
                ) + '\n'
            else:
                data_text += replace_spans(
                    self.data_text_template, span_dict
                ) + '\n'

        return data_text.rstrip('\n')

    def build_question_text(self, qna):
        source_lang, source_text = qna[1][0], qna[1][1]
        target_lang = qna[2][0]
        span_dict = {
            "<<SRC_LANG>>": source_lang,
            "<<SRC_TEXT>>": source_text,
            "<<TRG_LANG>>": target_lang,
        }
        # make sure to include target_lang but NOT target_text
        if target_lang == "<<BLANK>>":
            question_text = replace_spans(
                self.single_question_text_template, span_dict
            )
        else:
            question_text = replace_spans(
                self.question_text_template, span_dict
            )

        return question_text
