import re

def safe_search(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None

def extract_business_hours(text):
    text_lower = text.lower()
    days = None
    hours = None
    timezone = None

    if "monday" in text_lower and "friday" in text_lower:
        days = "Monday to Friday"
    if "8:00" in text_lower or "8 am" in text_lower:
        hours = "8:00 AM - 5:00 PM"
    
    if "est" in text_lower:
        timezone = "EST"
    elif "cst" in text_lower:
        timezone = "CST"
    elif "pst" in text_lower:
        timezone = "PST"

    return {"days": days, "hours": hours, "timezone": timezone}

def extract_services(text):
    text_lower = text.lower()
    service_keywords = {
        "electrical": "electrical",
        "electrician": "electrical",
        "hvac": "hvac",
        "sprinkler": "sprinkler systems",
        "fire alarm": "fire alarm systems",
        "inspection": "inspection services",
        "service call": "service calls"
    }
    services = []
    for keyword, label in service_keywords.items():
        if keyword in text_lower:
            services.append(label)
    return list(set(services))

def extract_emergency_definition(text):
    text_lower = text.lower()
    emergencies = []
    if "fire alarm" in text_lower:
        emergencies.append("fire alarm trigger")
    if "sprinkler leak" in text_lower:
        emergencies.append("sprinkler leak")
    if "gas station" in text_lower:
        emergencies.append("gas station service emergency")
    if "emergency call" in text_lower or "emergency service" in text_lower:
        emergencies.append("general emergency call")
    return list(set(emergencies))

def extract_transfer_rules(text):
    text_lower = text.lower()
    if "transfer" in text_lower:
        return "Caller can be transferred to the business owner if requested"
    if "forward" in text_lower or "forwarding" in text_lower:
        return "Calls are forwarded from business line to the AI agent"
    if "decline or don't answer" in text_lower:
        return "Agent answers calls when owner declines or misses calls"
    return None

def extract_emergency_routing_rules(text):
    text_lower = text.lower()
    if "dispatch" in text_lower:
        return "Route to dispatch immediately."
    if "call owner" in text_lower or "call me" in text_lower:
        return "Route to business owner's mobile."
    if "phone tree" in text_lower:
        return "Route to emergency phone tree."
    return None

def extract_non_emergency_routing_rules(text):
    text_lower = text.lower()
    if "voicemail" in text_lower:
        return "Send to voicemail."
    if "next day" in text_lower or "next business day" in text_lower:
        return "Collect details for next business day follow-up."
    return None

def extract_integration_constraints(text):
    text_lower = text.lower()
    if "servicetrade" in text_lower:
        return "Do not create certain jobs in ServiceTrade automatically."
    if "housecall pro" in text_lower:
        return "Log call in Housecall Pro."
    return None

def extract_questions_or_unknowns(data):
    questions = []
    if not data["company_name"]:
        questions.append("Company name not clearly identified")
    if not data["business_hours"]["hours"]:
        questions.append("Exact business hours not confirmed")
    if not data["services_supported"]:
        questions.append("Services supported not clearly mentioned")
    if not data["emergency_definition"]:
        questions.append("Emergency definition not clearly specified")
    if not data["call_transfer_rules"]:
        questions.append("Call transfer behavior not clearly defined")
    if not data["integration_constraints"]:
        questions.append("Integration constraints not mentioned")
    return questions

def extract_account(transcript, account_id):
    data = {
        "account_id": account_id,
        "company_name": safe_search(
            r"([A-Z][a-zA-Z]+(?:'s)?\s(?:Electric|Electrical|HVAC|Fire|Alarm|Solutions|Services))",
            transcript
        ),
        "business_hours": extract_business_hours(transcript),
        "office_address": None,
        "services_supported": extract_services(transcript),
        "emergency_definition": extract_emergency_definition(transcript),
        "emergency_routing_rules": extract_emergency_routing_rules(transcript),
        "non_emergency_routing_rules": extract_non_emergency_routing_rules(transcript),
        "call_transfer_rules": extract_transfer_rules(transcript),
        "integration_constraints": extract_integration_constraints(transcript),
        "after_hours_flow_summary": None,
        "office_hours_flow_summary": None,
        "questions_or_unknowns": [],
        "notes": "Extracted from transcript using rule-based extraction."
    }
    
    data["questions_or_unknowns"] = extract_questions_or_unknowns(data)
    return data