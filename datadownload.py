import xml.etree.ElementTree as ET
import requests
import pandas as pd
import re
import json
from progressbar import progressbar


for x in progressbar(range(1, 41741)):
    URL = 'https://pmtranscripts.pmc.gov.au/query?transcript=' + str(x)
    tree = ET.fromstring(requests.get(URL).text)