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

# Get the players stats 
strings = scripts[3].string 

# Getting rid of unnecessary characters from json data
ind_start = strings.index("('")+2 
ind_end = strings.index("')") 
json_data = strings[ind_start:ind_end] 
json_data = json_data.encode('utf8').decode('unicode_escape')
data = json.loads(json_data)

# Creating the dataframe
df = pd.DataFrame(data)

#columns are id player_name games time goals xG assists xA shots key_passes yellow_cards red_cards position team_title npg npxG xGChain xGBuildup
#remove id, games, yellow_cards, red_cards, position, npxG, xGChain and xGBuildup columns from df
df = df.drop(columns=['id', 'games', 'yellow_cards', 'red_cards', 'position', 'npxG', 'xGChain', 'xGBuildup'])

# Convert xG and xA to numeric before merging
df['xG'] = pd.to_numeric(df['xG'], errors='coerce')
df['xA'] = pd.to_numeric(df['xA'], errors='coerce')
df['xGI'] = df['xG'] + df['xA']
df['xGI'] = df['xGI'].round(2)
df = df.drop(columns=['xG', 'xA'])

# Convert goals and assists to numeric before merging
df['goals'] = pd.to_numeric(df['goals'], errors='coerce')
df['assists'] = pd.to_numeric(df['assists'], errors='coerce')
df['GI'] = df['goals'] + df['assists']
df = df.drop(columns=['goals', 'assists'])

#sort df by GI column in descending order
df = df.sort_values(by=['GI'], ascending=False)

print(df.head(25))