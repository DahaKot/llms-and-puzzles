import csv
import json

from datasets import Dataset  # type: ignore
import yaml  # type: ignore

from dataset_preparation import BaseDataset
from utils import replace_spans


class RosettaStone(BaseDataset):
    def __init__(
            self, prompt_name, similarity="random", ranking="random",
            n_shots=0, random_seed=42):
        self.embedding_field = "data"

        with open("rosetta_stone_prompts.yaml", "r") as file:
            self.prompts = yaml.safe_load(file)

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

        prompt_builder = PromptBuilder()
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

        prompt_builder = PromptBuilder()
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
        prompt = self.prompts[prompt_name]

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

        with open("rosetta_stone_prompts.yaml", "r") as file:
            self.prompts = yaml.safe_load(file)

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

    def generate_prompt(self, example, index, prompt_name):
        data = example['data']
        question = example['question']

        if "types" in prompt_name:
            example_type = None
            for t in self.type_dict:
                if index in self.type_dict[t]:
                    example_type = t

            if example_type:
                if "short" in prompt_name:
                    prompt_name = "deepseek_short_" + example_type
                else:
                    prompt_name = "deepseek_" + example_type

                if "mixtral_instruct" in prompt_name:
                    prompt_name += "_mixtral_instruct"
                    
                prompt = self.prompts[prompt_name]
                example["prompt"] = prompt.format(data=data, question=question)
            else:
                raise TypeError(
                    "coudnt find type of this example"
                )

            return example

        prompt = self.prompts[prompt_name]

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


# the code is taken from KV Aditya Srivatsa and Mukund Choudhary
class PromptBuilder:
    def __init__(self):
        # self.task_prompt_template = \
        #     prompts_list.rosetta_stone_prompts[prompt_name]

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

    # def build_prompt_message(self, data, qna_row, qna_whole, **kwargs):
    #     task_prompt = self.build_task_prompt(
    #         data, qna_row, qna_whole, **kwargs
    #     )
    #     return task_prompt

    # def build_task_prompt(self, data, qna_row, qna_whole=None, language=None)
    #     data_text = self.build_data_text(data)
    #     question_text = self.build_question_text(qna_row)

    #     span_dict = {
    #         "<<DATA>>": data_text,
    #         "<<QUESTION>>": question_text
    #     }
    #     task_prompt = replace_spans(self.task_prompt_template, span_dict)
    #     return task_prompt

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
