import json


def write_result_into_file(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
