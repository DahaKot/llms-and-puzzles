cryptic_crosswords_prompts = {"base": '''You are a cryptic crossword expert. You are given a cryptic crossword clue. Solve the clue and provide only the answer.
Clue:
{clue}
Answer:
''',
"zero_shot_chain_of_thought": '''You are a cryptic crossword expert. You are given a cryptic crossword clue. Solve the clue.
Clue:
{clue}
Answer:
Let's think step by step.
''',
"advanced": '''You are a cryptic crossword expert. You are given a cryptic crossword clue.
A cryptic clue typically consists of a definition and a wordplay. The definition is a synonym of the answer and usually appears at the beginning or the end of the clue. The wordplay provides instructions for deriving the answer in a less literal way. The number(s) in parentheses at the end of the clue indicate the length of the answer.
Extract the definition and the wordplay from the clue, then use them to solve it. Finally, provide the answer in the format "Answer: ...".
Clue:
{clue}
''',
"base_mixtral_instruct": '''[INST] You are a cryptic crossword expert. You are given a cryptic crossword clue. Solve the clue and provide only the answer.
Clue:
{clue}
Answer:
[/INST]''',
"zero_shot_chain_of_thought_mixtral_instruct": '''[INST] You are a cryptic crossword expert. You are given a cryptic crossword clue. Solve the clue.
Clue:
{clue}
Answer:
Let's think step by step.
[/INST]
''',
"advanced_mixtral_instruct": '''[INST] You are a cryptic crossword expert. You are given a cryptic crossword clue.
A cryptic clue typically consists of a definition and a wordplay. The definition is a synonym of the answer and usually appears at the beginning or the end of the clue. The wordplay provides instructions for deriving the answer in a less literal way. The number(s) in parentheses at the end of the clue indicate the length of the answer.
Extract the definition and the wordplay from the clue, then use them to solve it. Finally, provide the answer in the format "Answer: ...".
Clue:
{clue}
[/INST]'''
}

rosetta_stone_prompts = {"base": '''You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. Translate the sentence and provide only the answer.
Parallel sentences:
<<DATA>>
Sentence to translate:
<<QUESTION>>
Answer:
''',
"zero_shot_chain_of_thought": '''You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. Translate the sentence.
Parallel sentences:
<<DATA>>
Sentence to translate:
<<QUESTION>>
Answer:
Let's think step by step.
''',
"advanced": '''You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. Rosetta Stone puzzles require the solver to map vocabulary from one language to another and identify patterns in word order, affixes, and other linguistic features.
Parallel sentences:
<<DATA>>
Analyze how the language works and apply the deduced rules to translate the new sentence. Finally, provide the answer in the format "Answer: ...".
<<QUESTION>>
''',
"base_mixtral_instruct": '''[INST] You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate.
Parallel sentences:
<<DATA>>
Translate the sentence and provide only the answer.
<<QUESTION>>
Answer:
[/INST]
''',
"zero_shot_chain_of_thought_mixtral_instruct": '''[INST] You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. Translate the sentence.
Parallel sentences:
<<DATA>>
Sentence to translate:
<<QUESTION>>
Answer:
Let's think step by step.
[/INST]
''',
"advanced_mixtral_instruct": '''[INST] You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. Rosetta Stone puzzles require the solver to map vocabulary from one language to another and identify patterns in word order, affixes, and other linguistic features.
Parallel sentences:
<<DATA>>
Analyze how the language works and apply the deduced rules to translate the new sentence. Finally, provide the answer in the format "Answer: ...".
<<QUESTION>>
[/INST]
'''}

logic_puzzles_prompts = {"base": '''You are a logic expert. You are given a logic puzzle along with several answer options. Solve the puzzle and provide only the letter of the correct option in the format: "answer: <option letter>".
Puzzle:
{problem}
Possible answers:
{options}
Answer:
''',
"zero_shot_chain_of_thought": '''You are a logic expert. You are given a logic puzzle along with several answer options. Solve the puzzle and provide the letter of the correct option in the format: "answer: <option letter>".
Puzzle:
{problem}
Possible answers:
{options}
Answer:
Let's think step by step.
''',
"advanced": '''You are a logic expert. You are given a logic puzzle with several answer options. Logic puzzles often require breaking the problem into smaller components, identifying patterns, applying rules or reasoning, and eliminating incorrect options to arrive at the solution.
Solve the puzzle. Finally, provide the letter of the correct option in the format: "answer: <option letter>".
Puzzle:
{problem}
Possible answers:
{options}
''',
"base_mixtral_instruct": '''[INST] You are a logic expert. You are given a logic puzzle along with several answer options. Solve the puzzle and provide only the number of the correct option.
Puzzle:
{problem}
Possible answers:
{options}
Answer:
[/INST]''',
"advanced_mixtral_instruct": '''[INST] You are a logic expert. You are given a logic puzzle with several answer options. Logic puzzles often require breaking the problem into smaller components, identifying patterns, applying rules or reasoning, and eliminating incorrect options to arrive at the solution.
Solve the puzzle. Finally, provide the number of the correct option in the format "Answer: ...".
Puzzle:
{problem}
Possible answers:
{options}
[/INST]'''
}
