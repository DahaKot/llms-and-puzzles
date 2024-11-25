import argparse


def get_args():
    parser = argparse.ArgumentParser()
    add_args(parser)

    args, _ = parser.parse_known_args()
    return args

def add_args(parser: argparse.ArgumentParser):
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--run_name", type=str, required=True)
    parser.add_argument(
        "--dataset", type=str, choices=["cryptic_crosswords", "rosetta_stone"]
    )
    parser.add_argument(
        "--model", type=str, choices=["llama8b", "mixtral7x8b"]
    )
    parser.add_argument(
        "--prompt_name", type=str, default="base", choices=["base", "advanced"]
    )

