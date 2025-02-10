import prompts_list
from datasets import load_dataset, Dataset  # type: ignore
import re
import json
import random


N_SHOTS = 5


def exact_match(prediction, correct_answer, multiple_answers=False):
    if not multiple_answers:
        return correct_answer.lower() in prediction
    else:
        correct_answers = json.loads(correct_answer)
        print("correct_answers: ", correct_answers)
        return any([a.lower() in prediction for a in correct_answers])


def check_answer_against_correct(
        prediction, correct_answer, dataset, logprobs=None):
    if dataset == "cryptic_crosswords":
        return correct_answer.lower() in prediction.lower()
    elif dataset == "rosetta_stone":
        correct_answers = json.loads(correct_answer)
        return any([a.lower() in prediction.lower() for a in correct_answers])
    elif dataset == "logic_puzzles":
        # here it's complicated, not sure, if it is the best way to compare
        prediction = prediction.replace("[", "").lower()
        answer_position = prediction.find("answer: ")
        if answer_position < 0:
            return False
        answer = prediction[answer_position + 8: answer_position + 9]
        return answer.lower() == correct_answer.lower()


def random_similarity(example, dataset):
    random.seed(42)
    random_indices = random.sample(range(len(dataset)), N_SHOTS)

    examples = [dataset[i] for i in random_indices]

    clues_answers = {}

    for i, example in enumerate(examples):
        clues_answers["clue" + str(i + 1)] = example["input"]
        clues_answers["answer" + str(i + 1)] = example["target"]

    return clues_answers


def semantic_similarity(example, dataset):
    random_indices = random.sample(range(len(dataset)), N_SHOTS)

    return [dataset[i] for i in random_indices]


def thematic_similarity(example, dataset):
    random_indices = random.sample(range(len(dataset)), N_SHOTS)

    return [dataset[i] for i in random_indices]


def generate_prompt(
        example, dataset="cryptic_crosswords", prompt_name="base",
        similarity=random_similarity, full_dataset=None):
    if dataset == "cryptic_crosswords":
        clue = example['input']
        prompt = prompts_list.cryptic_crosswords_prompts[prompt_name]

        if full_dataset:
            few_shot_examples = similarity(example, full_dataset)
            example["prompt"] = prompt.format(clue=clue, **few_shot_examples)
        else:
            example["prompt"] = prompt.format(clue=clue)
    elif dataset == "logic_puzzles":
        problem = example["problem"]

        number_options = ["Option1", "Option2", "Option3", "Option4", "Option5"]
        letter_options = ["A", "B", "C", "D", "E"]
        options = []
        for i, option in enumerate(example["options"]):
            option = option.replace(number_options[i], letter_options[i])
            options.append(option)
        options = "\n".join(options)

        example["possible_answers_string"] = options

        prompt = prompts_list.logic_puzzles_prompts[prompt_name]
        example["prompt"] = prompt.format(problem=problem, options=options)
        example["target"] = letter_options[example["answer"] - 1]

    return example


def get_dataset_with_prompts(
        dataset_name, prompt_name="base", similarity="random", order="random"):
    similarity_functions = {
        "random": random_similarity, "semantic": semantic_similarity,
        "thematic": thematic_similarity
    }
    include_full_dataset = prompt_name.startswith("5_shot")

    if dataset_name == "cryptic_crosswords":
        dataset = load_dataset("boda/guardian_naive_random", split="test")

        mapped_dataset = dataset.map(
            generate_prompt,
            fn_kwargs={
                "prompt_name": prompt_name, "dataset": dataset_name,
                "similarity": similarity_functions[similarity],
                "full_dataset": dataset if include_full_dataset else None,
            },
            load_from_cache_file=False
        )
        return mapped_dataset

    elif dataset_name == "rosetta_stone":
        dataset = json.load(open(
            "./data/rosetta_stone/ModeLing_v2.json", "r", encoding="utf8"
        ))
        prompt_builder = PromptBuilder(prompt_name)

        samples = []
        for d in dataset:
            data = d["cleaned_data"]["data"]
            qna = d["cleaned_data"]["qna"]
            for row in qna:
                message = prompt_builder.build_prompt_message(
                    data, qna_row=row, qna_whole=qna
                )
                samples.append({
                    "prompt": message,
                    "target": json.dumps([row[2][1]]),
                    "input": message,
                    "dataset": "ModeLing"
                })

        dataset = json.load(open(
           "./data/rosetta_stone/LingOly_v9.json", "r", encoding="utf8"
        ))

        for d in dataset:
            data = d["data"]
            qna = d["qna"]
            for row in qna:
                message = prompt_builder.build_prompt_message(
                    data, qna_row=row, qna_whole=qna
                )

                target = row[2][1]
                if type(target) is not list:
                    samples.append({
                        "prompt": message,
                        "target": json.dumps([target]),
                        "input": message,
                        "dataset": "LingOly"
                    })
                else:
                    if type(target[0]) is list:
                        one_list_target = []
                        for sublist in target:
                            one_list_target.extend(sublist)
                        target = list(set(one_list_target))

                    samples.append({
                        "prompt": message,
                        "target": json.dumps(target),
                        "input": message,
                        "dataset": "LingOly"
                    })

        return Dataset.from_list(samples)

    elif dataset_name == "logic_puzzles":
        dataset = load_dataset(
            'json', split="train",
            data_files='./data/puzzle_ben/PuzzleBen_testset_updated.json'
        )

        mapped_dataset = dataset.map(
            generate_prompt,
            fn_kwargs={
                "prompt_name": prompt_name, "dataset": dataset_name,
                "similarity": similarity_functions[similarity],
                "full_dataset": dataset if include_full_dataset else None,
            },
            load_from_cache_file=False
        )

        final_dataset = mapped_dataset.rename_column("problem", "input")
        final_dataset = final_dataset.remove_columns(["options"])

        return final_dataset


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

    def build_prompt_message(self, data, qna_row, qna_whole, **kwargs):
        task_prompt = self.build_task_prompt(
            data, qna_row, qna_whole, **kwargs
        )
        return task_prompt

    def build_task_prompt(self, data, qna_row, qna_whole=None, language=None):
        data_text = self.build_data_text(data)
        question_text = self.build_question_text(qna_row)
        all_questions_text = '\n\n'.join(
            [self.build_question_text(qna_r) for qna_r in qna_whole]) \
            if qna_whole is not None else ""

        lang = [lang_name for lang_name in [data[0][1][0], data[0][2][0]]
                if lang_name.lower().strip() != "english"][0] \
            if language is None else language

        span_dict = {
            "<<LANG>>": lang,
            "<<DATA>>": data_text,
            "<<QUESTION>>": question_text,
            "<<ALL_QUESTIONS>>": all_questions_text,
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


def replace_spans(template, span_dict):
    text = template
    for k, v in span_dict.items():
        text = text.replace(k, v)
    return text


def normalize_unicode(s):
    for x in re.findall(r"\\u([\da-f]{4})", s):
        s = s.replace(f"\\u{x}", chr(int(x, 16)))
    return s
