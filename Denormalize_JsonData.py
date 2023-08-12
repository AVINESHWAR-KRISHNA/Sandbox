import pandas as pd
DATA = ''

def normalize_data(data):
    normalized_data = []

    for item in data:
        row = {}

        for key, value in item.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    row[f"{key}_{sub_key}"] = sub_value
            elif isinstance(value, list):
                for idx, sub_item in enumerate(value, start=1):
                    if isinstance(sub_item, dict):
                        for sub_key, sub_value in sub_item.items():
                            if isinstance(sub_value, dict):
                                for sub_sub_key, sub_sub_value in sub_value.items():
                                    row[f"{key}_{idx}_{sub_key}_{sub_sub_key}"] = sub_sub_value
                            else:
                                row[f"{key}_{idx}_{sub_key}"] = sub_value
                    else:
                        row[f"{key}_{idx}"] = sub_item
            else:
                row[key] = value

        normalized_data.append(row)

    return normalized_data
	
normalized_data = normalize_data(DATA)

DFF = pd.DataFrame(normalized_data)

print(DFF)