# standard library
import json
import math

def load_json(file_name):
    with open(file_name) as data:
        return json.load(data)

#TODO Make arbitrary
def first_index_not_all_nan(first_list, second_list):
    start_idx = 0
    for index, (first, second) in enumerate(zip(first_list, second_list)):
        if not math.isnan(first) and not math.isnan(second):
            start_idx = index
            break
        
    return start_idx

