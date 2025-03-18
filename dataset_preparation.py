import random

import torch
from sentence_transformers import SentenceTransformer
from torch.nn.functional import cosine_similarity  # type: ignore

from cryptic_crosswords import CrypticCrosswords, CrypticCrosswordsTypes
from logic_puzzles import LogicPuzzles
from rosetta_stone import RosettaStone, RosettaStoneTypes


class BaseDataset():
    def __init__(self, dataset_name, prompt_name, similarity="random",
                 ranking="random", n_shots=0, random_seed=42):
        # options for the dataset_name are:
        # cryptic_crosswords, rosetta_stone, logic_puzzles
        self.dataset_name = dataset_name
        self.prompt_name = prompt_name

        self.similarity_functions = {
            "random": self.random_similarity,
            "semantic": self.semantic_similarity,
            "thematic": self.thematic_similarity
        }
        self.similarity = self.similarity_functions[similarity]

        self.ranking_functions = {
            "random": self.random_ranking,
            "semantic_top_to_bottom": self.semantic_ranking_top_to_bottom,
            "semantic_bottom_to_top": self.semantic_ranking_bottom_to_top,
        }
        self.ranking = self.ranking_functions[ranking]

        self.embeddings = None
        if similarity in ["semantic", "thematic"]:
            self.embeddings = self._get_embeddings()

        if self.similarity.__name__.startswith("thematic"):
            self.type_dict = {}
            for i, example in enumerate(self.dataset):
                type = example["type"]
                if type in self.type_dict:
                    self.type_dict[type].append(i)
                else:
                    self.type_dict[type] = [i]

        self.n_shots = n_shots
        random.seed(random_seed)

    def check_answer_against_correct(self, prediction, correct_answer):
        pass

    def _too_similar(self, example1, example2):
        pass

    def _get_embeddings(self):
        model = SentenceTransformer("all-MiniLM-L6-v2")

        clues = [example[self.embedding_field] for example in self.dataset]

        embeddings = model.encode(clues, convert_to_tensor=True)
        return embeddings

    def random_similarity(self, example, index=None):
        examples = []
        while len(examples) < self.n_shots:
            index = random.sample(range(len(self.dataset)), 1)[0]

            if not self._too_similar(self.dataset[index], example, examples):
                examples.append(self.dataset[index])

        return self._map_examples_to_dict(examples)

    def semantic_similarity(self, example, index):
        similarities = cosine_similarity(
            self.embeddings[index].reshape(1, -1), self.embeddings
        )

        indices = torch.argsort(similarities, descending=True)

        examples = []
        i = 0
        while len(examples) < self.n_shots:
            index = int(indices[i])
            if not self._too_similar(self.dataset[index], example, examples):
                examples.append(self.dataset[index])
            i += 1

        examples = self.ranking(examples)

        return self._map_examples_to_dict(examples)

    def thematic_similarity(self, example, index):
        similarities = cosine_similarity(
            self.embeddings[index].reshape(1, -1), self.embeddings
        )

        indices = torch.argsort(similarities, descending=True)

        # # filter indices by type
        device = indices.device
        valid_indices = torch.tensor(
            list(self.type_dict[example["type"]]), device=device
        )
        mask = torch.isin(indices, valid_indices)
        indices = indices[mask]

        # now we have examples of the same type sorted by semantic similarity
        # if we don't shuffle, examples list will be filled with most similar
        if self.ranking.__name__.startswith("random"):
            indices = self.ranking(indices)

        examples = []
        i = 0
        while len(examples) < self.n_shots and i < len(indices):
            index = int(indices[i])
            if not self._too_similar(self.dataset[index], example, examples):
                examples.append(self.dataset[index])
            i += 1

        examples = self.ranking(examples)

        return self._map_examples_to_dict(examples)

    def random_ranking(self, example_list):
        n = len(example_list)
        indexes = list(range(n))
        random.shuffle(indexes)

        permuted_list = [example_list[i] for i in indexes]
        return permuted_list

    def semantic_ranking_top_to_bottom(self, example_list):
        return example_list

    def semantic_ranking_bottom_to_top(self, example_list):
        return example_list[::-1]

    def generate_prompt(self, example, prompt_name, similarity):
        pass


def get_dataset_with_prompts(dataset_name, prompt_name="base",
                             similarity="random", ranking="random", n_shots=0,
                             random_seed=42):
    datasets = {
        "cryptic_crosswords": CrypticCrosswords,
        "cryptic_crosswords_types": CrypticCrosswordsTypes,
        "rosetta_stone": RosettaStone,
        "rosetta_stone_types": RosettaStoneTypes, "logic_puzzles": LogicPuzzles
    }

    wrapped_dataset = datasets[dataset_name](
        prompt_name, similarity, ranking, n_shots, random_seed
    )

    return wrapped_dataset

