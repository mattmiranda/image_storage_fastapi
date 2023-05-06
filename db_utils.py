# Utility functions to read and write data to JSON database file

import json
from typing import Optional

def read(filename: Optional[str] = 'database.json') -> list:
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def write(data: list, filename: Optional[str] = 'database.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_image(data: dict):
    images_list = read()
    images_list.append(data)
    write(images_list)

def remove_image(image_id: str):
    images = list_to_dict(read())
    image = images.pop(image_id)
    write(dict_to_list(images))
    return image

def list_to_dict(data: list):
    d = {}
    for item in data:
        d[item['_id']] = item
    return d

def dict_to_list(data: dict):
    l = []
    for item in data.values():
        l.append(item)
    return l
