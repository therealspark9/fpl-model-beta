from understatapi import UnderstatClient
import pandas as pd
import matplotlib.pyplot as plt

with UnderstatClient() as understat:
    teams = understat.team_list(league="EPL", season="2025")
    all_data = []
    for team in teams:
        match_data = understat.team(team=team).get_match_data(season="2025")
        for match in match_data:
            # Extract team name, date, goals, xG
            # Handle if 'goals' and 'xG' are lists
            goals = match['goals'][0] if isinstance(match['goals'], list) else match['goals']
            xG = match['xG'][0] if isinstance(match['xG'], list) else match['xG']
            all_data.append({
                'team': team,
                'date': match['date'],
                'goals': goals,
                'xG': xG
            })

df = pd.DataFrame(all_data)
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['goals'] = pd.to_numeric(df['goals'], errors='coerce')
df['xG'] = pd.to_numeric(df['xG'], errors='coerce')

# Group by date and sum goals/xG for all teams
df_grouped = df.groupby('date')[['goals', 'xG']].sum().reset_index()

plt.figure(figsize=(12, 6))
plt.plot(df_grouped['date'], df_grouped['goals'], label='Total Actual Goals', marker='o')
plt.plot(df_grouped['date'], df_grouped['xG'], label='Total Expected Goals (xG)', marker='x')
plt.xlabel('Date')
plt.ylabel('Goals')
plt.title('EPL 2025: Total Actual Goals vs Expected Goals (xG) per Matchday')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
