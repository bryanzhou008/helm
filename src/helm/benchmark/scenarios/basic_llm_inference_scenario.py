import csv
import os
import json
from typing import Dict, List
from PIL import Image

from .scenario import Scenario, Instance, Reference, TRAIN_SPLIT, VALID_SPLIT, TEST_SPLIT, CORRECT_TAG, Input, Output
from .grammar import read_grammar, generate_derivations, Derivation, get_values, get_tags
from helm.common.general import ensure_file_downloaded
from helm.common.media_object import MediaObject, MultimediaObject


class Basic_LLM_Inference_Scenario(Scenario):
    """
    Basic_LLM_Inference
    """

    name = "Basic_LLM_Inference"
    description = "Basic_LLM_Inference"
    tags = ["instructions"]

    def __init__(self, simulator: str, subtask: str):
        super().__init__()
        self.simulator = simulator
        self.subtask = subtask

    def download_data(self, path: str):
        ensure_file_downloaded(
            source_url="https://drive.google.com/uc?id=116q05b_obktK5hVg7YqBfM5USFGCKDqP",
            target_path=path,
            unpack=True,
            unpack_type="unzip",
        )

    def get_instances(self, output_path: str) -> List[Instance]:
        # Download the raw data
        data_path: str = "HELM_input"
        self.download_data(data_path)

        # Read all the instances
        instances: List[Instance] = []

        user_prompt_path = os.path.join(data_path, self.simulator, self.subtask, "user_prompts.json")
        
        with open(user_prompt_path, "r") as json_file:
            user_prompts = json.load(json_file)
        
        # include the index here for debugging purposes
        for index, (key, value) in enumerate(user_prompts.items()):
            instance = Instance(
                id = value["identifier"],
                input=Input(text=value["llm_prompt"]),
                references=[Reference(Output(text="place holder reference text"), tags=[CORRECT_TAG])],
                split=TEST_SPLIT,
            )
            instances.append(instance)

        return instances