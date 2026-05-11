import json
import os


def load_golden_dataset(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..", "data", "golden_dataset.json")
    with open(path) as f:
        return json.load(f)
