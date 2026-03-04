import json

def apply_patch(v1_data, onboarding_data):
    updated = v1_data.copy()

    for key, value in onboarding_data.items():
        if value and value != v1_data.get(key):
            updated[key] = value

    return updated