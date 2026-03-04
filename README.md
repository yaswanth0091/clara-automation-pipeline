# Clara Answers – Zero-Cost Automation Pipeline

## Overview

This project implements an automation pipeline that converts **customer demo and onboarding calls into structured AI voice agent configurations**.

The system simulates the real workflow used by Clara Answers:

1. A **demo call** introduces the client’s business and high-level requirements.
2. The system generates a **preliminary Retell AI agent configuration (v1)**.
3. During **onboarding**, operational details are confirmed.
4. The system updates the configuration to **v2** and produces a **change log**.
## Pipeline Flow

The pipeline transforms:

**Conversation → Structured Account Memo → AI Agent Configuration → Version Update → Change Log**

The system runs entirely locally using **rule-based extraction** and satisfies the assignment's **zero-cost constraint**.

## Architecture

### Demo Pipeline (Pipeline A)

```
Demo Transcript
      ↓
Rule-Based Extraction
      ↓
Account Memo JSON
      ↓
Agent Spec Generator
      ↓
Retell Agent Draft Spec (v1)
      ↓
Stored in outputs/accounts/<account_id>/v1
```

### Onboarding Pipeline (Pipeline B)

```
Onboarding Transcript
        ↓
Rule-Based Extraction
        ↓
Patch Existing Memo (v1 → v2)
        ↓
Generate Updated Agent Spec
        ↓
Compute Version Diff
        ↓
Store v2 + changelog
```

### Data Flow

```
dataset/demo/*.txt
dataset/onboarding/*.txt
        ↓
run_pipeline.py
        ↓
scripts/
   extract.py
   generate_agent.py
   apply_patch.py
   diff.py
        ↓
outputs/accounts/<account_id>/
```

## Setup

### 1. Clone the Repository

```bash
git clone <repo_url>
cd clara-automation-pipeline
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

**Activate environment:**

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies used:**
- **DeepDiff** – for version diff tracking
- **python-dateutil**

### 4. Prepare Dataset

Place transcripts inside:
- `dataset/demo/`
- `dataset/onboarding/`

**Example:**
```
dataset/demo/bens_electric.txt
dataset/onboarding/bens_electric.txt
```

- **Demo transcripts** represent exploratory conversations.
- **Onboarding transcripts** represent confirmed operational rules.
- **Transcripts** are used instead of audio to maintain the zero-cost requirement and avoid paid speech-to-text services.

### 5. Run the Pipeline

```bash
python scripts/run_pipeline.py
```

The system automatically processes all transcript pairs.

## Where Outputs Go

Outputs are generated under:

```
outputs/accounts/<account_id>/
```

**Example structure:**

```
outputs/accounts/bens_electric/

v1/
   account_memo.json
   agent_spec.json

v2/
   account_memo.json
   agent_spec.json

changes.json
```

Additionally, a task tracker file is generated:

```
outputs/tasks.csv
```

This simulates a **task management system** such as Asana.

## Output File Explanation

### account_memo.json

Structured operational rules extracted from transcripts.

**Example fields:**
- `account_id`
- `company_name`
- `business_hours`
- `services_supported`
- `emergency_definition`
- `call_transfer_rules`
- `questions_or_unknowns`

The system **avoids hallucinating missing information**.

### agent_spec.json

Draft configuration for a voice AI agent.

**Contains:**
- `agent_name`
- `voice_style`
- `system_prompt`
- `call_transfer_protocol`
- `fallback_protocol`
- `version`

This file represents the **Retell agent configuration**.

### changes.json

Tracks configuration changes between v1 and v2.

**Example:**

```json
{
  "values_changed": {
    "root['business_hours']['hours']": {
      "old_value": null,
      "new_value": "8:00 AM - 5:00 PM"
    }
  }
}
```

## Versioning Logic

### v1 – Demo Configuration

Generated from demo calls.

**Characteristics:**
- Exploratory
- Incomplete information
- Missing data flagged

**Example:**

```json
"business_hours": null,
"questions_or_unknowns": [
   "Business hours not confirmed"
]
```

### v2 – Onboarding Configuration

Generated after onboarding calls.

**Characteristics:**
- Confirmed business rules
- Operational configuration
- Refined agent behavior

**Example:**

```json
"business_hours": {
   "days": "Monday to Friday",
   "hours": "8:00 AM - 5:00 PM"
}
```

## Patch Update Logic

The onboarding pipeline updates existing configuration using a **recursive merge strategy**.

This ensures onboarding updates do not overwrite unrelated v1 fields.

**Example:**

```
v1:
  business_hours:
    days: Monday-Friday
    timezone: EST

onboarding update:
  hours: 8-5

v2 result:
  days: Monday-Friday
  hours: 8-5
  timezone: EST
```

## Diff Logic

Configuration differences are detected using **DeepDiff**.

The system compares:
- `v1 account_memo.json`
- `v2 account_memo.json`

**Example diff:**
- `business_hours.days`
- `business_hours.hours`
- `services_supported`

This creates a **clear configuration change history**.

## Task Tracking

The assignment requires creating a task item for onboarding progress.

Instead of paid tools like Asana, this pipeline creates a local task tracker:

```
outputs/tasks.csv
```

**Example:**

```
Account ID      | Stage                      | Status      | Timestamp
bens_electric   | Pipeline A (Demo)          | Completed   | 2026-03-05
bens_electric   | Pipeline B (Onboarding)    | Completed   | 2026-03-05
```

This satisfies the task tracker requirement using a **zero-cost approach**.

## Retell Agent Setup

The pipeline generates a **Retell Agent Draft Specification**.

**File location:**

```
outputs/accounts/<account_id>/v2/agent_spec.json
```

### To Create the Retell AI Voice Agent:

1. Create a Retell account.
2. Create a new voice agent.
3. Open the generated file: `outputs/accounts/<account_id>/v2/agent_spec.json`
4. Copy the `system_prompt` from this file.
5. Select Single Prompt Agent in Retell AI
6. Paste it into the Retell agent configuration.
7. Configure call transfer and fallback rules according to the generated specification.



This step is **manual** because the Retell free tier does not allow automated API provisioning.

## Idempotency

The pipeline is designed to be **idempotent**.

Running the pipeline multiple times:
- Does not duplicate accounts
- Overwrites existing outputs safely
- Maintains consistent version structure

## Limitations

Current implementation has some limitations:

- **Rule-based extraction** may miss information if phrasing changes
- **Transcripts** must be manually prepared
- **Emergency routing logic** is simplified
- **Integration constraints detection** is basic
- **Agent deployment** to Retell is manual

These tradeoffs were made to maintain **zero-cost execution**.

## Production Improvements

In a production system, the following improvements would be implemented.

### LLM-Based Extraction

Replace rule-based parsing with LLM extraction for:
- Routing rules
- Escalation logic
- Integration constraints

### Automatic Transcription

Use open-source speech-to-text such as:
- **Whisper**

to process raw audio recordings.

### Database Storage

Replace JSON files with structured storage such as:
- **PostgreSQL**
- **Supabase**

for multi-account scaling.

### Workflow Orchestration

Use tools like **n8n** to automate ingestion and agent configuration updates.

### Retell API Integration

Push agent configurations directly to Retell using their API.

### UI Dashboard

Add a dashboard to visualize:
- Account configuration
- Version history
- Configuration diff

## Summary

This project demonstrates how **unstructured conversations can be converted into structured AI voice agent configurations** using an automated pipeline.

The system emphasizes:
- **Reliable automation**
- **Version-controlled configuration**
- **Safe data extraction**
- **Reproducibility**
- **Zero-cost operation**

The pipeline models how **Clara Answers** can scale onboarding automation for multiple service-trade businesses.

