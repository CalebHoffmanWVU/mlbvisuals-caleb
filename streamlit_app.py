import streamlit as st
import pandas as pd
import datetime
import pybaseball
import matplotlib.pyplot as plt

st.title("MLB Visualizations Website for 2024")
st.subheader("This application will allow you to go into your favorite teams game and understand strike zone data for both pitchers and batters")


note = "Neontetete"
mlb_teams = {
    'Arizona Diamondbacks': 'ARI',
    'Atlanta Braves': 'ATL',
    'Baltimore Orioles': 'BAL',
    'Boston Red Sox': 'BOS',
    'Chicago Cubs': 'CHC',
    'Chicago White Sox': 'CWS',
    'Cincinnati Reds': 'CIN',
    'Cleveland Guardians': 'CLE',
    'Colorado Rockies': 'COL',
    'Detroit Tigers': 'DET',
    'Houston Astros': 'HOU',
    'Kansas City Royals': 'KC',
    'Los Angeles Angels': 'LAA',
    'Los Angeles Dodgers': 'LAD',
    'Miami Marlins': 'MIA',
    'Milwaukee Brewers': 'MIL',
    'Minnesota Twins': 'MIN',
    'New York Mets': 'NYM',
    'New York Yankees': 'NYY',
    'Oakland Athletics': 'OAK',
    'Philadelphia Phillies': 'PHI',
    'Pittsburgh Pirates': 'PIT',
    'San Diego Padres': 'SD',
    'Seattle Mariners': 'SEA',
    'San Francisco Giants': 'SF',
    'St. Louis Cardinals': 'STL',
    'Tampa Bay Rays': 'TB',
    'Texas Rangers': 'TEX',
    'Toronto Blue Jays': 'TOR',
    'Washington Nationals': 'WSH'
}

# Dropdown Menu for MLB Team Selection
selected_team_name = st.selectbox('Select an MLB team', list(mlb_teams.keys()))

selected_team_abbreviation = mlb_teams[selected_team_name]

data = pybaseball.schedule_and_record(2024, selected_team_abbreviation)

startseason = datetime.date(2024, 3, 28)
endseason = datetime.date(2024, 9, 30)

selected_date = st.date_input('Select a date from the 2024 Regular Season', min_value = startseason, max_value = endseason)

formatted_date = selected_date.strftime('%Y-%m-%d')

statcast = pybaseball.statcast(formatted_date, team=selected_team_abbreviation)

pitcher_info = statcast[['player_name', 'pitcher']]

if statcast.empty:
    st.write("No games scheduled for this day")
else:
    st.subheader("Pitcher Visualizations")
    selected_pitcher = st.selectbox('Select a pitcher from the game', list(statcast['player_name'].unique()))
    pitcher_filtered = pitcher_info[pitcher_info['player_name'] == selected_pitcher]
    pitcher_id = pitcher_filtered.iloc[0, 1]
    day_data = pybaseball.statcast_pitcher(start_dt = formatted_date, end_dt = formatted_date, player_id = pitcher_id)
    innings_list = list((day_data['inning'].unique()))
    innings_list.insert(0, 'All Innings')
    inning_selected = st.selectbox('Select an inning', innings_list)
    if inning_selected == 'All Innings':
        pybaseball.plot_strike_zone(day_data, title = f"Strike Zone for {selected_pitcher} on {selected_date} for All Innings", annotation='effective_speed')
        st.pyplot(plt.gcf())
        plt.clf()
        ba_data = day_data[day_data['estimated_ba_using_speedangle'].notna()]
        pybaseball.plot_strike_zone(ba_data, title=f"Estimated BA for Batters against {selected_pitcher} on {selected_date} for All Innings", annotation='estimated_ba_using_speedangle')
        st.pyplot(plt.gcf())
        plt.clf()
    else:
        pybaseball.plot_strike_zone(day_data.loc[day_data['inning'] == inning_selected], title = f"Strike Zone for {selected_pitcher} on {selected_date} in Inning #{inning_selected}", annotation='effective_speed')
        st.pyplot(plt.gcf())
        plt.clf()
        ba_data = day_data[day_data['estimated_ba_using_speedangle'].notna()]
        pybaseball.plot_strike_zone(ba_data.loc[ba_data['inning'] == inning_selected], title=f"Estimated BA for Batters against {selected_pitcher} on {selected_date} in Inning #{inning_selected}", annotation='estimated_ba_using_speedangle')
        st.pyplot(plt.gcf())
        plt.clf()

    st.subheader("Batter Visualization")

    away_team = statcast.iloc[0, 20]

    batstatcast = pybaseball.statcast(formatted_date, team=selected_team_abbreviation)

    bat_id_list = list(batstatcast['batter'].unique())

    names = pybaseball.playerid_reverse_lookup(bat_id_list)

    names['full_name'] = names['name_last'].str.capitalize() + ' , ' + names['name_first'].str.capitalize()

    name_dict = dict(zip(names['full_name'], names['key_mlbam']))

    selected_batter = st.selectbox('Select a batter from the game', list(names['full_name']))

    pybaseball.plot_strike_zone(batstatcast.loc[batstatcast["batter"] == name_dict[selected_batter]], title = f"{selected_batter} Launch Speeds for {selected_date}", colorby='pitcher', annotation="launch_speed")
    st.pyplot(plt.gcf())
    plt.clf()

st.subheader("About the Developer")
st.write("Caleb Hoffman is a student at West Virginia University, graduating with a Bachelor of Science in Data Science in December 2024. During his time at West Virginia University, Caleb was a Lewis Fellow for Data Driven WV, an outreach program that paired students up with real business to solve real-world problems with data-driven solutions. In his free time, Caleb enjoys playing Disc Golf, watching Pittsburgh Sports Teams, and playing Nintendo Video Games")
st.image("Caleb Hoffman - Headshot.png", caption="Caleb Hoffman")




















