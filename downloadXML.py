import xml.etree.ElementTree as ET
import requests
import pandas as pd
import re
import json
import os
from progressbar import progressbar

directoryname = 'XLM_FILES'
os.mkdir(directoryname)

for x in progressbar(range(1, 41740)):
    URL = 'https://pmtranscripts.pmc.gov.au/query?transcript=' + str(x)
    tree = ET.fromstring(requests.get(URL).text)
    tree = ET.ElementTree(tree)
    tree.write(directoryname + "/file_" + str(x) + ".xml")