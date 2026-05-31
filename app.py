import streamlit as st
import pickle
import pandas as pd

st.title('IPL Win Predictor')
teams = [
    'Chennai Super Kings',
    'Delhi Capitals',
    'Gujarat Titans',
    'Kolkata Knight Riders',
    'Lucknow Super Giants',
    'Mumbai Indians',
    'Punjab Kings',
    'Rajasthan Royals',
    'Royal Challengers Bengaluru',
    'Sunrisers Hyderabad'
]

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali', 'Bengaluru']
try:
    with open('pipe.pkl', 'rb') as f:
        pipe = pickle.load(f)
except FileNotFoundError:
    st.error("Model file 'pipe.pkl' not found. Please check the file path and ensure it's available.")

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
with col2:
    bowling_team= st.selectbox('Select the bowling team', sorted(teams))

selected_city = st.selectbox('select host city' , sorted(cities))

target = st.number_input('target')
col3,col4,col5= st.columns(3)

with col3:
    score= st.number_input('Score')
with col4:
    overs = st.number_input('overs completed' )
with col5:
    wickets = st.number_input('wickets out' )


if st.button('Predict Probability'):

    run_left = target - score
    ball_left = 120 - int(overs * 6)

    wicket_fallen = wickets
    wickets_remaining = 10 - wickets

    crr = score / overs if overs > 0 else 0
    required_run_rate = (run_left * 6) / ball_left if ball_left > 0 else 0
    run_rate_diff = crr - required_run_rate

    input_df = pd.DataFrame({
        'city':[selected_city],
        'target_runs':[target],
        'batting_team':[batting_team],
        'bowling_team':[bowling_team],
        'current_score':[score],
        'wickets_remaining':[wickets_remaining],
        'run_left':[run_left],
        'ball_left':[ball_left],
        'wicket_fallen':[wicket_fallen],
        'required_run_rate':[required_run_rate],
        'crr':[crr],
        'run_rate_diff':[run_rate_diff]
    })

    result = pipe.predict_proba(input_df)

    loss = result[0][0]
    win = result[0][1]

    st.header(f"{batting_team} : {round(win*100,2)}%")
    st.header(f"{bowling_team} : {round(loss*100,2)}%")