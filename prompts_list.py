cryptic_crosswords_prompts = {"base": '''You are a cryptic crossword expert. You are given a clue for a cryptic crossword. Output only the answer. 
clue:
{clue}
answer:
''',
"advanced": '''You are a cryptic crossword expert. The cryptic clue consists of a definition and a wordplay.
The definition is a synonym of the answer and usually comes at the beginning or the end of the clue.
The wordplay gives some instructions on how to get to the answer in another (less literal) way.
The number/s in the parentheses at the end of the clue indicates the number of letters in the answer.
Extract the definiton and the wordplay in the clue, and use them to solve the clue. Finally, output the answer in this format:
answer:
<answer>,
clue:
{clue}
answer:
''',
"base_mixtral_instruct": '''[INST] You are a cryptic crossword expert. You are given a clue for a cryptic crossword. Output only the answer.
clue:
{clue}
answer:
[/INST]''',
"advanced_mixtral_instruct": '''[INST] You are a cryptic crossword expert. The cryptic clue consists of a definition and a wordplay.
The definition is a synonym of the answer and usually comes at the beginning or the end of the clue.
The wordplay gives some instructions on how to get the answer in another (less literal) way.
The number/s in the parentheses at the end of the clue indicates the number of letters in the answer.
Extract the definition and the wordplay in the clue, and use them to solve the clue. Finally, output the answer in this format:
answer:
<answer>,
clue:
{clue}
answer:
[/INST]'''
}

rosetta_stone_prompts = {"base": '''Here are some expressions in <<LANG>> (a never-seen-before foreign language) and their translations in English:

<<DATA>>

Given the above examples, please translate the following expression.

<<QUESTION>>
''',
"advanced": '''This is a translation puzzle. Below are example phrases in <<LANG>> (a never-seen-before foreign language) as well as their English translations. Some test phrases follow them. Your task is to look closely at the example phrases and use only the information from them to translate the test phrases.

<<DATA>>

Given the above examples, please translate the following expression.

<<QUESTION>>
'''}

logic_puzzles_prompts = {"base": '''{problem}
Possible answers:
{options}
Please, outout the number of the correct answer only:
''',
"advanced": '''You are a cryptic crossword expert. The cryptic clue consists of a definition and a wordplay.
The definition is a synonym of the answer and usually comes at the beginning or the end of the clue.
The wordplay gives some instructions on how to get to the answer in another (less literal) way.
The number/s in the parentheses at the end of the clue indicates the number of letters in the answer.
Extract the definiton and the wordplay in the clue, and use them to solve the clue. Finally, output the answer on this format:
answer:
<answer>,
clue:
{clue}
answer:
'''
}
