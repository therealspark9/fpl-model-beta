import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

url = 'https://understat.com/league/EPL/2025' # Adjust league and season as needed

res = requests.get(url)
soup = BeautifulSoup(res.content, 'lxml')

#fetch team data for all teams from url
scripts = soup.find_all('script')
string_with_json_obj = ''
for script in scripts:
    if 'teamsData' in script.text:
        string_with_json_obj = script.text.strip()
        break

# Correct extraction and decoding of JSON string
start = string_with_json_obj.index("JSON.parse('") + len("JSON.parse('")
end = string_with_json_obj.index("')", start)
json_data = string_with_json_obj[start:end]
json_data = json_data.encode('utf8').decode('unicode_escape')
data = json.loads(json_data)
team_data_list = []

#print league table for all teams
for team_id, team_info in data.items():
    team_title = team_info['title']  # Get team name
    for season_stats in team_info['history']:
        print(season_stats)  # Print all columns of season_stats
        season_stats['team_title'] = team_title  # Add team name to stats
        # Ensure 'goals' key exists
        season_stats['goals'] = season_stats.get('goals', 0)
        team_data_list.append(season_stats)

df = pd.DataFrame(team_data_list)

#print dataframe
print(df)