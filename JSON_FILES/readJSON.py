import json

with open('test.json', 'r') as json_file:
    json_object = json.load(json_file)
    print(json.dumps(json_object, indent=1))
