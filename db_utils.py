# Utility functions to read and write data to JSON database file

import json

def db_read(data: dict):
    #??
    return []

def db_write(data: dict):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def list_to_dict(data: list):
    print("hello")
    return {}

def dict_to_list(data: dict):
    print("hello")
    return []

