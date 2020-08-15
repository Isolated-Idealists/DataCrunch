import xml.etree.ElementTree as ET
import requests
import pandas as pd
import re
import json
import os
from progressbar import progressbar


TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

directoryname = 'JSON_FILES'
os.mkdir(directoryname)

for x in range(41735, 41741):
    URL = 'https://pmtranscripts.pmc.gov.au/query?transcript=' + str(x)
    tree = ET.fromstring(requests.get(URL).text)
    dictionary = {}
    for child in tree:

        for child_of_root in child:

            if child_of_root.tag == 'content':
                text_clean = remove_tags(child_of_root.text).strip()
                text_clean = text_clean.replace('\n', ' ').replace('\r', '')
                dictionary[child_of_root.tag] = text_clean
            else:
                dictionary[child_of_root.tag] = child_of_root.text

    print(dictionary)
    filename = "JSON_TRANSCRIPT_" + str(x)
    filename = os.path.join(directoryname, filename)
    with open(filename, 'w') as outfile:
        json.dump(dictionary, outfile)