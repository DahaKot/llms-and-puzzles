import prompts_list
from datasets import load_dataset, Dataset
import re
import json
import pandas as pd

def exact_match(prediction, correct_answer, multiple_answers=False):
    if not multiple_answers:
        return correct_answer.lower() in prediction
    else:
        correct_answers = json.loads(correct_answer)
        print("correct_answers: ", correct_answers)
        return any([a.lower() in prediction for a in correct_answers])

def generate_prompt(example, dataset="cryptic_crosswords", prompt_name="base"):
    clue = example['input']

    if dataset == "cryptic_crosswords":
        prompt = prompts_list.cryptic_crosswords_prompts[prompt_name]
    elif dataset == "logic_puzzles":
        prompt = prompts_list.logic_puzzles_prompts[prompt_name]

    example["prompt"] = prompt.format(clue=clue)

    return example

def get_dataset_with_prompts(dataset_name, prompt_name="base"):
    if dataset_name == "cryptic_crosswords":
        print("dataset is cryptic crosswords")
        dataset = load_dataset("boda/guardian_naive_random", split="test")

        mapped_dataset = dataset.map(
            generate_prompt,
            fn_kwargs={"prompt_name": prompt_name, "dataset": dataset_name},
            load_from_cache_file=True
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
                    samples.append({
                        "prompt": message,
                        "target": json.dumps(target),
                        "input": message,
                        "dataset": "LingOly"
                    })

        return Dataset.from_list(samples)
    
# the code is taken from KV Aditya Srivatsa and Mukund Choudhary
class PromptBuilder:
    def __init__(self, prompt_name):
        self.task_prompt_template = prompts_list.rosetta_stone_prompts[prompt_name]

        self.data_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"<<TRG_TEXT>>\"\n"
        self.question_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"\""

        self.single_data_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n"
        self.single_question_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\""

    def build_prompt_message(self, data, qna_row, qna_whole, **kwargs):
        task_prompt = self.build_task_prompt(data, qna_row, qna_whole, **kwargs)
        return task_prompt

    def build_task_prompt(self, data, qna_row, qna_whole=None, language=None):
        data_text = self.build_data_text(data)
        question_text = self.build_question_text(qna_row)
        all_questions_text = '\n\n'.join([self.build_question_text(qna_r) for qna_r in qna_whole]) if qna_whole != None else ""
        lang = [l for l in [data[0][1][0], data[0][2][0]] if l.lower().strip()!="english"][0] if language==None else language
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

            if target_lang=="<<BLANK>>" or target_text=="<<BLANK>>":
                data_text += replace_spans(self.single_data_text_template, span_dict) + '\n'
            else:
                data_text += replace_spans(self.data_text_template, span_dict) + '\n'

        return data_text.rstrip('\n')

    def build_question_text(self, qna):
        source_lang, source_text = qna[1][0], qna[1][1]
        target_lang, target_text = qna[2][0], qna[2][1] 
        span_dict = {
            "<<SRC_LANG>>": source_lang,
            "<<SRC_TEXT>>": source_text,
            "<<TRG_LANG>>": target_lang,
        }
        # make sure to include target_lang but NOT target_text
        if target_lang=="<<BLANK>>":
            question_text = replace_spans(self.single_question_text_template, span_dict)
        else:
            question_text = replace_spans(self.question_text_template, span_dict)

        return question_text

def replace_spans(template, span_dict):
    text = template
    for k, v in span_dict.items():
        text = text.replace(k,v)
    return text

def normalize_unicode(s):
    for x in re.findall(r"\\u([\da-f]{4})", s):
        s = s.replace(f"\\u{x}", chr(int(x, 16)))
    return s


