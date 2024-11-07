import argparse


def get_args():
    parser = argparse.ArgumentParser()
    add_args(parser)

    args, _ = parser.parse_known_args()
    return args

def add_args(parser: argparse.ArgumentParser):
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--prompt_name", type=str, default="base")
    parser.add_argument("--run_name", type=str)

    # parser.add_argument('--do_eval',
    #                         type=bool,
    #                         default=False)

