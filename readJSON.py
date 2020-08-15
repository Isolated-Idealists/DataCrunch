import json

with open('basicScrape.json', 'r') as json_file:
    json_object = json.load(json_file)
    print(json.dumps(json_object, indent=1))
