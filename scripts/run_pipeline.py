import os
import json
import csv
from datetime import datetime
from extract import extract_account
from generate_agent import generate_agent_spec
from apply_patch import apply_patch
from diff import generate_diff

DATASET_DEMO = "dataset/demo"
DATASET_ONBOARD = "dataset/onboarding"
OUTPUT_DIR = "outputs/accounts"
TASKS_FILE = "outputs/tasks.csv"

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def create_task_ticket(account_id, stage, status):
    """Mocks a task tracker (like Asana) using a local CSV file."""
    os.makedirs("outputs", exist_ok=True)
    file_exists = os.path.isfile(TASKS_FILE)
    
    with open(TASKS_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Account ID", "Stage", "Status", "Timestamp"])
        writer.writerow([account_id, stage, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def process_demo(file):
    transcript = read_file(os.path.join(DATASET_DEMO, file))
    account_id = file.replace(".txt", "")
    account_dir = os.path.join(OUTPUT_DIR, account_id, "v1")
    os.makedirs(account_dir, exist_ok=True)

    memo = extract_account(transcript, account_id)
    agent = generate_agent_spec(memo, "v1")

    save_json(os.path.join(account_dir, "account_memo.json"), memo)
    save_json(os.path.join(account_dir, "agent_spec.json"), agent)
    
    create_task_ticket(account_id, "Pipeline A (Demo)", "Completed")

def process_onboarding(file):
    transcript = read_file(os.path.join(DATASET_ONBOARD, file))
    account_id = file.replace(".txt", "")

    v1_path = os.path.join(OUTPUT_DIR, account_id, "v1", "account_memo.json")
    
    # Graceful error handling if v1 doesn't exist yet
    if not os.path.exists(v1_path):
        print(f"Skipping {account_id} onboarding: v1 memo not found.")
        return

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
    
    create_task_ticket(account_id, "Pipeline B (Onboarding)", "Completed")

if __name__ == "__main__":
    # Process Demos first
    if os.path.exists(DATASET_DEMO):
        for file in os.listdir(DATASET_DEMO):
            if file.endswith(".txt"):
                process_demo(file)
    else:
        print(f"Directory not found: {DATASET_DEMO}")

    # Process Onboarding second
    if os.path.exists(DATASET_ONBOARD):
        for file in os.listdir(DATASET_ONBOARD):
            if file.endswith(".txt"):
                process_onboarding(file)
    else:
        print(f"Directory not found: {DATASET_ONBOARD}")

    print("Pipeline completed. Check /outputs for results and tasks.csv.")