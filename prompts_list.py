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
"generate_solution": '''You are a cryptic crossword expert. You are given a cryptic crossword clue and its answer. Generate a valid reasoning chain that arrives at the correct answer.
Clue:
{clue}
Answer:
{answer}
''',
"advanced": '''You are a cryptic crossword expert. You are given a cryptic crossword clue.
A cryptic clue typically consists of a definition and a wordplay. The definition is a synonym of the answer and usually appears at the beginning or the end of the clue. The wordplay provides instructions for deriving the answer in a less literal way. The number(s) in parentheses at the end of the clue indicate the length of the answer.
Extract the definition and the wordplay from the clue, then use them to solve it. Finally, provide the answer in the format "Answer: ...".
Clue:
{clue}
''',
"5_shot": '''You are a cryptic crossword expert. You are given a cryptic crossword clue. Solve the clue and provide only the answer.
Examples:
Clue:
{clue1}
Answer:
{answer1}

Clue:
{clue2}
Answer:
{answer2}

Clue:
{clue3}
Answer:
{answer3}

Clue:
{clue4}
Answer:
{answer4}

Clue:
{clue5}
Answer:
{answer5}

Clue:
{clue}
''',
"5_shot_solutions": '''You are a cryptic crossword expert. You are given a cryptic crossword clue. Solve the clue and provide the answer.
Examples:
Clue:
{clue1}
Solution:
{solution1}

Clue:
{clue2}
Solution:
{solution2}

Clue:
{clue3}
Solution:
{solution3}

Clue:
{clue4}
Solution:
{solution4}

Clue:
{clue5}
Solution:
{solution5}

Clue:
{clue}
''',
"deepseek_advanced": '''Analyze the cryptic clue by following these steps:  
1. **Identify Components**: Split the clue into its *definition* (usually at the start or end) and *wordplay* (the cryptic element).  
2. **Check for Common Cryptic Types**:  
   - **Anagram**: Look for words like *mixed, chaotic, broken*. Rearrange letters.  
   - **Charade**: Combine parts of words (e.g., *‘fish’ + ‘ing’ = ‘fishing’*).  
   - **Hidden Word**: Find a word concealed within the clue (e.g., *‘part of *castle*’ = ‘cast’*).  
   - **Reversal**: Words like *back, returning* hint at reversing letters (e.g., *‘flow’ reversed = ‘wolf’*).  
   - **Homophone**: Words like *heard, sounds like* indicate similar-sounding words.  
   - **Container/Insertion**: Words like *holding, inside* suggest inserting letters (e.g., *‘anger’ holding ‘v’ = ‘vanger’*).  
   - **Deletion**: Words like *losing, without* signal removing letters.  
3. **Parse Abbreviations/Symbols**: Convert parts of the clue into abbreviations (e.g., *‘queen’ = Q, ‘heart’ = ♥ = ‘art’*).  
4. **Double Definitions**: Check if the clue offers two distinct meanings for the answer.  
5. **Verify Answer**: Ensure the solution matches both the definition and wordplay, and fits the required letter count (if provided).  

**Clue:**
{clue}
**Final Output**: Clearly state the answer and explain how each component (definition + wordplay) leads to it.
''',
"deepseek_anagram": '''To solve this cryptic anagram clue, follow these steps:  
1. **Identify the definition**: This is the part of the clue that directly describes the answer (often at the start or end).  
2. **Locate the anagram indicator**: Look for words suggesting rearrangement, such as "change," "breaking," "shocking," "ridiculous," or "awkward."  
3. **Extract the letters**: Take the remaining words (excluding the definition and indicator) and combine their letters. Ignore punctuation and spaces.  
4. **Rearrange the letters**: Form a word or phrase that matches the definition and has the specified letter count (provided in parentheses).  

**Clue:**
{clue}
**Answer:**
''',
"deepseek_assemblage": '''To solve this cryptic *assemblage* clue, follow these steps:  
1. **Identify the definition**: This directly defines the answer, typically at the start or end of the clue.  
2. **Locate wordplay components**: Look for:  
   - **Extractions** (e.g., “fourth of X” = the 4th letter of X, “beginning” = first letter).  
   - **Synonyms** (e.g., “transport” = *vehicle*).  
   - **Abbreviations** (e.g., “prize” = *E* for “excellence”).  
   - **Hidden words** or letters at intervals (e.g., “at regular intervals” = every other letter).  
   - **Reversals** (e.g., “returning” = reverse a substring).  
3. **Break down each component**: Extract letters, substitute synonyms, apply abbreviations, or reverse segments as indicated.  
4. **Assemble the parts**: Combine the elements to form the answer, ensuring the total length matches the number in parentheses.  

**Clue:**
{clue}
**Answer:**
''',
"deepseek_container": '''To solve this cryptic *container* clue, follow these steps: 
1. **Identify the definition**: Determine the part of the clue that directly defines the answer, usually positioned at the beginning or end.  
2. **Spot insertion indicators**: Look for words or phrases like "in," "around," "holding," "encased," or "invested in," which signal that one substring (*contained*) is nested inside another (*container*).  
3. **Break down components**:  
   - **Container**: Identify the outer substring (often a synonym, abbreviation, or truncated word).  
   - **Contained**: Locate the inner substring to be inserted (check for synonyms, abbreviations, or wordplay like reversals).  
4. **Assemble**: Insert the *contained* substring into the *container*, ensuring proper letter order.  
5. **Verify length**: Confirm the total letters match the number in parentheses.  

**Clue:**
{clue}
**Answer:**
''',
"deepseek_double_definition": '''To solve a cryptic double definition clue, follow these steps:  

1. **Identify the two definitions**: Split the clue into segments that represent *two distinct meanings* of the same word.  
2. **Consider homonyms and polysemes**: Look for a word with separate definitions (e.g., differing parts of speech, alternate pronunciations, or unrelated meanings).  
3. **Match the letter count**: Ensure the answer aligns with the specified length (provided in parentheses).  
4. **Verify mutual fit**: Confirm the word logically satisfies *both* definitions without relying on wordplay (e.g., anagrams or hidden words).  

**Clue:**
{clue}
**Answer:**
''',
"deepseek_double_hidden_word": '''To solve this cryptic *hidden word* clue, follow these steps:  
1. **Identify the definition**: This directly defines the answer, often positioned at the start or end of the clue.  
2. **Locate hidden indicators**: Look for terms like “kept by,” “from,” “in,” “offering,” or “contained in” that signal letters are embedded within adjacent words.  
3. **Analyze the text as a continuous string**: Ignore spaces and punctuation. Search for a consecutive sequence of letters matching the specified length (in parentheses), which may span multiple words.  
4. **Confirm the answer**: Ensure the extracted letters align with the definition and length requirement.  

**Clue:**
{clue}
**Answer:**
''',
"base_mixtral_instruct": '''[INST] You are a cryptic crossword expert. You are given a cryptic crossword clue. Solve the clue and provide only the answer.
Clue:
{clue}
Answer:
[/INST]
''',
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
[/INST]
''',
"5_shot_mixtral_instruct": '''[INST] You are a cryptic crossword expert. You are given a cryptic crossword clue. Solve the clue and provide only the answer.
Examples:
Clue:
{clue1}
Answer:
{answer1}

Clue:
{clue2}
Answer:
{answer2}

Clue:
{clue3}
Answer:
{answer3}

Clue:
{clue4}
Answer:
{answer4}

Clue:
{clue5}
Answer:
{answer5}

Clue:
{clue}
[/INST]
''',
"5_shot_solutions_mixtral_instruct": '''[INST] You are a cryptic crossword expert. You are given a cryptic crossword clue. Solve the clue and provide the answer.
Examples:
Clue:
{clue1}
Solution:
{solution1}

Clue:
{clue2}
Solution:
{solution2}

Clue:
{clue3}
Solution:
{solution3}

Clue:
{clue4}
Solution:
{solution4}

Clue:
{clue5}
Solution:
{solution5}

Clue:
{clue}
[/INST]
'''
}

rosetta_stone_prompts = {"base": '''You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. Translate the sentence and provide only the answer.
Parallel sentences:
{data}

Sentence to translate:
{question}
Answer:
''',
"zero_shot_chain_of_thought": '''You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. Translate the sentence.
Parallel sentences:
{data}

Sentence to translate:
{question}
Answer:
Let's think step by step.
''',
"generate_solution": '''You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. The translation of the last sentence is the answer and it is given to you. Generate a valid reasoning chain that arrives at the correct answer.
Parallel sentences:
{data}

Sentence to translate:
{question}
Answer:
{answer}
''',
"advanced": '''You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. Rosetta Stone puzzles require the solver to map vocabulary from one language to another and identify patterns in word order, affixes, and other linguistic features.
Analyze how the language works and apply the deduced rules to translate the new sentence. Finally, provide the answer in the format "Answer: ...".
Parallel sentences:
{data}

Sentence to translate:
{question}
''',
"5_shot": '''You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. Translate the sentence and provide only the answer.
Examples:
Parallel sentences:
{data1}
Sentence to translate:
{question1}
Answer:
{answer1}

Parallel sentences:
{data2}
Sentence to translate:
{question2}
Answer:
{answer2}

Parallel sentences:
{data3}
Sentence to translate:
{question3}
Answer:
{answer3}

Parallel sentences:
{data4}
Sentence to translate:
{question4}
Answer:
{answer4}

Parallel sentences:
{data5}
Sentence to translate:
{question5}
Answer:
{answer5}

Parallel sentences:
{data}

Sentence to translate:
{question}
''',
"5_shot_solutions": '''You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. Translate the sentence and provide the answer.
Examples:
Parallel sentences:
{data1}
Sentence to translate:
{question1}
Solution:
{solution1}

Parallel sentences:
{data2}
Sentence to translate:
{question2}
Solution:
{solution2}

Parallel sentences:
{data3}
Sentence to translate:
{question3}
Solution:
{solution3}

Parallel sentences:
{data4}
Sentence to translate:
{question4}
Solution:
{solution4}

Parallel sentences:
{data5}
Sentence to translate:
{question5}
Solution:
{solution5}

Parallel sentences:
{data}

Sentence to translate:
{question}
''',
"base_mixtral_instruct": '''[INST] You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. Translate the sentence and provide only the answer.
Parallel sentences:
{data}

Sentence to translate:
{question}
Answer:
[/INST]
''',
"zero_shot_chain_of_thought_mixtral_instruct": '''[INST] You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. Translate the sentence.
Parallel sentences:
{data}

Sentence to translate:
{question}
Answer:
Let's think step by step.
[/INST]
''',
"advanced_mixtral_instruct": '''[INST] You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. Rosetta Stone puzzles require the solver to map vocabulary from one language to another and identify patterns in word order, affixes, and other linguistic features.
Analyze how the language works and apply the deduced rules to translate the new sentence. Finally, provide the answer in the format "Answer: ...".
Parallel sentences:
{data}

Sentence to translate:
{question}
[/INST]
''',
"5_shot_mixtral_instruct": '''[INST] You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. Translate the sentence and provide only the answer.
Examples:
Parallel sentences:
{data1}
Sentence to translate:
{question1}
Answer:
{answer1}

Parallel sentences:
{data2}
Sentence to translate:
{question2}
Answer:
{answer2}

Parallel sentences:
{data3}
Sentence to translate:
{question3}
Answer:
{answer3}

Parallel sentences:
{data4}
Sentence to translate:
{question4}
Answer:
{answer4}

Parallel sentences:
{data5}
Sentence to translate:
{question5}
Answer:
{answer5}

Parallel sentences:
{data}

Sentence to translate:
{question}
[/INST]
''',
"5_shot_solutions_mixtral_instruct": '''[INST] You are a linguistic expert. You are given a Rosetta Stone puzzle containing several parallel sentences in two languages, followed by a new sentence to translate. Translate the sentence and provide the answer.
Examples:
Parallel sentences:
{data1}
Sentence to translate:
{question1}
Solution:
{solution1}

Parallel sentences:
{data2}
Sentence to translate:
{question2}
Solution:
{solution2}

Parallel sentences:
{data3}
Sentence to translate:
{question3}
Solution:
{solution3}

Parallel sentences:
{data4}
Sentence to translate:
{question4}
Solution:
{solution4}

Parallel sentences:
{data5}
Sentence to translate:
{question5}
Solution:
{solution5}

Parallel sentences:
{data}

Sentence to translate:
{question}
[/INST]
'''
}

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
"generate_solution": '''You are a logic expert. You are given a logic puzzle along with several answer options. The correct answer is given to you. Generate a valid reasoning chain that arrives at the correct answer.
Puzzle:
{problem}
Possible answers:
{options}
Answer:
{answer}
''',
"advanced": '''You are a logic expert. You are given a logic puzzle with several answer options. Logic puzzles often require breaking the problem into smaller components, identifying patterns, applying rules or reasoning, and eliminating incorrect options to arrive at the solution.
Solve the puzzle. Finally, provide the letter of the correct option in the format: "answer: <option letter>".
Puzzle:
{problem}
Possible answers:
{options}
''',
"5_shot": '''You are a logic expert. You are given a logic puzzle along with several answer options. Solve the puzzle and provide only the letter of the correct option in the format: "answer: <option letter>".
Examples:
Puzzle:
{problem1}
Possible answers:
{options1}
Answer:
{answer1}

Puzzle:
{problem2}
Possible answers:
{options2}
Answer:
{answer2}

Puzzle:
{problem3}
Possible answers:
{options3}
Answer:
{answer3}

Puzzle:
{problem4}
Possible answers:
{options4}
Answer:
{answer4}

Puzzle:
{problem5}
Possible answers:
{options5}
Answer:
{answer5}

Puzzle:
{problem}
Possible answers:
{options}
''',
"5_shot_solutions": '''You are a logic expert. You are given a logic puzzle along with several answer options. Solve the puzzle and provide only the letter of the correct option in the format: "answer: <option letter>".
Examples:
Puzzle:
{problem1}
Possible answers:
{options1}
Solution:
{solution1}

Puzzle:
{problem2}
Possible answers:
{options2}
Solution:
{solution2}

Puzzle:
{problem3}
Possible answers:
{options3}
Solution:
{solution3}

Puzzle:
{problem4}
Possible answers:
{options4}
Solution:
{solution4}

Puzzle:
{problem5}
Possible answers:
{options5}
Solution:
{solution5}

Puzzle:
{problem}
Possible answers:
{options}
''',
"base_mixtral_instruct": '''[INST] You are a logic expert. You are given a logic puzzle along with several answer options. Solve the puzzle and provide only the letter of the correct option in the format: "answer: <option letter>".
Puzzle:
{problem}
Possible answers:
{options}
Answer:
[/INST]
''',
"zero_shot_chain_of_thought_mixtral_instruct": '''[INST] You are a logic expert. You are given a logic puzzle along with several answer options. Solve the puzzle and provide the letter of the correct option in the format: "answer: <option letter>".
Puzzle:
{problem}
Possible answers:
{options}
Answer:
Let's think step by step.
[/INST]
''',
"advanced_mixtral_instruct": '''[INST] You are a logic expert. You are given a logic puzzle with several answer options. Logic puzzles often require breaking the problem into smaller components, identifying patterns, applying rules or reasoning, and eliminating incorrect options to arrive at the solution.
Solve the puzzle. Finally, provide the letter of the correct option in the format: "answer: <option letter>".
Puzzle:
{problem}
Possible answers:
{options}
[/INST]''',
"5_shot_mixtral_instruct": '''[INST] You are a logic expert. You are given a logic puzzle along with several answer options. Solve the puzzle and provide only the letter of the correct option in the format: "answer: <option letter>".
Examples:
Puzzle:
{problem1}
Possible answers:
{options1}
Answer:
{answer1}

Puzzle:
{problem2}
Possible answers:
{options2}
Answer:
{answer2}

Puzzle:
{problem3}
Possible answers:
{options3}
Answer:
{answer3}

Puzzle:
{problem4}
Possible answers:
{options4}
Answer:
{answer4}

Puzzle:
{problem5}
Possible answers:
{options5}
Answer:
{answer5}

Puzzle:
{problem}
Possible answers:
{options}
[/INST]
''',
"5_shot_solutions": '''[INST] You are a logic expert. You are given a logic puzzle along with several answer options. Solve the puzzle and provide only the letter of the correct option in the format: "answer: <option letter>".
Examples:
Puzzle:
{problem1}
Possible answers:
{options1}
Solution:
{solution1}

Puzzle:
{problem2}
Possible answers:
{options2}
Solution:
{solution2}

Puzzle:
{problem3}
Possible answers:
{options3}
Solution:
{solution3}

Puzzle:
{problem4}
Possible answers:
{options4}
Solution:
{solution4}

Puzzle:
{problem5}
Possible answers:
{options5}
Solution:
{solution5}

Puzzle:
{problem}
Possible answers:
{options}
[/INST]
''',
}
