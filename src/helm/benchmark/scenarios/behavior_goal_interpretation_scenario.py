import csv
import os
import json
from typing import Dict, List

from .scenario import Scenario, Instance, Reference, TRAIN_SPLIT, VALID_SPLIT, TEST_SPLIT, CORRECT_TAG, Input, Output
from .grammar import read_grammar, generate_derivations, Derivation, get_values, get_tags
from helm.common.general import ensure_file_downloaded


class Behavior_Goal_Interpretation_Scenario(Scenario):
    """
    Scenario to evaluate LLM Goal Interpretation Ability in B-100
    """

    name = "Behavior_Goal_Interpretation"
    description = "Interpretation of Behavior-100 Task Goal Conditions from Natural Language form to Symbolic Form"
    tags = ["instructions"]

    def __init__(self):
        super().__init__()
        import vertexai
        vertexai.init()

    def download_data(self, path: str):
        ensure_file_downloaded(
            source_url="https://drive.google.com/uc?id=116q05b_obktK5hVg7YqBfM5USFGCKDqP",
            target_path=path,
            unpack=True,
            unpack_type="unzip",
        )

    def get_instances(self, output_path: str) -> List[Instance]:
        # Download the raw data
        data_path: str = os.path.join(output_path, "data")
        self.download_data(data_path)

        # Read all the instances
        instances: List[Instance] = []

        prompt_path = os.path.join(data_path, "llm_prompts.json")
        reference_path = os.path.join(data_path, "all_conditions.json")

        with open(prompt_path, "r") as json_file:
            demo_to_prompt = json.load(json_file)

        with open(reference_path, "r") as json_file:
            demo_to_conds = json.load(json_file)

        for key, value in demo_to_prompt.items():
            instance = Instance(
                input=Input(text=value),
                references=[Reference(Output(text=demo_to_conds[key]), tags=[CORRECT_TAG])],
                split=TEST_SPLIT,
            )
            instances.append(instance)

        return instances