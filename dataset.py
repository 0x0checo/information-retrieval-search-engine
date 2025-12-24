import os
import json
from collections import Counter

input_folder = "OG_json"
output_file = "clean_data.json"
all_data = []

# Loop over each file in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(input_folder, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file) # that file's list of dict objects
            for obj in data:
                all_data.append(obj) # add each object to master list


def delete_keys_from_dicts(dict_list):
    keys_to_delete = ["portal", "date_published", "portal2", "date_published2", "annotator", "annotation_id", "created_at", "updated_at", "lead_time"]

    for d in dict_list:
        for key in keys_to_delete:
            if key in d:
                del d[key]

    return dict_list

clean_data = delete_keys_from_dicts(all_data)

with open(output_file, "w", encoding="utf-8") as output:
    json.dump(clean_data, output, ensure_ascii=False, indent=2)


#Reachig for pairs of documents with similarity score 4 or 5
fours_fives = []

with open("clean_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

for obj in data:
    if (str(obj.get("choice")) == "5") or (str(obj.get("choice")) == "4"):
        fours_fives.append(obj)
       
with open("fours_fives.json", "w", encoding="utf-8") as output_file:
    json.dump(fours_fives, output_file, ensure_ascii=False, indent=2)


#Creating a seperate json file containing single articla as oposed to the one with pairs and similarity scores
def split_and_rename_dicts(dict_list):
    result = []
    seen_titles = set()

    for d in dict_list:
        key = "choice"
        if key in d:
            del d[key]

        # Create first dictionary with id, title, body
        dict1 = {
            "id": d["id"],
            "title": d["title"],
            "body": d["body"]
        }

        # Create second dictionary with id2, title2, body2 renamed to id, title, body
        dict2 = {
            "id": d["id2"],
            "title": d["title2"],
            "body": d["body2"]
        }

        # Add both dictionaries to the result list

        if dict1["title"] not in seen_titles:
            result.append(dict1)
            seen_titles.add(dict1["title"])

        if dict2["title"] not in seen_titles:
            result.append(dict2)
            seen_titles.add(dict2["title"])

    return result

Individual_data = split_and_rename_dicts(clean_data)

for i, article in enumerate(Individual_data):
    # Assign new ids starting from 1
    article['id'] = i + 1

with open("individual_data.json", "w", encoding="utf-8") as output:
    json.dump(Individual_data, output, ensure_ascii=False, indent=2)
