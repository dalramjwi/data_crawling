import os
import json

def save_json_file(folder, file_name, data):
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(folder, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return file_path
