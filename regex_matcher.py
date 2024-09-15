# Regex Finder

import re
import csv

DATA_PATH = "sample_data.csv"
OUTPUT_PATH = "sample_output.csv"


def create_basic_mapping(filepath: str) -> dict:
    with open(filepath,"r",encoding="utf-8") as r:
        reader = csv.reader(r)
        return {row[2]:[row[2]] for row in reader}


def create_custom_mapping(filepath: str) -> dict:
    with open(filepath,"r",encoding="utf-8") as r:
        reader = csv.reader(r)
        data = {}
        for row in reader:
            if row[0] not in data:
                data[row[0]] = [row[1]]
            else:
                data[row[0]].append(row[1])
        
        return data

def merge_dicts(d1: dict, d2: dict) -> dict:
    keys = set(list(d1.keys()) + list(d2.keys()))
    return {key: d1.get(key, []) + d2.get(key, []) for key in keys}

def reverse_mapping(d: dict) -> dict:
    return {v: k for k, vs in d.items() for v in vs}

with open(DATA_PATH,"r",encoding="utf-8") as r:
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as w:
        data_1 = create_basic_mapping(DATA_PATH)
        data_2 = create_custom_mapping("mapping_data.csv")
        merged_data = merge_dicts(data_1, data_2)

        reversed_mapping = reverse_mapping(merged_data)
        reader = csv.reader(r)
        writer = csv.writer(w)

        print(reversed_mapping)
        
        # headers = next(reader)

        for row in reader:
            title = row[1].upper()

            data_to_write = [row[0], title]
            found = False

            for k,v in reversed_mapping.items():
                pattern = r"\b" + k + r"\b"
                pattern = rf'\b{re.escape(k)}\b'
                if re.search(pattern, title):
                    data_to_write.append(v)
                    found = True
                    break
            
            if not found:
                data_to_write.append("No Match")
            writer.writerow(data_to_write)



