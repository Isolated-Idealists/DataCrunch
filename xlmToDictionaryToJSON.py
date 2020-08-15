import xml.etree.ElementTree as ET
import requests
import pandas as pd
import re
import json
import os
from progressbar import progressbar
import boto3
from collections import Counter
from rake_nltk import Rake, Metric

REGION = 'ap-southeast-2'


text_file = open("common_words.txt", "r")
common_words = text_file.read().split('\n')
# print(common_words)

def detect_key_phraes(text, language_code):
    comprehend = boto3.client('comprehend', region_name=REGION)
    response = comprehend.detect_key_phrases(Text=text, LanguageCode=language_code)
    return response


def utf8len(s):
    return len(s.encode('utf-8'))

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

directoryname = 'JSON_FILES'

fileData = []

for x in progressbar(range(41731, 41741)):
    URL = 'https://pmtranscripts.pmc.gov.au/query?transcript=' + str(x)
    tree = ET.fromstring(requests.get(URL).text)
    dictionary = {}
    flag = True
    for child in tree:

        for child_of_root in child:

            if child_of_root.tag == 'content':
                text_clean = remove_tags(child_of_root.text).strip()
                text_clean = text_clean.replace('\n', ' ').replace('\r', '').replace('\u2019', '')
                r = Rake(stopwords=common_words, ranking_metric=Metric.WORD_FREQUENCY, punctuations=[",", "-", ".", "'", ":", "?", "$", '"'])
                r.extract_keywords_from_text(text_clean)
                result = r.get_ranked_phrases_with_scores()
                final = result[:20]
                content_dictionary = []
                for i, content in enumerate(final):
                    content_dictionary.append({"weight" : content[0], "content" : content[1]})

                dictionary[child_of_root.tag] = content_dictionary
            else:
                dictionary[child_of_root.tag] = child_of_root.text

    fileData.append(dictionary.copy())


filename = "test.json"
filename = os.path.join(directoryname, filename)
with open(filename, 'w') as outfile:
    json.dump(fileData, outfile)

print(fileData)

