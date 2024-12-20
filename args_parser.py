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
    parser.add_argument("--max_tokens", type=int, default=512)
    parser.add_argument(
        "--dataset", type=str, choices=["cryptic_crosswords", "rosetta_stone",
                                        "logic_puzzles"]
    )
    parser.add_argument(
        "--model", type=str, choices=["llama8b", "mixtral7x8b", "falcon40b",
                                      "mistral7b", "qwen"]
    )
    parser.add_argument(
        "--prompt_name", type=str, default="base", choices=["base", "advanced"]
    )
