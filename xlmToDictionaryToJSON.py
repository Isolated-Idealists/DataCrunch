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
from tqdm import tqdm




text_file = open("common_words.txt", "r")
common_words = text_file.read().split('\n')
# print(common_words)





TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

directoryname = 'JSON_FILES'

fileData = []

directory = os.getcwd()
xlm_files = filename = os.path.join(directory, 'XLM_FILES_all.7z/XLM_FILES')


for x in progressbar(range(1, 41739)):

    # print(filename)
    filename = "file_" + str(x) + ".xml"
    # print(filename)
    file = os.path.join(xlm_files, filename)
    tree = ET.parse(file)
    tree = tree.getroot()
    dictionary = {}
    for child in tree:
        flag = True
        for child_of_root in child:

            if child_of_root.tag == 'content':
                # print(child_of_root.text)
                if child_of_root.text != None:

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

                # else:
                #     dictionary[child_of_root.tag] = ["None"]

            else:
                if child_of_root.tag == "transcript-id":
                    dictionary["transcriptId"] = child_of_root.text

                elif child_of_root.tag == "prime-minister":
                    dictionary["primeMinister"] = child_of_root.text
                elif child_of_root.tag == "period-of-service":
                    dictionary["periodOfService"] = child_of_root.text
                elif child_of_root.tag == "release-date":
                    dictionary["releaseDate"] = child_of_root.text
                elif child_of_root.tag == "release-type":
                    dictionary["releaseType"] = child_of_root.text
                else:

                    dictionary[child_of_root.tag] = child_of_root.text


    if dictionary:
        fileData.append(dictionary.copy())


filename = "test3.json"
filename = os.path.join(directoryname, filename)
with open(filename, 'w') as outfile:
    json.dump(fileData, outfile)

print(fileData)

