cryptic_crosswords_prompts = {"base": '''You are a cryptic crossword expert. You are given a clue for a cryptic crossword. Output only the answer. 
clue:
{clue}
answer:
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