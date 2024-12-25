import requests
import streamlit as st

# Global constants
URL = 'https://stats.nba.com/stats/drafthistory'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.nba.com/',
    'Origin': 'https://www.nba.com',
}

def get_team_draft_picks_by_name(season, team_name):

    response = requests.get(URL, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        result_sets = data.get("resultSets", [])
        for result_set in result_sets:
            if result_set.get("name") == "DraftHistory":
                headers = result_set.get("headers", [])
                rows = result_set.get("rowSet", [])
                filtered_picks = [
                    dict(zip(headers, row))
                    for row in rows
                    if row[headers.index("SEASON")] == season and row[headers.index("TEAM_NAME")].lower() == team_name.lower()
                ]
                
                return filtered_picks
    else:
        st.error(f"Failed to fetch data: HTTP {response.status_code}")#NEW
        return []
def get_all_years_and_teams():
    response = requests.get(URL, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        result_sets = data.get("resultSets", [])
        
        for result_set in result_sets:
            if result_set.get("name") == "DraftHistory":
                rows = result_set.get("rowSet", [])
                years = sorted({row[2] for row in rows})  
                teams = sorted({row[9] for row in rows})  
                return years, teams
    else:
        st.error(f"Failed to fetch data: HTTP {response.status_code}")
        return [], []

st.title("NBA Draft Picks Viewer 🏀")
st.write("Select a team name and season to view their draft picks.")
years, teams = get_all_years_and_teams()
season = st.selectbox("Select Season Year", years) #NEW
team_name = st.selectbox("Select Team Name", teams)


if st.button("Get Draft Picks"): #NEW
    if season and team_name:
        picks = get_team_draft_picks_by_name(season, team_name)
        if picks:
            st.write(f"Draft Picks for {team_name} in Season {season}:")
            st.table(picks)
        else:
            st.write(f"No draft picks found for {team_name} in Season {season}.")
    else:
        st.error("Please enter both a season year and a team name.")
