import json

def load_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def save_json(path, json_dat):
    with open(path, 'w') as file:
        json.dump(json_dat, file, indent = 6)