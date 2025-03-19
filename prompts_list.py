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
<<<<<<< HEAD
=======
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
>>>>>>> e6673fda9f317101c5d71b7e28ee3c1ebec04d91
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
<<<<<<< HEAD
=======
"deepseek_advanced": '''Decipher the unknown sentence by systematically analyzing the parallel texts. Follow these steps:  

1. **Analyze Parallel Sentences**:  
   - Review the provided **Parallel sentences** to identify consistent structural patterns (e.g., sentence length, word/symbol positions, punctuation).  
   - Detect repeated elements (words, symbols, numbers) across sentences and note their alignment.  

2. **Establish Element Relationships**:  
   - Map recurring elements between known languages/texts (e.g., if a word appears in the same position in two sentences, hypothesize equivalence).  
   - Track frequencies and contextual usage to prioritize high-confidence matches.  

3. **Develop Translation Rules**:  
   - Propose rules (e.g., substitutions, transliterations, grammatical transformations) that align elements between parallel sentences.  
   - Validate rules by checking consistency across all parallel examples. Revise if contradictions arise.  

4. **Translate the Unknown Sentence**:  
   - Apply the validated rules to the **Sentence to translate**.  
   - Ensure the translation maintains structural coherence (e.g., word order, syntax) observed in the parallel sentences.  

5. **Verify and Refine**:  
   - Cross-check the translated sentence against the original patterns.  
   - Adjust rules if the output conflicts with established relationships or lacks logical consistency.  

**Input Data**:  
**Parallel sentences**: 
  {data}
**Sentence to translate**:
  {question}

Focus on positional alignment, frequency analysis, and iterative validation to decode the unknown text.
''',
"deepseek_POSS": '''Decipher the unknown sentence by systematically analyzing the possessive morphology patterns in the parallel texts. Follow these steps:  

1. **Identify Possessive Components**:  
   - Examine the **Parallel sentences** to isolate the **possessor** (owner) and **possessed noun** (owned item) in both the source and target language.  
   - Note the order of the possessor and possessed noun (e.g., possessor first vs. possessed first) and any markers (affixes, particles, or word order) indicating possession.  

2. **Map Morphological Patterns**:  
   - Compare equivalent phrases to determine how possession is marked (e.g., suffixes, prefixes, separate particles, or compounding).  
   - Identify how grammatical person (first, second, third), number (singular, plural), or noun class influence the possessive markers (e.g., "my" vs. "their").  

3. **Derive Possession Rules**:  
   - Formulate rules for the target language’s possessive structure (e.g., "In [Language], the possessor precedes the possessed noun, and ownership is marked with a suffix on the possessor").  
   - Validate rules by ensuring they apply consistently across all examples. Adjust if irregularities exist.  

4. **Apply Rules to Translate**:  
   - Break down the **Sentence to translate** into the possessor and possessed noun based on the source language.  
   - Modify these components according to the target language’s possessive rules (e.g., add affixes, adjust word order).  

5. **Cross-Validate Translation**:  
   - Verify that the translated phrase aligns with possessive markers and word order observed in the parallel texts.  
   - Ensure grammatical agreement (person, number) matches established patterns.  

**Input Data**:  
**Parallel sentences**:  
{data}  

**Sentence to translate**:  
{question}  

Prioritize morphological logic, possessive agreement, and iterative validation to decode the correct structure.
''',
"deepseek_SEM": '''Decipher the unknown semantic compounds by systematically analyzing morpheme alignment and meaning composition in the parallel texts. Follow these steps:  

1. **Identify Semantic Units**:  
   - Examine the **Parallel sentences** to isolate root words, affixes, and modifiers in both the source and target language.  
   - Note how these units combine to form compound meanings (e.g., directional terms, possession markers, tense/aspect indicators).  

2. **Map Meaning Relationships**:  
   - Compare equivalent phrases to determine how semantic units align across languages (e.g., a directional root in the source language might pair with a suffix in English).  
   - Highlight consistent compounding rules (e.g., modifiers precede roots, suffixes denote origin or directionality).  

3. **Derive Composition Rules**:  
   - Formulate rules for how semantic units combine in the target language (e.g., "In [Language], directionality is marked by a suffix derived from the root term").  
   - Validate rules by ensuring they explain all provided examples. Adjust if mismatches occur.  

4. **Apply Rules to Translate**:  
   - Deconstruct the **Sentence to translate** into its semantic components based on the source language’s compounding logic.  
   - Reassemble these components using the target language’s rules for meaning composition.  

5. **Cross-Validate Translation**:  
   - Verify that the translated phrase preserves the original semantic relationships (e.g., direction, possession, intensity).  
   - Ensure affixes, modifiers, and roots align with the established compounding patterns.  

**Parallel sentences**:  
{data}  

**Sentence to translate**:  
{question}  

Prioritize morpheme alignment, semantic consistency, and iterative validation to decode the correct compound meaning.
''',
"deepseek_ORDER": '''Decipher the unknown sentence by systematically analyzing the word order patterns in the parallel texts. Follow these steps:  

1. **Identify Core Components**:  
   - Examine the **Parallel sentences** to isolate the subject (S), verb (V), and object (O) in both the source and target language sentences.  
   - Note the relative positions of S, V, and O in each sentence pair (e.g., SVO, SOV, VSO).  

2. **Map Structural Patterns**:  
   - Compare sentences of equivalent meaning to determine how S, V, and O align across languages (e.g., a subject in English might occupy a different position in the target language).  
   - Highlight consistent word order rules (e.g., adjectives follow nouns, tense markers precede verbs).  

3. **Derive Syntactic Rules**:  
   - Formulate rules for the target language’s word order (e.g., "In [Language], the verb follows the subject but precedes the object").  
   - Validate rules by ensuring they apply universally across all provided examples. Adjust if exceptions emerge.  

4. **Apply Rules to Translate**:  
   - Break down the **Sentence to translate** into S, V, and O components based on the source language.  
   - Reorder these components according to the target language’s syntactic rules.  

5. **Cross-Validate Translation**:  
   - Verify that the translated sentence adheres to the word order patterns observed in the parallel texts.  
   - Ensure modifiers (e.g., adjectives, adverbs) and grammatical markers align with established positional rules.  

**Input Data**:  
**Parallel sentences**:  
{data}  

**Sentence to translate**:  
{question}  

Prioritize positional logic, syntactic consistency, and iterative validation to decode the correct word order.
''',
"deepseek_NOUN-ADJ": '''Decipher the unknown sentence by systematically analyzing the structural relationship between nouns and adjectives. Follow these steps:  

1. **Analyze Parallel Sentences**:  
   - Review the **Parallel sentences** to identify consistent patterns in noun-adjective order.  
   - Note whether adjectives precede or follow nouns in the target language by comparing word positions to their English translations.  

2. **Establish Word Relationships**:  
   - Map recurring adjectives and nouns across sentences (e.g., if "kümé" aligns with "good" in multiple examples, classify it as an adjective).  
   - Confirm consistency: Verify if the same word retains its role (noun/adjective) across all contexts.  

3. **Determine Word Order Rule**:  
   - Deduce the target language’s grammatical rule: Does it use **noun + adjective** or **adjective + noun** order?  
   - Cross-validate this rule against all parallel sentences to ensure no exceptions exist.  

4. **Apply the Rule to Translate**:  
   - For the **Sentence to translate**, first identify the noun and adjective based on established relationships.  
   - Arrange them according to the target language’s confirmed word order.  

5. **Validate and Refine**:  
   - Check if the translated sentence aligns structurally with all parallel examples.  
   - If conflicts arise, re-examine word roles or adjust the proposed order rule.  

**Input Data**:  
**Parallel sentences**: 
  {data}
  
**Sentence to translate**:
  {question}

Focus on positional patterns, role consistency, and rule validation to decode the correct noun-adjective order.
''',
>>>>>>> e6673fda9f317101c5d71b7e28ee3c1ebec04d91
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
<<<<<<< HEAD
=======
"deepseek_advanced": '''To solve any logic puzzle systematically, follow this adaptable framework:  

### **1. Classify the Puzzle Type**  
Determine the core structure (e.g., deductive reasoning, sequencing, spatial arrangement, trivia, or riddles/wordplay).  

### **2. Analyze Clues**  
- Break down explicit facts and implicit relationships.  
- Translate ambiguous or complex statements into clear constraints.  

### **3. Select Tools & Strategies**  
- **Logical/Deductive Puzzles**:  
  - Use elimination grids, mathematical comparisons, or conditional logic (*If X, then Y*).  
- **Sequencing/Ordering**:  
  - Identify chronological, causal, or structural links (e.g., dates, pronouns, cause-effect).  
- **Spatial/Seating Arrangements**:  
  - Sketch diagrams or tables to visualize positions and adjacency rules.  
- **Trivia/Knowledge-Based**:  
  - Leverage cultural, historical, or contextual associations.  
- **Riddles/Wordplay**:  
  - Decode abbreviations, homonyms, or thematic patterns.  

### **4. Test Hypotheses**  
- Propose tentative conclusions and check for contradictions.  
- Eliminate impossible options first.  

### **5. Validate Consistency**  
- Ensure the final solution satisfies *all* clues without exceptions.  

### **6. Match to Answer Choices**  
- Compare your conclusion to the provided options.  
- Prioritize answers that align with *all* constraints, not just some.  

**Puzzle**:  
{problem}  

**Possible Answers**:  
{options} 

**Answer**:  
[Correct Letter]
''',
"deepseek_brainteasers": '''**To solve logic puzzles and brain-teasers requiring structured analysis, apply this methodical approach:**  

**1. Analyze Clues & Relationships**  
- Identify **explicit elements** (objects, roles, constraints) and **implicit connections** (cause-effect, contradictions, dependencies).  
- Map out logical sequences or hierarchies implied by the narrative (e.g., generational roles, spatial setups, symbolic metaphors).  

**2. Identify Constraints & Patterns**  
- Note contradictions or paradoxes in the scenario (e.g., overlapping roles, conflicting testimonies, physical impossibilities).  
- Pinpoint recurring themes, wordplay, or double meanings (e.g., "chain gang" as both literal chains and collaboration).  

**3. Evaluate Answer Choices**  
- **Resolve Ambiguities**:  
  - Determine which option aligns with *all* constraints, including hidden premises (e.g., "four fathers" implies generational overlap).  
- **Eliminate Mismatches**:  
  - Reject choices that conflict with critical details (e.g., bullet trajectory vs. suspect positioning) or fail to address paradoxes.  
- **Validate Completeness**:  
  - Prioritize answers that explain *all* elements of the puzzle, not just isolated parts.  

**4. Stress-Test Solutions**  
- For each option, ask: *Does this account for every clue, resolve contradictions, and adhere to the puzzle’s logical framework?*  

**5. Prioritize Logical Consistency**  
- Select the answer that leaves no unresolved gaps, even if counterintuitive. Avoid assumptions beyond the given data.  

**Puzzle**:  
{problem}  

**Possible Answers**:  
{options}  

**Answer**:  
[Correct Letter]
''',
"deepseek_cr": '''**To solve critical reasoning puzzles involving paradoxes, assumptions, and conclusions, apply this structured approach:**  

**1. Deconstruct the Argument**  
- Identify the **stated premise(s)**, **unstated assumptions**, and **explicit conclusion**.  
- Highlight paradoxes or contradictions in the reasoning (e.g., self-referential claims, circular logic).  

**2. Evaluate Assumptions & Gaps**  
- Question implicit premises that bridge evidence to conclusion (e.g., causality vs. correlation, hidden biases).  
- Determine whether the conclusion logically follows from the premises.  

**3. Analyze Answer Choices**  
- **Strengthen/Weaken**:  
  - Identify which option directly impacts the conclusion’s validity by supporting/undermining assumptions or causal links.  
- **Resolve Paradoxes**:  
  - Seek answers that reconcile conflicting evidence or clarify ambiguous premises.  
- **Eliminate Distractors**:  
  - Discard choices that address irrelevant details, restate the premise, or introduce out-of-scope factors.  

**4. Stress-Test Hypotheses**  
- For each answer, ask: *Does this directly resolve the paradox, validate/break the assumption chain, or explain the conclusion’s plausibility?*  

**5. Prioritize Logical Precision**  
- Select the option that most tightly aligns with the argument’s core structure, avoiding tangential or partial solutions.  

**Puzzle**:  
{problem}  

**Possible Answers**:  
{options}  

**Answer**:  
[Correct Letter]
''',
"deepseek_puzzles": '''**To solve logic puzzles involving analogies, sequences, or relational reasoning, apply this structured approach:**  

**1. Identify Core Elements**  
- Break down the problem into **key components** (e.g., terms, relationships, sequence rules).  
- Clarify the **type of relationship** (categorical, functional, hierarchical) or **pattern** (positional, semantic, numerical).  

**2. Determine Relationships/Patterns**  
- For analogies, isolate the **primary link** (e.g., "Power : Watt" = concept : unit).  
- For sequences, identify **transition rules** (e.g., letter shifts, semantic categories, embedded patterns).  
- For relational puzzles, map **connections** (e.g., familial roles, cause-effect chains).  

**3. Analyze Answer Options**  
- **Test Consistency**: Check if each option aligns with the core relationship/pattern.  
- **Eliminate Misfits**: Discard choices that violate the rule, introduce irrelevant factors, or misrepresent the relationship.  
- **Resolve Ambiguities**: Prioritize answers that address *all* aspects of the problem (e.g., both term function *and* category).  

**4. Stress-Test Logic**  
- For each option, ask: *Does this maintain the structure of the original analogy, sequence, or relationship without introducing exceptions?*  

**5. Prioritize Structural Precision**  
- Select the answer that most directly and fully aligns with the problem’s logic, avoiding partial or overcomplicated solutions.  

**Puzzle**:  
{problem}  

**Possible Answers**:  
{options}  

**Answer**:  
[Correct Letter]
''',
"deepseek_riddles": '''**To solve metaphorical riddles requiring creative interpretation, apply this structured approach:**  

**1. Decode Metaphorical Language**  
- Identify **key metaphors**, **symbolic elements**, and **dual-meaning words** in each line.  
- Break down abstract descriptions into literal or conceptual equivalents (e.g., "darkness" as ignorance, "light" as knowledge).  

**2. Analyze Contradictions & Patterns**  
- Highlight paradoxical phrases or conflicting imagery (e.g., "rises in darkness but rises in light").  
- Look for repeating motifs, rhythmic patterns, or wordplay (e.g., homophones, hidden letters).  

**3. Evaluate Answer Choices**  
- **Literal vs. Symbolic**:  
  - Test whether options align with *both* literal clues and symbolic interpretations.  
- **Resolve Paradoxes**:  
  - Prioritize answers that logically reconcile contradictions in the riddle’s narrative.  
- **Eliminate Distractors**:  
  - Reject choices that fit only surface-level clues or ignore critical metaphors.  

**4. Stress-Test Interpretations**  
- For each option, ask: *Does this explain all lines of the riddle, resolve its paradoxes, and align with its symbolic structure?*  

**5. Prioritize Holistic Alignment**  
- Select the answer that integrates the most clues cohesively, avoiding partial or forced solutions.  

**Puzzle**:  
{problem}  

**Possible Answers**:  
{options}  

**Answer**:  
[Correct Letter]
''',
"deepseek_parajumble": '''**To solve parajumble puzzles requiring cause-effect analysis, apply this structured approach:**  

**1. Identify the Core Narrative**  
- Locate the **topic sentence** that establishes the central event, subject, or premise (often standalone and context-independent).  
- Discern whether the paragraph is **chronological**, **problem-solution**, or **argument-evidence** structured.  

**2. Map Cause-Effect Links**  
- Highlight sentences with explicit causal language (*because, since, therefore, as a result*).  
- Trace **actions** to their **consequences** and **reasons** to their **outcomes**, ensuring no gaps in logic.  

**3. Track Chronology & Transitions**  
- Note time markers (*first, later, finally*) and transitional phrases (*however, furthermore*).  
- Prioritize sequences where events or ideas progress logically (e.g., problem → action → result).  

**4. Resolve Pronouns & References**  
- Link pronouns (*it, they, this*) to their **antecedents** in prior sentences.  
- Identify contextual terms (*the decision, this process*) that depend on earlier explanations.  

**5. Evaluate Coherence**  
- Assemble a trial sequence and verify that each sentence **builds** on the prior one.  
- Check for contradictions, abrupt shifts, or unresolved references.  

**6. Eliminate Implausible Orders**  
- Cross-check options against your reconstructed flow.  
- Reject sequences where cause-effect chains break, pronouns lack antecedents, or chronology is violated.  

**Puzzle**:  
{problem}  

**Possible Answers**:  
{options}  

**Answer**:  
[Correct Letter]
''',
>>>>>>> e6673fda9f317101c5d71b7e28ee3c1ebec04d91
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
<<<<<<< HEAD
"5_shot_solutions_mixtral_instruct": '''[INST] You are a logic expert. You are given a logic puzzle along with several answer options. Solve the puzzle and provide only the letter of the correct option in the format: "answer: <option letter>".
=======
"5_shot_solutions": '''[INST] You are a logic expert. You are given a logic puzzle along with several answer options. Solve the puzzle and provide only the letter of the correct option in the format: "answer: <option letter>".
>>>>>>> e6673fda9f317101c5d71b7e28ee3c1ebec04d91
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
