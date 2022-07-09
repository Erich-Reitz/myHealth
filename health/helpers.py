# standard library
import json


def load_json(file_name):
    with open(file_name) as data:
        return json.load(data)
