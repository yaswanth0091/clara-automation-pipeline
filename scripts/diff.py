from deepdiff import DeepDiff
import json

def generate_diff(old, new):
    diff = DeepDiff(old, new, ignore_order=True)
    return json.loads(diff.to_json())