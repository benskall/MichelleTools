import streamlit as st
import requests
import os
import google.generativeai as genai
import json



def configure_gemini(api_key):
    genai.configure(api_key=api_key)

key = (st.secrets["key"])

genai.configure(api_key=key)
def generate_content(prompt, model_name="gemini-1.5-flash"):
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return "An error occurred while generating content."

def fetch_draft_data(year):
    url = 'https://stats.nba.com/stats/drafthistory'
    headers = {
        'Host': 'stats.nba.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-nba-stats-token': 'true',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'x-nba-stats-origin': 'stats',
        'Referer': 'https://stats.nba.com/draft/history/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en',
        'Origin': 'https://www.nba.com'
    }
    params = {
        'LeagueID': '00',
        'Season': str(year),
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        draft_rows = data['resultSets'][0]['rowSet']
        draft_headers = data['resultSets'][0]['headers']
        draft_data = [dict(zip(draft_headers, row)) for row in draft_rows]

        return draft_data
    except Exception as e:
        st.error(f"Error fetching draft data: {e}")
        return None

def filter_draft_data(draft_data, selected_team, selected_round, team_city_mapping):
    filtered_data = []

    if selected_team != 'All Teams':
        selected_city = team_city_mapping.get(selected_team, None)
        if selected_city is None:
            return []
    else:
        selected_city = None  
    for player in draft_data:
        if selected_city:
            team_match = player['TEAM_NAME'] == selected_city
        else:
            team_match = True

        if selected_round != 'All Rounds':
            round_match = str(player['ROUND_NUMBER']) == selected_round
        else:
            round_match = True

        if team_match and round_match:
            filtered_data.append(player)

    return filtered_data

def generate_summary(draft_data):
    try:
        limited_data = draft_data[:5]
        prompt = f"As mario in his language also include more mario references: Provide an analysis of the following NBA draft data and using there data from their recent games: {json.dumps(limited_data)}. Additionally explain how these players are better than lebron,pretend they will be, and they are; also pretend lebron is overrated, and how they could live up to Jordan's Legacy."
        summary = generate_content(prompt)
        return summary
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None

def main():
    API_KEY = st.secrets["key"]
    if not API_KEY or API_KEY == "your_api_key_here":
        st.error("Please set your GEMINI_API_KEY environment variable.")
        return
    configure_gemini(API_KEY)

    st.title("NBA Draft History Explorer 🤖")
    st.write("Explore NBA draft history and get AI-generated insights.")

    if 'selected_year' not in st.session_state:
        st.session_state['selected_year'] = 2023  
    if 'selected_team' not in st.session_state:
        st.session_state['selected_team'] = 'All Teams'
    if 'selected_round' not in st.session_state:
        st.session_state['selected_round'] = 'All Rounds'
    if 'draft_data' not in st.session_state:
        st.session_state['draft_data'] = fetch_draft_data(st.session_state['selected_year'])

    year = st.selectbox("Select Draft Year", list(range(2023, 1946, -1)), index=0)

    if st.session_state['selected_year'] != year:
        st.session_state['draft_data'] = fetch_draft_data(year)
        st.session_state['selected_year'] = year

    draft_data = st.session_state['draft_data']

    if draft_data is not None:
        team_city_mapping = {
            'Atlanta Hawks': 'Hawks',
            'Boston Celtics': 'Celtics',
            'Brooklyn Nets': 'Nets',
            'Buffalo Braves':'Braves',
            'Charlotte Bobcats': 'Bobcats',
            'Charlotte Hornets': 'Hornets',
            'Chicago Bulls': 'Bulls',
            'Chicago Packers':'Packers',
            'Chicago Stags':'Stags',
            'Chicago Zephyrs':'Zephyrs',
            'Cincinnatti Royals': 'Royals',
            'Cleveland Cavaliers': 'Cavaliers',
            'Dallas Mavericks': 'Mavericks',
            'Denver Nuggets': 'Nuggets',
            'Detroit Pistons': 'Pistons',
            'Golden State Warriors': 'Warriors',
            'Houston Rockets': 'Rockets',
            'Indiana Pacers': 'Pacers',
            'Indianapolis Jets': 'Jets',
            'Indianapolis Olympians': 'Olympians',
            'Los Angeles Clippers': 'Clippers',
            'Los Angeles Lakers': 'Lakers',
            'Memphis Grizzlies': 'Grizzlies',
            'Miami Heat': 'Heat',
            'Milwaukee Bucks': 'Bucks',
            'Minnesota Timberwolves': 'Timberwolves',
            'New Orleans Pelicans': 'Pelicans',
            'New York Knicks': 'Knicks',
            'Oklahoma City Thunder': 'Thunder',
            'Orlando Magic': 'Magic',
            'Philadelphia 76ers': '76ers',
            'Pittsburgh Ironmen':'Ironmen',
            'Phoenix Suns': 'Suns',
            'Portland Trail Blazers': 'Trail Blazers',
            'Providence Steamrollers':'Steamrollers',
            'Sacramento Kings': 'Kings',
            'San Antonio Spurs': 'Spurs',
            'Seattle SuperSonics':'SuperSonics',
            'Syracuse Nationals':'Nationals',
            'Toronto Raptors': 'Raptors',
            'Toronto Huskies': 'Huskies',
            'Tri-Cities Blackhawks': 'Blackhawks',
            'Utah Jazz': 'Jazz',
            'Washington Bullets': 'Bullets',
            'Washington Capitols':'Capitols',
            'Washington Wizards': 'Wizards'
        }

        team_list = ['All Teams'] + list(team_city_mapping.keys())
        selected_team = st.selectbox(
            "Select Team",
            team_list,
            index=team_list.index(st.session_state['selected_team'])
        )
        st.session_state['selected_team'] = selected_team

        round_options = ['All Rounds','0', '1', '2','3','4','5','6','7','8','9','10']
        selected_round = st.selectbox(
            "Select Round",
            round_options,
            index=round_options.index(st.session_state['selected_round'])
        )
        st.session_state['selected_round'] = selected_round

        filtered_data = filter_draft_data(
            draft_data,
            selected_team,
            selected_round,
            team_city_mapping
        )

        if filtered_data:
            st.success(f"Found {len(filtered_data)} draft picks.")
            st.write(filtered_data)
            if st.button("Generate Summary with Gemini"):
                summary = generate_summary(filtered_data)
                if summary:
                    st.write("**Gemini-Generated Summary:**")
                    st.write(summary)
        else:
            st.warning("No data found for the selected criteria.")
    else:
        st.error("Failed to fetch draft data.")

if __name__ == "__main__":
    main()
