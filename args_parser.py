import argparse


def get_args():
    parser = argparse.ArgumentParser()
    add_args(parser)

    args, _ = parser.parse_known_args()
    return args


def add_args(parser: argparse.ArgumentParser):
    parser.add_argument("--run_name", type=str, required=True)
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--n_gpus", type=int, default=1)
    parser.add_argument("--n_shots", type=int, default=5)
    parser.add_argument("--max_tokens", type=int, default=256)
    parser.add_argument("--logprobs", type=int, default=1)
    parser.add_argument("--random_seed", type=int, default=42)
    parser.add_argument(
        "--dataset", type=str,
        choices=["cryptic_crosswords", "rosetta_stone", "logic_puzzles",
                 "cryptic_crosswords_types", "rosetta_stone_types"]
    )
    parser.add_argument(
        "--model", type=str,
        choices=["llama", "mixtral", "qwen", "deepseek"]
    )
    parser.add_argument(
        "--prompt_name", type=str, default="base",
        choices=["base", "advanced", "zero_shot_chain_of_thought", "5_shot",
                 "5_shot_solutions", "deepseek_advanced", "deepseek_anagram",
                 "deepseek_assemblage", "deepseek_double_defintion", 
                 "deepseek_container", "deepseek_hidden_word",
                 "base_mixtral_instruct", "advanced_mixtral_instruct",
                 "zero_shot_chain_of_thought_mixtral_instruct",
                 "5_shot_mixtral_instruct",
                 "5_shot_solutions_mixtral_instruct", "generate_solution"]
    )
    parser.add_argument(
        "--similarity", type=str, default="random",
        choices=["random", "semantic", "thematic"]
    )
    parser.add_argument(
        "--ranking", type=str, default="random",
        choices=["random", "semantic_top_to_bottom", "semantic_bottom_to_top"]
    )
