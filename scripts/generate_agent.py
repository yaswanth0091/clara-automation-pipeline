import json

def generate_agent_spec(account_data, version="v1"):
    business_hours = account_data["business_hours"]["hours"]
    timezone = account_data["business_hours"]["timezone"]
    
    # Format lists into readable strings
    emergencies = ", ".join(account_data.get("emergency_definition", [])) or "Not specified"
    transfer_rules = account_data.get("call_transfer_rules") or "Not specified"
    
    system_prompt = f"""
You are Clara, the AI answering agent.

BUSINESS HOURS FLOW:
1. Greet caller.
2. Ask purpose.
3. Collect name and phone number.
4. Route call appropriately.
5. If transfer fails, apologize and assure callback.
6. Ask if anything else is needed.
7. Close politely.

AFTER HOURS FLOW:
1. Greet caller.
2. Ask purpose.
3. Confirm emergency.
4. If emergency: collect name, phone, address immediately.
5. Attempt transfer.
6. If transfer fails: assure rapid follow-up.
7. If non-emergency: collect details and confirm follow-up next business day.
8. Ask if anything else is needed.
9. Close politely.

ACCOUNT SPECIFICS:
Business hours: {business_hours}
Timezone: {timezone}
Emergency Definition: {emergencies}
Call transfer rules: {transfer_rules}
Fallback protocol: If transfer fails, apologize and confirm callback.

Never mention internal tools.
Ask only necessary routing questions.
"""

    return {
        "agent_name": f"{account_data['company_name']}_agent",
        "voice_style": "professional, calm, concise",
        "system_prompt": system_prompt.strip(),
        "version": version
    }