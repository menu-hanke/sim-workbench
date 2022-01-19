import json
from typing import Tuple, List
from sim.ForestDataModels import ForestStand, ReferenceTree


def read_forest_json(json_file: str) -> List[ForestStand]:
    with open(json_file, 'r') as f:
        return json.loads(f.read(), object_hook=lambda d: ReferenceTree(**d) if "tree" in d['identifier'] else ForestStand(**d))