import os
import json
from extract import extract_account
from generate_agent import generate_agent_spec
from apply_patch import apply_patch
from diff import generate_diff

DATASET_DEMO = "dataset/demo"
DATASET_ONBOARD = "dataset/onboarding"
OUTPUT_DIR = "outputs/accounts"

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def process_demo(file):
    transcript = read_file(os.path.join(DATASET_DEMO, file))
    account_id = file.replace(".txt", "")
    account_dir = os.path.join(OUTPUT_DIR, account_id, "v1")
    os.makedirs(account_dir, exist_ok=True)

    memo = extract_account(transcript, account_id)
    agent = generate_agent_spec(memo, "v1")

    save_json(os.path.join(account_dir, "account_memo.json"), memo)
    save_json(os.path.join(account_dir, "agent_spec.json"), agent)

def process_onboarding(file):
    transcript = read_file(os.path.join(DATASET_ONBOARD, file))
    account_id = file.replace(".txt", "")

    v1_path = os.path.join(OUTPUT_DIR, account_id, "v1", "account_memo.json")
    with open(v1_path) as f:
        v1_data = json.load(f)

    onboarding_data = extract_account(transcript, account_id)
    updated = apply_patch(v1_data, onboarding_data)

    account_dir = os.path.join(OUTPUT_DIR, account_id, "v2")
    os.makedirs(account_dir, exist_ok=True)

    agent_v2 = generate_agent_spec(updated, "v2")

    save_json(os.path.join(account_dir, "account_memo.json"), updated)
    save_json(os.path.join(account_dir, "agent_spec.json"), agent_v2)

    changes = generate_diff(v1_data, updated)
    save_json(os.path.join(OUTPUT_DIR, account_id, "changes.json"), changes)

if __name__ == "__main__":
    for file in os.listdir(DATASET_DEMO):
        process_demo(file)

    for file in os.listdir(DATASET_ONBOARD):
        process_onboarding(file)

    print("Pipeline completed.")