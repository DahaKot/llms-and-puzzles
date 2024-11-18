import json
from utils import replace_spans
import prompts_list

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


# class ModelingMinimalPromptBuilder(NullPromptBuilder):

#     def __init__(self):

#         self.system_prompt = ""
#         self.task_prompt_template = """Here are some expressions in <<LANG>> (a never-seen-before foreign language) and their translations in English:

# <<DATA>>

# Given the above examples, please translate the following expression.

# <<QUESTION>>

# """
#         self.data_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"<<TRG_TEXT>>\"\n"
#         self.question_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"\""

#         self.single_data_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n"
#         self.single_question_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\""

# class ModelingHandTunedPromptBuilder(NullPromptBuilder):

#     def __init__(self):

#         self.system_prompt = ""
#         self.task_prompt_template = """This is a translation puzzle. Below are example phrases in <<LANG>> (a never-seen-before foreign language) as well as their English translations. Some test phrases follow them. Your task is to look closely at the example phrases and use only the information from them to translate the test phrases.

# <<DATA>>

# Given the above examples, please translate the following expression.

# <<QUESTION>>

# """
#         self.data_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"<<TRG_TEXT>>\"\n"
#         self.question_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"\""

#         self.single_data_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n"
#         self.single_question_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\""

# class ModelingBasicCoTPromptBuilder(NullPromptBuilder):

#     def __init__(self):

#         self.system_prompt = ""
#         self.task_prompt_template = """This is a translation puzzle. Below are example phrases in <<LANG>> (a never-seen-before foreign language) as well as their English translations. Some test phrases follow them. Your task is to look closely at the example phrases and use only the information from them to translate the test phrases.

# <<DATA>>

# Given the above examples, please translate the following statements. Let’s think step by step in a logical way, using careful analytical reasoning to get the correct result.

# <<QUESTION>>

# """
#         self.data_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"<<TRG_TEXT>>\"\n"
#         self.question_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"\""

#         self.single_data_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n"
#         self.single_question_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\""

# class ModelingFullCoTPromptBuilder(NullPromptBuilder):

#     def __init__(self):

#         self.system_prompt = ""
#         self.task_prompt_template = """This is a translation puzzle. In a moment, you will use logic and analytical reasoning to translate from a never-seen-before language <<LANG>> to English. As a training example, here are some expressions in Spanish and their translations in English.

# 1. Spanish: ventana roja
# English: red window
# 2. Spanish: ventana azul
# English: blue window
# 3. Spanish: manzana azul
# English: blue apple

# Using the above examples, translate the following.
# Spanish: manzana roja

# ANSWER: English: red apple

# EXPLANATION: The first step we notice is that the word “ventana” must mean window because (1) the word “ventana” appears twice between sentences 1 and 2, and (2) the only word that appears twice in the English translation is “window.” Next, we infer that “roja” must be “red” and “azul” must be “blue” by process of elimination. Next, we guess that in Spanish, the noun precedes the adjective because “ventana” comes before “roja” and “azul.” Therefore, the noun in sentence 3 (“apple”) must correspond to the word preceding the adjective (“manzana”) in the Spanish translations. Putting this together, “manzana
# roja” must mean “red apple” in English.
 
# Using a similar logical and analytical reasoning to understand the grammar of the foreign languages step by step, look closely
# at the following example in <<LANG>> phrases and use only the information from them to translate the following test phrases.

# <<DATA>>

# Given the above examples, please translate the following statements.

# <<QUESTION>>

# """
#         self.data_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"<<TRG_TEXT>>\"\n"
#         self.question_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"\""

#         self.single_data_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n"
#         self.single_question_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\""

# class NoContextPromptBuilder(NullPromptBuilder):
    
#     def __init__(self):
        
#         self.system_prompt = ""
#         self.task_prompt_template = """This is a translation puzzle from a linguistics exam. Below are some test phrases to be translated in <<LANG>> (a never-seen-before foreign language) and some in English. You will be asked to translate a specific phrase from the set. 
 
# <<ALL_QUESTIONS>>
 
# Now translate the following phrase:
 
# <<QUESTION>>"""

#         self.data_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"<<TRG_TEXT>>\"\n"
#         self.question_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"\""

#         self.single_data_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n"
#         self.single_question_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\""

# class LingOlyStdPromptBuilder(NullPromptBuilder):

#     def __init__(self):

#         self.system_prompt = ""
#         self.task_prompt_template = """Below is a problem sheet from a lingusitics exam. You will first see the entire mapped data and questions, then be asked to respond to the questions individually. Your answers to the questions should rely only on reasoning about the information provided in the sheet.
# Data:

# <<DATA>>

# Questions:

# <<ALL_QUESTIONS>>

# Now respond to the following question from the set:

# <<QUESTION>>
# """
#         self.data_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"<<TRG_TEXT>>\"\n"
#         self.question_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n<<TRG_LANG>>: \"\""

#         self.single_data_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\"\n"
#         self.single_question_text_template = "<<SRC_LANG>>: \"<<SRC_TEXT>>\""

