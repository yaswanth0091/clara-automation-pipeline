import copy

def apply_patch(v1_data, onboarding_data):
    # Deepcopy to avoid mutating the original v1 dictionary
    updated = copy.deepcopy(v1_data)

    def dict_merge(base, update):
        for key, value in update.items():
            # If both are dictionaries, recurse (fixes the business_hours bug)
            if isinstance(value, dict) and isinstance(base.get(key), dict):
                dict_merge(base[key], value)
            # If the value is a list and it's empty, ignore it (assumes onboarding didn't mention it)
            elif isinstance(value, list) and not value:
                continue
            # Otherwise, if we have a valid extracted value, apply the update
            elif value is not None:
                base[key] = value
        return base

    return dict_merge(updated, onboarding_data)