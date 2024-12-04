from tqdm import tqdm
from utils import get_dataset_with_prompts, exact_match

from torch.utils.data import DataLoader
from args_parser import get_args
from vllm import LLM, SamplingParams
import json
from models_list import models_dict

if __name__ == "__main__":
    args = get_args()

    dataset = get_dataset_with_prompts(args.dataset, args.prompt_name)
    dataset_length = len(dataset)
    dataloader = DataLoader(dataset, batch_size=args.batch_size)

    model = LLM(
        model=models_dict[args.model],
        dtype="float16",
        max_model_len=4098,
        gpu_memory_utilization=0.8,
        tensor_parallel_size=args.n_gpus
    )
    tokenizer = model.get_tokenizer()

    sampling_params = SamplingParams(
        temperature=0.0, top_p=1, max_tokens=args.max_tokens,
        stop_token_ids=[tokenizer.eos_token_id,
                        tokenizer.convert_tokens_to_ids("<|eot_id|>")]
    )

    correct_count = 0
    inputs, correct_answers, predictions = [], [], []

    for batch in tqdm(dataloader):
        batch_inputs = batch["input"]
        batch_correct_answers = batch["target"]
        batch_prompts = batch["prompt"]

        batch_predictions = model.generate(
            batch_prompts, sampling_params, use_tqdm=False
        )
        text_predictions = []

        for prediction, correct_answer in zip(
                batch_predictions, batch_correct_answers):

            model_prediction = prediction.outputs[0].text.lower().strip()
            text_predictions.append(model_prediction)

            if exact_match(model_prediction, correct_answer,
                           multiple_answers=(args.dataset == "rosetta_stone")):
                correct_count += 1

        inputs.extend(batch_prompts)
        correct_answers.extend(batch_correct_answers)
        predictions.extend(text_predictions)

    accuracy = correct_count / dataset_length

    log_file = open("./logs/" + args.run_name + ".txt", "w")

    log_file.write(json.dumps(vars(args), indent=4, sort_keys=True))
    log_file.write("\nAccuracy: " + str(accuracy) + "\n")

    for input, correct_answer, prediction in zip(
            inputs, correct_answers, predictions):
        log_file.write(
            "\nInput: " + input + "\nPrediction: " + prediction
            + "\nCorrect Answer: " + correct_answer
            + "\nCounted?" + str(exact_match(prediction, correct_answer, multiple_answers=(args.dataset == "rosetta_stone")))
        )
