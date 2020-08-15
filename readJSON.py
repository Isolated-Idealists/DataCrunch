import json

with open('JSON_TRANSCRIPT_1', 'r') as json_file:
    json_object = json.load(json_file)
    print(json.dumps(json_object, indent=1))
