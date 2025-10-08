import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re

# Entering the league's link
link = "https://understat.com/league/EPL"
res = requests.get(link)
soup = BeautifulSoup(res.content,'lxml')
scripts = soup.find_all('script')

# Get the table 
strings = scripts[2].string 

# Getting rid of unnecessary characters from json data
ind_start = strings.index("('")+2 
ind_end = strings.index("')") 
json_data = strings[ind_start:ind_end] 
json_data = json_data.encode('utf8').decode('unicode_escape')
data = json.loads(json_data)


df = pd.DataFrame(data.values())
df = df.explode("history")
h = df.pop("history")
df = pd.concat([df.reset_index(drop=True), pd.DataFrame(h.tolist())], axis=1)
df = df.infer_objects()

#table = df.groupby(['title']).agg({'wins': 'sum', 'draws': 'sum', 'loses': 'sum', 'scored': 'sum', 'missed': 'sum', 'pts': 'sum', 'xG': 'sum', 'xGA': 'sum', 'xpts': 'sum', 'npxG': 'sum', 'npxGA': 'sum', 'deep': 'sum', 'deep_allowed': 'sum'}).reset_index()
table = df.groupby(['title']).agg({'wins': 'sum', 'draws': 'sum', 'loses': 'sum', 'scored': 'sum', 'missed': 'sum', 'pts': 'sum', 'xG': 'sum', 'xGA': 'sum', 'xpts': 'sum', 'npxG': 'sum', 'npxGA': 'sum'}).reset_index()
print(table)