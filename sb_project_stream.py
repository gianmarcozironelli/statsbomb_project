from asyncio import events
import code
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from mplsoccer.pitch import Pitch
from statsbombpy import sb
import streamlit as st
import base64
from PIL import Image
import seaborn as sns

st.set_page_config(layout="wide")

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

#RETRIEVING DATA
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


#DATA EXPLORATION
#quick view of the variables
events_df.head()
events_df.tail(10)
events_df.info()

#filling Nan values with 0
events_df = events_df.fillna(0)
events2_df = events2_df.fillna(0)

#replacing "true" with 1 for a better handling
events_df = events_df.replace('TRUE','1')
events2_df = events2_df.replace('TRUE','1')

#dropping a column that rose issues with streamlit
#raw_data_to_display = events2_df.drop(['50_50', 'foul_committed_card'], 1)

#creating a histogram to understan which are the main events of both matches 
fig_1 = plt.figure(figsize =(20, 6))
ax_1 = fig_1.add_subplot(1, 2, 1)
events_df.type.hist(bins=25, ax=ax_1)
plt.title('Koeman')
plt.ylabel('type count')
plt.xticks(rotation = 90)
ax_2 = fig_1.add_subplot(1, 2, 2)
events2_df.type.hist(bins=25, ax=ax_2)
plt.title('Guardiola')
plt.ylabel('type count')
plt.xticks(rotation = 90)
plt.show()

code_1 = '''
#filling Nan values with 0
events_df = events_df.fillna(0)
events2_df = events2_df.fillna(0)

#replacing "true" with 1 for a better handling
events_df = events_df.replace('TRUE','1')
events2_df = events2_df.replace('TRUE','1')

#creating a histogram to understan which are the main events of both matches 
fig_1 = plt.figure(figsize =(20, 6))
ax_1 = fig_1.add_subplot(1, 2, 1)
events_df.type.hist(bins=25, ax=ax_1)
plt.title('Koeman')
plt.ylabel('type count')
plt.xticks(rotation = 90)
ax_2 = fig_1.add_subplot(1, 2, 2)
events2_df.type.hist(bins=25, ax=ax_2)
plt.title('Guardiola')
plt.ylabel('type count')
plt.xticks(rotation = 90)
'''

with st.expander('Data Exploration'):
     st.write('A quick look at the raw data')
     #st.write(raw_data_to_display)
     st.write('Data exploration and general cleaning')
     st.code(code_1, language='python')
     st.write(fig_1)




#PASS MAP
#data wrangling
#considering only significative "pass" type events
pass_df = events_df[events_df.type == 'Pass']
pass2_df = events2_df[events_df.type == 'Pass']

#selecting only relevant columns 
new_pass_df = pass_df.iloc[:,[17,31,32,35,37,85]]
new_pass_df2 = pass_df.iloc[:,40:71]
new_pass2_df = pass2_df.iloc[:,[17,31,32,35,37,85]]
new_pass2_df2 = pass2_df.iloc[:,40:71]

#creating a single df
pass_df = pd.concat([new_pass_df, new_pass_df2], axis=1, join='inner')
pass2_df = pd.concat([new_pass2_df, new_pass2_df2], axis=1, join='inner')

#unpacking the coordinates of the start location and the end location
pass_df['xstart'] = [x for x,y in pass_df['location']]
pass_df['ystart'] = [y for x,y in pass_df['location']]
pass_df['xend'] = [x for x,y in pass_df['pass_end_location']]
pass_df['yend'] = [y for x,y in pass_df['pass_end_location']]

pass2_df = pass2_df[pass2_df['pass_end_location'].notna()]
pass2_df = pass2_df.loc[~((pass2_df['pass_end_location'] == 0))]

pass2_df['xstart'] = [x for x,y in pass2_df['location']]
pass2_df['ystart'] = [y for x,y in pass2_df['location']]
pass2_df['xend'] = [x for x,y in pass2_df['pass_end_location']]
pass2_df['yend'] = [y for x,y in pass2_df['pass_end_location']]

#modifyng the pass_outcome due to some differences between dataframes.
pass_df['pass_outcome'].replace(0,'Complete', inplace=True)
pass2_df['pass_outcome'].replace(0,'Complete', inplace=True)

code_2 = '''
#considering only significative "pass" type events
pass_df = events_df[events_df.type == 'Pass']
pass2_df = events2_df[events_df.type == 'Pass']

#selecting only relevant columns 
new_pass_df = pass_df.iloc[:,[17,31,32,35,37,85]]
new_pass_df2 = pass_df.iloc[:,40:71]
new_pass2_df = pass2_df.iloc[:,[17,31,32,35,37,85]]
new_pass2_df2 = pass2_df.iloc[:,40:71]

#creating a single df
pass_df = pd.concat([new_pass_df, new_pass_df2], axis=1, join='inner')
pass2_df = pd.concat([new_pass2_df, new_pass2_df2], axis=1, join='inner')

#unpacking the coordinates of the start location and the end location
pass_df['xstart'] = [x for x,y in pass_df['location']]
pass_df['ystart'] = [y for x,y in pass_df['location']]
pass_df['xend'] = [x for x,y in pass_df['pass_end_location']]
pass_df['yend'] = [y for x,y in pass_df['pass_end_location']]

pass2_df = pass2_df[pass2_df['pass_end_location'].notna()]
pass2_df = pass2_df.loc[~((pass2_df['pass_end_location'] == 0))]

pass2_df['xstart'] = [x for x,y in pass2_df['location']]
pass2_df['ystart'] = [y for x,y in pass2_df['location']]
pass2_df['xend'] = [x for x,y in pass2_df['pass_end_location']]
pass2_df['yend'] = [y for x,y in pass2_df['pass_end_location']]

#modifyng the pass_outcome due to some differences between dataframes.
pass_df['pass_outcome'].replace(0,'Complete', inplace=True)
pass2_df['pass_outcome'].replace(0,'Complete', inplace=True)
'''

#pitch setup
pitch = Pitch(pitch_type='statsbomb', pitch_color='#46494d', line_color='#ffffff')

pass_map, axs = pitch.grid(ncols=2, axis=False, endnote_height=0.05)
pass_map.set_facecolor('#46494d')

#2020
for ind in pass_df.index:
    if pass_df['team'][ind] == 'Barcelona' and pass_df['pass_outcome'][ind] == 'Complete':
         pitch.arrows((pass_df['xstart'][ind]),(pass_df['ystart'][ind]),
                      (pass_df['xend'][ind]) ,(pass_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#2cab3d',
                       ax=axs['pitch'][0], label='completed passes')

    if pass_df['team'][ind] == 'Barcelona' and pass_df['pass_outcome'][ind] == 'Incomplete':
         pitch.arrows((pass_df['xstart'][ind]),(pass_df['ystart'][ind]),
                      (pass_df['xend'][ind]) ,(pass_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#bd2924',
                       ax=axs['pitch'][0], label='other passes')

#2010
for ind in pass2_df.index:
    if pass2_df['possession_team'][ind] == 'Barcelona' and pass2_df['pass_outcome'][ind] == 'Complete':
         pitch.arrows((pass2_df['xstart'][ind]),(pass2_df['ystart'][ind]),
                      (pass2_df['xend'][ind]) ,(pass2_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#2cab3d',
                       ax=axs['pitch'][1], label='completed passes')

    if pass2_df['possession_team'][ind] == 'Barcelona' and pass2_df['pass_outcome'][ind] == 'Incomplete':
         pitch.arrows((pass2_df['xstart'][ind]),(pass2_df['ystart'][ind]),
                      (pass2_df['xend'][ind]) ,(pass2_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#bd2924',
                       ax=axs['pitch'][1], label='other passes')

axs['pitch'][0].set_title('Barcelona passages 2020' ,color='white',size=25)
axs['pitch'][1].set_title('Barcelona passages 2010' ,color='white',size=25)

code_3 = '''
#pitch setup
pitch = Pitch(pitch_type='statsbomb', pitch_color='#46494d', line_color='#ffffff')

pass_map, axs = pitch.grid(ncols=2, axis=False, endnote_height=0.05)
pass_map.set_facecolor('#46494d')

#2020
for ind in pass_df.index:
    if pass_df['team'][ind] == 'Barcelona' and pass_df['pass_outcome'][ind] == 'Complete':
         pitch.arrows((pass_df['xstart'][ind]),(pass_df['ystart'][ind]),
                      (pass_df['xend'][ind]) ,(pass_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#2cab3d',
                       ax=axs['pitch'][0], label='completed passes')

    if pass_df['team'][ind] == 'Barcelona' and pass_df['pass_outcome'][ind] == 'Incomplete':
         pitch.arrows((pass_df['xstart'][ind]),(pass_df['ystart'][ind]),
                      (pass_df['xend'][ind]) ,(pass_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#bd2924',
                       ax=axs['pitch'][0], label='other passes')

#2010
for ind in pass2_df.index:
    if pass2_df['possession_team'][ind] == 'Barcelona' and pass2_df['pass_outcome'][ind] == 'Complete':
         pitch.arrows((pass2_df['xstart'][ind]),(pass2_df['ystart'][ind]),
                      (pass2_df['xend'][ind]) ,(pass2_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#2cab3d',
                       ax=axs['pitch'][1], label='completed passes')

    if pass2_df['possession_team'][ind] == 'Barcelona' and pass2_df['pass_outcome'][ind] == 'Incomplete':
         pitch.arrows((pass2_df['xstart'][ind]),(pass2_df['ystart'][ind]),
                      (pass2_df['xend'][ind]) ,(pass2_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#bd2924',
                       ax=axs['pitch'][1], label='other passes')

axs['pitch'][0].set_title('Barcelona passages 2020' ,color='white',size=25)
axs['pitch'][1].set_title('Barcelona passages 2010' ,color='white',size=25)
'''

#calulating the xstart mean for each teams to better explain what the graph is showing us
barcelona_pass_df= pass_df.groupby('team').mean()
barcelona_pass2_df= pass2_df.groupby('possession_team').mean()
#barcelona_pass_df['xstart'] #62
#barcelona_pass2_df['xstart'] #59

#since I didn't expect those values, I'll try to plot a displot to understand what happened
xstart_2020_df = pass_df.filter(['team', 'xstart'], axis=1)
xstart_2010_df =pass2_df.filter(['possession_team', 'xstart'], axis=1)
xstart_2010_df.rename(columns={'possession_team': 'team'}, inplace=True)
xstart_2020_df['team'].replace('Barcelona','Barcelona 2020', inplace=True)
xstart_2010_df['team'].replace('Barcelona','Barcelona 2010', inplace=True)
xstart_displot_df = xstart_2020_df.append(xstart_2010_df)
xstart_displot_df = xstart_displot_df[xstart_displot_df.team !='Real Madrid']
xstart_displot_df = xstart_displot_df.reset_index()

#plotting
pass_displot = sns.displot(xstart_displot_df, x="xstart", hue="team")

code_4 = '''
#calulating the xstart mean for each teams to better explain what the graph is showing us
barcelona_pass_df= pass_df.groupby('team').mean()
barcelona_pass2_df= pass2_df.groupby('possession_team').mean()
barcelona_pass_df['xstart'] #62
barcelona_pass2_df['xstart'] #59

#since I didn't expect those values, I'll try to plot a displot to understand what happened
xstart_2020_df = pass_df.filter(['team', 'xstart'], axis=1)
xstart_2010_df =pass2_df.filter(['possession_team', 'xstart'], axis=1)
xstart_2010_df.rename(columns={'possession_team': 'team'}, inplace=True)
xstart_2020_df['team'].replace('Barcelona','Barcelona 2020', inplace=True)
xstart_2010_df['team'].replace('Barcelona','Barcelona 2010', inplace=True)
xstart_displot_df = xstart_2020_df.append(xstart_2010_df)
xstart_displot_df = xstart_displot_df[xstart_displot_df.team !='Real Madrid']
xstart_displot_df = xstart_displot_df.reset_index()

#plotting
pass_displot = sns.displot(xstart_displot_df, x="xstart", hue="team")
'''

#streamlit section
with st.expander('Pass Map'):
    st.write("Data wrangling")
    st.code(code_2)
    st.write("creating the Pass Map")
    st.code(code_3)
    st.write(pass_map)
    col1, col2 = st.columns(2)
    with col1:

        barcelona_pass_df['xstart']

    with col2:

        barcelona_pass2_df['xstart']
    st.text('To better understand the 2 differents playstyles I created a displot based on the xstart')
    st.write(pass_displot)
