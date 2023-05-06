# Utility functions to read and write data to JSON database file

import json
from typing import Optional

def read(filename: Optional[str] = 'database.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def write(data: list, filename: Optional[str] = 'database.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def list_to_dict(data: list):
    print("hello")
    return {}

def dict_to_list(data: dict):
    print("hello")
    return []

