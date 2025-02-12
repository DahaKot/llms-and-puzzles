import prompts_list
from datasets import load_dataset, Dataset  # type: ignore
import json
import random
from utils import replace_spans
import re


class MyDataset():
    def __init__(self, dataset_name, prompt_name, similarity="random",
                 order="random", n_shots=0):
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
        self.order = order

        self.n_shots = n_shots

    def check_answer_against_correct(prediction, correct_answer):
        pass

    def random_similarity(example):
        pass

    def semantic_similarity(example):
        pass

    def thematic_similarity(example):
        pass

    def generate_prompt(example, prompt_name, similarity):
        pass


class CrypticCrosswords(MyDataset):
    def __init__(
            self, prompt_name, similarity="random", order="random", n_shots=0):
        super().__init__(
            "cryptic_crosswords", prompt_name, similarity, order, n_shots
        )

        self.dataset = load_dataset("boda/guardian_naive_random", split="test")

        self.mapped_dataset = self.dataset.map(
            self.generate_prompt,
            fn_kwargs={"prompt_name": prompt_name},
            load_from_cache_file=False
        )

    def generate_prompt(self, example, prompt_name):
        clue = example['input']
        prompt = prompts_list.cryptic_crosswords_prompts[prompt_name]

        if self.n_shots:
            few_shot_examples = self.similarity(example)
            example["prompt"] = prompt.format(clue=clue, **few_shot_examples)
        else:
            example["prompt"] = prompt.format(clue=clue)

        return example

    def _too_similar(self, example1, example2):
        return example1["target"] in example2["target"] \
               or example2["target"] in example1["target"]

    def random_similarity(self, example):
        # here maybe we need a filter so that there is no clue with the same
        # answer in the examples
        random.seed(42)

        examples = []
        while len(examples) < self.n_shots:
            random_index = random.sample(range(len(self.dataset)), 1)

            if not self._too_similar(self.dataset[random_index], example):
                examples.append(self.dataset[random_index])

        data = {}

        for i, example in enumerate(examples):
            data["clue" + str(i + 1)] = example["input"]
            data["answer" + str(i + 1)] = example["target"]

        return data

    def semantic_similarity(self, example):
        pass

    def thematic_similarity(self, example):
        pass

    def check_answer_against_correct(self, prediction, correct_answer):
        pattern = rf'\b{re.escape(correct_answer.lower())}\b'
        return bool(re.search(pattern, prediction.lower()))


class RosettaStone(MyDataset):
    def __init__(
            self, prompt_name, similarity="random", order="random", n_shots=0):
        super().__init__(
            "rosetta_stone", prompt_name, similarity, order, n_shots
        )

        self.modeling_raw = json.load(open(
            "./data/rosetta_stone/ModeLing_v2.json", "r", encoding="utf8"
        ))
        self.lingoly_raw = json.load(open(
            "./data/rosetta_stone/LingOly_v9.json", "r", encoding="utf8"
        ))

        modeling_data = self._load_modeling_data()
        lingoly_data = self._load_lingoly_data()
        combined_samples = modeling_data + lingoly_data

        self.dataset = Dataset.from_list(combined_samples)

        self.mapped_dataset = self.dataset.map(
            self.generate_prompt,
            fn_kwargs={"prompt_name": prompt_name},
            load_from_cache_file=False
        )

    def _load_modeling_data(self):
        dataset = json.load(open(
            "./data/rosetta_stone/ModeLing_v2.json", "r", encoding="utf8"
        ))

        prompt_builder = PromptBuilder(self.prompt_name)
        samples = []

        for d in dataset:
            data = d["cleaned_data"]["data"]
            qna = d["cleaned_data"]["qna"]
            language = re.sub(r"[\\d\\s]+", "", d["name"])
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
                    "language": language
                })

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
                    "language": language
                })

        return samples

    def generate_prompt(self, example, prompt_name):
        data = example['data']
        question = example['question']
        prompt = prompts_list.rosetta_stone_prompts[prompt_name]

        if self.n_shots:
            few_shot_examples = self.similarity(example)
            example["prompt"] = prompt.format(
                data=data, question=question, **few_shot_examples
            )
        else:
            example["prompt"] = prompt.format(data=data, question=question)

        return example

    def _too_similar(self, example1, example2):
        return example1["language"] == example2["language"]

    def random_similarity(self, example):
        # here we need to filter the same languages
        random.seed(42)

        examples = []
        while len(examples) < self.n_shots:
            random_index = random.sample(range(len(self.dataset)), 1)

            if not self._too_similar(self.dataset[random_index], example):
                examples.append(self.dataset[random_index])

        data = {}

        for i, example in enumerate(examples):
            data["data" + str(i + 1)] = example["data"]
            data["question" + str(i + 1)] = example["question"]

            one_correct_answer = json.loads(example["target"])[0]
            data["answer" + str(i + 1)] = one_correct_answer

        return data

    def semantic_similarity(self, example):
        pass

    def thematic_similarity(self, example):
        pass

    def check_answer_against_correct(self, prediction, correct_answer):
        correct_answers = json.loads(correct_answer)
        return any([a.lower() in prediction.lower() for a in correct_answers])


class LogicPuzzles(MyDataset):
    def __init__(
            self, prompt_name, similarity="random", order="random", n_shots=0):
        super().__init__(
            "logic_puzzles", prompt_name, similarity, order, n_shots
        )

        self.dataset = load_dataset(
            'json', split="train",
            data_files='./data/puzzle_ben/PuzzleBen_testset_updated.json'
        )

        self.mapped_dataset = self.dataset.map(
            self.generate_prompt,
            fn_kwargs={
                "prompt_name": prompt_name
            },
            load_from_cache_file=False
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

    def generate_prompt(self, example, prompt_name):
        problem = example["problem"]
        prompt = prompts_list.logic_puzzles_prompts[prompt_name]

        example["possible_answers_string"] = self._generate_options_string(
            example
        )

        if self.n_shots:
            few_shot_examples = self.similarity(example)
            example["prompt"] = prompt.format(
                problem=problem,
                options=example["possible_answers_string"], **few_shot_examples
            )
        else:
            example["prompt"] = prompt.format(
                problem=problem, options=example["possible_answers_string"]
            )

        letter_options = ["A", "B", "C", "D", "E"]
        example["target"] = letter_options[example["answer"] - 1]

        return example

    def _too_similar(self, example1, example2):
        return example1["problem"] == example2["problem"]

    def random_similarity(self, example):
        letter_options = ["A", "B", "C", "D", "E"]

        random.seed(42)

        examples = []
        while len(examples) < self.n_shots:
            random_index = random.sample(range(len(self.dataset)), 1)

            if not self._too_similar(self.dataset[random_index], example):
                examples.append(self.dataset[random_index])

        data = {}

        for i, example in enumerate(examples):
            data["problem" + str(i + 1)] = example["problem"]
            data["answer" + str(i + 1)] = letter_options[example["answer"] - 1]
            data["options" + str(i + 1)] = self._generate_options_string(
                example
            )

        return data

    def semantic_similarity(self, example):
        pass

    def thematic_similarity(self, example):
        pass

    def check_answer_against_correct(self, prediction, correct_answer):
        prediction = prediction.replace("[", "").lower()
        answer_position = prediction.find("answer: ")
        if answer_position < 0:
            return False
        answer = prediction[answer_position + 8: answer_position + 9]
        return answer.lower() == correct_answer.lower()


def get_dataset_with_prompts(dataset_name, prompt_name="base",
                             similarity="random", order="random", n_shots=0):
    datasets = {
        "cryptic_crosswords": CrypticCrosswords, "rosetta_stone": RosettaStone,
        "logic_puzzles": LogicPuzzles
    }

    wrapped_dataset = datasets[dataset_name](
        prompt_name, similarity, order, n_shots
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
