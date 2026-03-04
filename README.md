# Clara Answers – Automation Pipeline Assignment

## 1. Overview
This project implements an automation pipeline that converts customer call transcripts into structured AI voice agent configurations. The system simulates Clara’s real onboarding workflow:

1. **Demo Call:** Provides high-level information about the customer’s business.
2. **v1 Configuration:** The system generates a preliminary AI agent configuration.
3. **Onboarding:** Additional operational details are captured.
4. **v2 Configuration:** The pipeline updates the configuration and generates a change log.

The goal is to transform **unstructured conversation** → **structured operational rules** → **deployable AI agent configuration**. This pipeline operates fully locally using rule-based extraction to satisfy zero-cost constraints.

---

## 2. Architecture

### Pipeline Flow
`Demo Transcript` ➔ `Rule-Based Extraction` ➔ `Account Memo (JSON)` ➔ `Agent Prompt Generator` ➔ `Retell Agent Draft Spec (v1)`

### Data Flow
```text
dataset/demo/*.txt
dataset/onboarding/*.txt
        ↓
run_pipeline.py
        ↓
scripts/
   ├── extract.py
   ├── generate_agent.py
   ├── apply_patch.py
   └── diff.py
        ↓
outputs/accounts/<account_id>/
