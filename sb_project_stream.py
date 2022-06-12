from asyncio import events
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from mplsoccer.pitch import Pitch
from statsbombpy import sb
import streamlit as st
import base64
from PIL import Image

barca1_lineup = sb.lineups(match_id=3773585)['Barcelona'] 
barca1_lineup = barca1_lineup[['jersey_number', 'player_name', 'player_nickname']]

barca2_lineup = sb.lineups(match_id=69299)['Barcelona'] 
barca2_lineup = barca1_lineup[['jersey_number', 'player_name', 'player_nickname']]

koeman_face = Image.open('/Users/gianmarcozironelli/Desktop/koeman_face.png')
guardiola_face = Image.open('/Users/gianmarcozironelli/Desktop/guardiola_face.png')

st.header('StatsBomb Analysis')
st.subheader('Ronald Koeman vs Pep Guardiola Playstyle')

col1, col2 = st.columns(2)
with col1:

    st.image(koeman_face)
    st.write("Barcelona 2020")
    st.write(barca1_lineup)

with col2:

    st.image(guardiola_face)
    st.write("Barcelona 2010")
    st.write(barca2_lineup)

#Retrieving Data
events_df = sb.events(match_id=3773585)
events2_df = sb.events(match_id=69299)

competitions = sb.competitions()
LaLiga_2020 = sb.matches(competition_id=11, season_id=90)


with st.expander('Retrieving Data'):
     st.text('Data can be accessed by importing "sb" from statsbombpy. All the instructions can be found on the homonym GitHub repository or on the Statsbomb website https://statsbomb.com/')
     st.subheader('Available competitions')
     st.dataframe(competitions)
     st.subheader('La Liga 2020 Matches')
     st.dataframe(LaLiga_2020)

with st.expander('Data Exploration')
     st.write('A quick look at the raw data')
     st.write(events_df)
