# llms-and-puzzles

This is a repo for my masters thesis titled *Cracking the Code: How LLMs Solve Cryptic Clues, Linguistic Puzzles, and Logic Problems*. In this study we push the limit of LLMs reasoning capabilities testing them on challenging tasks: logic puzzles, Rosetta Stone puzzles, and cryptic crosswords. We mainly use *0-shot* and *few-shot* approaches and test a lot of different methods inside those approaches.

This repo is structured as follows:

- All the experiments are run through `eval.bash` or `inference.py` scripts. `inference.py` contains all the technical details of inferecing the model models with `vllm` library.
- All prompts are found in `.yaml` files corresponding to the tasks: `logic_puzzles_prompts.yaml` and others.
- In the `dataset_preparation.py` you can find base class for the datasets with details on how selection and ranking of *few-shot* examples are working inside this study.
- Details on how the dataset are processed can be found in specific `.py` files: `logic_puzzles.py` and others. Answer extraction and evaluation methods are also contained in those files, as they are task specfic. 
- Finally, `analysis.py` contains code for significance testing (`compare_two_groups` to compare two groups of prompts and `analyze_prompt_effectiveness` to compare prompts one by one) and analysis by task type. In `logs` folder we present `total_solutions_by_examples.csv` - a file with rows representing examples in the dataset and columns corresponding to an experiments (model + prompt). In this file 0 or 1 corresponds to whether the example has been solved in the experiment. Also, in `logs` folder you can find significance testing results for one by one comparisons of prompts. We omit actual logs of the models answers to save space.
