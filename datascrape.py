import xml.etree.ElementTree as ET
import requests
import pandas as pd
import re
import json

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
tag_1 = []
frames = []
tag = []
CSV_NAME = 'test.csv'


TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

for x in range(1, 10):
    URL = 'https://pmtranscripts.pmc.gov.au/query?transcript=' + str(x)
    tree = ET.fromstring(requests.get(URL).text)

    for child in tree:

        tag_1.sort()
        tag.sort()

        if tag != tag_1:
            print("PROBLEM, DATA IS INCONSISTENT")
            print(tag_1)
            print(tag)

        tag = []
        text = []
        for child_of_root in child:
            tag.append(child_of_root.tag)
            tag_1 = tag
            if child_of_root.tag == 'content':
                text_clean = remove_tags(child_of_root.text).strip()
                text_clean = text_clean.replace('\n', ' ').replace('\r', '')
                text.append(text_clean)
            else:
                text.append(child_of_root.text)
            # print (child_of_root.tag, child_of_root.text)

        df = pd.DataFrame(columns=tag)
        df.loc[0] = text
        frames.append(df)

final = pd.concat(frames)
final.reset_index(drop=True, inplace=True)
# new_f = final.replace('\n',' ')
# for index, row in final.iterrows:
#     print(type(x))
#     print(x)
#     final.replace(x, x.replace('\n', ' ').replace('\r', ''))

# print(final['content'])

# final.to_csv(CSV_NAME)
print(final)
final.set_index('transcript-id', inplace=True)
print(final)



final.to_json (r'C:\Users\mklocker\PycharmProjects\govHack2020\Export_DataFrame.json')


with open('Export_DataFrame.json', 'r') as json_file:
    json_object = json.load(json_file)
    print(json.dumps(json_object, indent=1))
