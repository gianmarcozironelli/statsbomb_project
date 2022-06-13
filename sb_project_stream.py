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
sns.displot(xstart_displot_df, x="xstart", hue="team")
plt.savefig('pass_displot.png')

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

#messi passes focus
messi_pass_map, axs = pitch.grid(ncols=2, axis=False, endnote_height=0.05)
messi_pass_map.set_facecolor('#46494d')

#2020
for ind in pass_df.index:
    if pass_df['player'][ind] == 'Lionel Andrés Messi Cuccittini' and pass_df['pass_outcome'][ind] == 'Complete':
         pitch.arrows((pass_df['xstart'][ind]),(pass_df['ystart'][ind]),
                      (pass_df['xend'][ind]) ,(pass_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#2cab3d',
                       ax=axs['pitch'][0], label='completed passes')

    if pass_df['player'][ind] == 'Lionel Andrés Messi Cuccittini' and pass_df['pass_outcome'][ind] == 'Incomplete':
         pitch.arrows((pass_df['xstart'][ind]),(pass_df['ystart'][ind]),
                      (pass_df['xend'][ind]) ,(pass_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#bd2924',
                       ax=axs['pitch'][0], label='other passes')

#2009
for ind in pass2_df.index:
    if pass2_df['player'][ind] == 'Lionel Andrés Messi Cuccittini' and pass2_df['pass_outcome'][ind] == 'Complete':
         pitch.arrows((pass2_df['xstart'][ind]),(pass2_df['ystart'][ind]),
                      (pass2_df['xend'][ind]) ,(pass2_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#2cab3d',
                       ax=axs['pitch'][1], label='completed passes')

    if pass2_df['player'][ind] == 'Lionel Andrés Messi Cuccittini' and pass2_df['pass_outcome'][ind] == 'Incomplete':
         pitch.arrows((pass2_df['xstart'][ind]),(pass2_df['ystart'][ind]),
                      (pass2_df['xend'][ind]) ,(pass2_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#bd2924',
                       ax=axs['pitch'][1], label='other passes')

axs['pitch'][0].set_title('Messi passages 2020' ,color='white',size=25)
axs['pitch'][1].set_title('Messi passages 2009' ,color='white',size=25)

code_5 ='''
if pass2_df['player'][ind] == 'Lionel Andrés Messi Cuccittini' and pass2_df['pass_outcome'][ind] == 'Complete':
'''

#streamlit section
with st.expander('Pass Map'):
    st.write("Data wrangling")
    st.code(code_2)
    st.write("creating the Pass Map")
    st.code(code_3)
    st.write(pass_map)
    st.code(code_4)
    col1, col2 = st.columns(2)
    with col1:

        barcelona_pass_df['xstart']
    with col2:

        barcelona_pass2_df['xstart']
    st.text('To better understand the 2 differents playstyles I created a displot based on the xstart')
    pass_displot = Image.open('pass_displot.png')
    st.image(pass_displot)
    st.write("Messi Focus")
    st.code(code_5)
    st.write(messi_pass_map)


#PASS NETWORK MAP
barca_pass_df = pass_df[pass_df['team']=='Barcelona']
barca_pass2_df = pass2_df[pass2_df['possession_team']=='Barcelona']

#considering only completed passes
barca_pass_df = barca_pass_df[barca_pass_df['pass_outcome']=='Complete']
barca_pass2_df = barca_pass2_df[barca_pass2_df['pass_outcome']=='Complete']
#creating two columns for the passer and the recipient (the latter by using .shift)
barca_pass_df['passer'] = barca_pass_df['player']
barca_pass_df['recipient'] = barca_pass_df['player'].shift(-1)
barca_pass2_df['passer'] = barca_pass2_df['player']
barca_pass2_df['recipient'] = barca_pass2_df['player'].shift(-1)

#the number of players to represent has to be = 11
barca_pass2_df['player'].value_counts()

#To reach that number I need to choose only the first half (before subs)
substitution_df = events_df[events_df['type']=='Substitution']
subs_minute_df = substitution_df['minute']
first_subs = subs_minute_df.min()

substitution2_df = events2_df[events2_df['type']=='Substitution']
subs_minute2_df = substitution2_df['minute']
first_subs2 = subs_minute2_df.min()

barca_pass_df = barca_pass_df[barca_pass_df['minute'] < first_subs]
barca_pass2_df = barca_pass2_df[barca_pass2_df['minute'] < first_subs2]

#update of number of players and removing errors
barca_pass2_df = barca_pass2_df[barca_pass2_df.player != 'Karim Benzema']
barca_pass2_df = barca_pass2_df[barca_pass2_df.player != 'Sergio Ramos García'] 
barca_pass2_df = barca_pass2_df[barca_pass2_df.player != 'Marcelo Vieira da Silva Júnior']

#grouping the passer
#avrg value of the x
#avrg value of the y + count
average_loc_df = barca_pass_df.groupby('passer').agg({'xstart':['mean'], 'ystart':['mean', 'count']})
average_loc2_df = barca_pass2_df.groupby('passer').agg({'xstart':['mean'], 'ystart':['mean', 'count']})

average_loc_df.columns = ['x_loc', 'y_loc', 'count']
average_loc2_df.columns = ['x_loc', 'y_loc', 'count']

pass_network_barca_df = barca_pass_df.groupby(['passer', 'recipient']).index.count().reset_index()
pass_network2_barca_df = barca_pass2_df.groupby(['passer', 'recipient']).index.count().reset_index()

pass_network_barca_df.rename({'index':'pass_count'}, axis='columns',inplace=True)
pass_network2_barca_df.rename({'index':'pass_count'}, axis='columns',inplace=True)

#to create the complete df I need to merge the 2 dfs obtained --> here I have the PASSER column that let me use .merge function
pass_network_barca_df = pass_network_barca_df.merge(average_loc_df, left_on='passer',right_index=True)
pass_network_barca_df = pass_network_barca_df.merge(average_loc_df, left_on='recipient',right_index=True,suffixes=['', '_end'])

pass_network2_barca_df = pass_network2_barca_df.merge(average_loc2_df, left_on='passer',right_index=True)
pass_network2_barca_df = pass_network2_barca_df.merge(average_loc2_df, left_on='recipient',right_index=True,suffixes=['', '_end'])

#setting max values of width
pass_network_barca_df['width'] = (pass_network_barca_df.pass_count / pass_network_barca_df.pass_count.max() * 17)
pass_network2_barca_df['width'] = (pass_network2_barca_df.pass_count / pass_network2_barca_df.pass_count.max() * 17)


min_transparency = 0.3
c_transparency = pass_network_barca_df.pass_count / pass_network_barca_df.pass_count.max()
c2_transparency = pass_network2_barca_df.pass_count / pass_network2_barca_df.pass_count.max()

c_transparency = (c_transparency * (1 - min_transparency)) + min_transparency
c2_transparency = (c2_transparency * (1 - min_transparency)) + min_transparency

dw_pass_network_map_code = '''
barca_pass_df = pass_df[pass_df['team']=='Barcelona']
barca_pass2_df = pass2_df[pass2_df['possession_team']=='Barcelona']

#considering only completed passes
barca_pass_df = barca_pass_df[barca_pass_df['pass_outcome']=='Complete']
barca_pass2_df = barca_pass2_df[barca_pass2_df['pass_outcome']=='Complete']
#creating two columns for the passer and the recipient (the latter by using .shift)
barca_pass_df['passer'] = barca_pass_df['player']
barca_pass_df['recipient'] = barca_pass_df['player'].shift(-1)
barca_pass2_df['passer'] = barca_pass2_df['player']
barca_pass2_df['recipient'] = barca_pass2_df['player'].shift(-1)

#the number of players to represent has to be = 11
barca_pass2_df['player'].value_counts()

#To reach that number I need to choose only the first half (before subs)
substitution_df = events_df[events_df['type']=='Substitution']
subs_minute_df = substitution_df['minute']
first_subs = subs_minute_df.min()

substitution2_df = events2_df[events2_df['type']=='Substitution']
subs_minute2_df = substitution2_df['minute']
first_subs2 = subs_minute2_df.min()

barca_pass_df = barca_pass_df[barca_pass_df['minute'] < first_subs]
barca_pass2_df = barca_pass2_df[barca_pass2_df['minute'] < first_subs2]

#update of number of players and removing errors
barca_pass2_df = barca_pass2_df[barca_pass2_df.player != 'Karim Benzema']
barca_pass2_df = barca_pass2_df[barca_pass2_df.player != 'Sergio Ramos García'] 
barca_pass2_df = barca_pass2_df[barca_pass2_df.player != 'Marcelo Vieira da Silva Júnior']

#grouping the passer
#avrg value of the x
#avrg value of the y + count
average_loc_df = barca_pass_df.groupby('passer').agg({'xstart':['mean'], 'ystart':['mean', 'count']})
average_loc2_df = barca_pass2_df.groupby('passer').agg({'xstart':['mean'], 'ystart':['mean', 'count']})

average_loc_df.columns = ['x_loc', 'y_loc', 'count']
average_loc2_df.columns = ['x_loc', 'y_loc', 'count']

pass_network_barca_df = barca_pass_df.groupby(['passer', 'recipient']).index.count().reset_index()
pass_network2_barca_df = barca_pass2_df.groupby(['passer', 'recipient']).index.count().reset_index()

pass_network_barca_df.rename({'index':'pass_count'}, axis='columns',inplace=True)
pass_network2_barca_df.rename({'index':'pass_count'}, axis='columns',inplace=True)

#to create the complete df I need to merge the 2 dfs obtained --> here I have the PASSER column that let me use .merge function
pass_network_barca_df = pass_network_barca_df.merge(average_loc_df, left_on='passer',right_index=True)
pass_network_barca_df = pass_network_barca_df.merge(average_loc_df, left_on='recipient',right_index=True,suffixes=['', '_end'])

pass_network2_barca_df = pass_network2_barca_df.merge(average_loc2_df, left_on='passer',right_index=True)
pass_network2_barca_df = pass_network2_barca_df.merge(average_loc2_df, left_on='recipient',right_index=True,suffixes=['', '_end'])

#setting max values of width
pass_network_barca_df['width'] = (pass_network_barca_df.pass_count / pass_network_barca_df.pass_count.max() * 17)
pass_network2_barca_df['width'] = (pass_network2_barca_df.pass_count / pass_network2_barca_df.pass_count.max() * 17)


min_transparency = 0.3
c_transparency = pass_network_barca_df.pass_count / pass_network_barca_df.pass_count.max()
c2_transparency = pass_network2_barca_df.pass_count / pass_network2_barca_df.pass_count.max()

c_transparency = (c_transparency * (1 - min_transparency)) + min_transparency
c2_transparency = (c2_transparency * (1 - min_transparency)) + min_transparency
'''

#Plotting the Network Map
network_map_field = Pitch(pitch_type='statsbomb', pitch_color='#46494d', line_color='#ffffff')
network_map, axs = pitch.grid(ncols=2, axis=False, endnote_height=0.05)
network_map.set_facecolor('#46494d')

links = network_map_field.lines(pass_network_barca_df.x_loc, pass_network_barca_df.y_loc, 
                                 pass_network_barca_df.x_loc_end, pass_network_barca_df.y_loc_end,
                                 linewidth = pass_network_barca_df.width, color = 'w', ax = axs['pitch'][0], zorder = 1, alpha = 0.6)

nodes = network_map_field.scatter(average_loc_df.x_loc, average_loc_df.y_loc,
                     s = 300, color = 'red', edgecolors = 'black', linewidth = 1.5, alpha = 1, zorder = 1, ax=axs['pitch'][0])

#2010
links2 = network_map_field.lines(pass_network2_barca_df.x_loc, pass_network2_barca_df.y_loc, 
                                 pass_network2_barca_df.x_loc_end, pass_network2_barca_df.y_loc_end,
                                 linewidth = pass_network2_barca_df.width, color = 'w', ax = axs['pitch'][1], zorder = 1, alpha = 0.6)

nodes2 = network_map_field.scatter(average_loc2_df.x_loc, average_loc2_df.y_loc,
                     s = 300, color = 'red', edgecolors = 'black', linewidth = 1.5, alpha = 1, zorder = 1, ax=axs['pitch'][1])

axs['pitch'][0].set_title(' Network map 2020' ,color='white',size=25)
axs['pitch'][1].set_title(' Network map 2010' ,color='white',size=25)

network_map_code = '''
network_map_field = Pitch(pitch_type='statsbomb', pitch_color='#46494d', line_color='#ffffff')
fig, axs = pitch.grid(ncols=2, axis=False, endnote_height=0.05)
fig.set_facecolor('#46494d')

links = network_map_field.lines(pass_network_barca_df.x_loc, pass_network_barca_df.y_loc, 
                                 pass_network_barca_df.x_loc_end, pass_network_barca_df.y_loc_end,
                                 linewidth = pass_network_barca_df.width, color = 'w', ax = axs['pitch'][0], zorder = 1, alpha = 0.6)

nodes = network_map_field.scatter(average_loc_df.x_loc, average_loc_df.y_loc,
                     s = 300, color = 'red', edgecolors = 'black', linewidth = 1.5, alpha = 1, zorder = 1, ax=axs['pitch'][0])

#2010
links2 = network_map_field.lines(pass_network2_barca_df.x_loc, pass_network2_barca_df.y_loc, 
                                 pass_network2_barca_df.x_loc_end, pass_network2_barca_df.y_loc_end,
                                 linewidth = pass_network2_barca_df.width, color = 'w', ax = axs['pitch'][1], zorder = 1, alpha = 0.6)

nodes2 = network_map_field.scatter(average_loc2_df.x_loc, average_loc2_df.y_loc,
                     s = 300, color = 'red', edgecolors = 'black', linewidth = 1.5, alpha = 1, zorder = 1, ax=axs['pitch'][1])

axs['pitch'][0].set_title(' Network map 2020' ,color='white',size=25)
axs['pitch'][1].set_title(' Network map 2010' ,color='white',size=25)
'''

#streamlit section
with st.expander('Pass Network Map'):
    st.write("Data wrangling")
    st.code(dw_pass_network_map_code)
    st.write("creating the Pass Network Map")
    st.code(network_map_code)
    st.write(network_map)

#CARRIES HEATMAP
#Data wrangling
carries_df = events_df[events_df.type == 'Carry']
carries2_df = events2_df[events2_df.type == 'Carry']

carries_df['carry_xstart'] = [x for x,y in carries_df['location']]
carries_df['carry_ystart'] = [y for x,y in carries_df['location']]
carries_df['carry_xend'] = [x for x,y in carries_df['carry_end_location']]
carries_df['carry_yend'] = [y for x,y in carries_df['carry_end_location']]

carries2_df['carry_xstart'] = [x for x,y in carries2_df['location']]
carries2_df['carry_ystart'] = [y for x,y in carries2_df['location']]
carries2_df['carry_xend'] = [x for x,y in carries2_df['carry_end_location']]
carries2_df['carry_yend'] = [y for x,y in carries2_df['carry_end_location']]

dw_heatmap_code = '''
carries_df = events_df[events_df.type == 'Carry']
carries2_df = events2_df[events2_df.type == 'Carry']

carries_df['carry_xstart'] = [x for x,y in carries_df['location']]
carries_df['carry_ystart'] = [y for x,y in carries_df['location']]
carries_df['carry_xend'] = [x for x,y in carries_df['carry_end_location']]
carries_df['carry_yend'] = [y for x,y in carries_df['carry_end_location']]

carries2_df['carry_xstart'] = [x for x,y in carries2_df['location']]
carries2_df['carry_ystart'] = [y for x,y in carries2_df['location']]
carries2_df['carry_xend'] = [x for x,y in carries2_df['carry_end_location']]
carries2_df['carry_yend'] = [y for x,y in carries2_df['carry_end_location']]
'''

#Creating the Heatmap
heatmap, axs = pitch.grid(ncols=2, axis=False, endnote_height=0.05)
heatmap.set_facecolor('#46494d')

kde = sns.kdeplot(carries_df['carry_xstart'], carries_df['carry_ystart'], cmap = 'magma', 
                  shade = True, alpha=0.7, shade_lowest=False, ax = axs['pitch'][0])

kde2 = sns.kdeplot(carries2_df['carry_xstart'], carries2_df['carry_ystart'], cmap = 'magma', 
                  shade = True, alpha=0.7, shade_lowest=False, ax = axs['pitch'][1])

axs['pitch'][0].set_title(' Heatmap 2020' ,color='white',size=25)
axs['pitch'][1].set_title(' Heatmap 2009' ,color='white',size=25)

heatmap_code = '''
heatmap, axs = pitch.grid(ncols=2, axis=False, endnote_height=0.05)
heatmap.set_facecolor('#46494d')

kde = sns.kdeplot(carries_df['carry_xstart'], carries_df['carry_ystart'], cmap = 'magma', 
                  shade = True, alpha=0.7, shade_lowest=False, ax = axs['pitch'][0])

kde2 = sns.kdeplot(carries2_df['carry_xstart'], carries2_df['carry_ystart'], cmap = 'magma', 
                  shade = True, alpha=0.7, shade_lowest=False, ax = axs['pitch'][1])

axs['pitch'][0].set_title(' Heatmap 2020' ,color='white',size=25)
axs['pitch'][1].set_title(' Heatmap 2009' ,color='white',size=25)

'''

#messi focus heatmap
messi_carries_df = carries_df[carries_df.player == 'Lionel Andrés Messi Cuccittini']
messi_carries2_df = carries2_df[carries2_df.player == 'Lionel Andrés Messi Cuccittini']

messi_heatmap, axs = pitch.grid(ncols=2, axis=False, endnote_height=0.05)
messi_heatmap.set_facecolor('#46494d')

sns.kdeplot(messi_carries_df['carry_xstart'], messi_carries_df['carry_ystart'], shade = True, alpha=0.8, ax = axs['pitch'][0])
sns.kdeplot(messi_carries2_df['carry_xstart'], messi_carries2_df['carry_ystart'], shade = True, alpha=0.8, ax = axs['pitch'][1])

axs['pitch'][0].set_title('Messi Heatmap 2020' ,color='white',size=25)
axs['pitch'][1].set_title('Messi Heatmap 2009' ,color='white',size=25)


#Heatmap + passes map of Leo Messi
heatmap_passes_messi, axs = pitch.grid(ncols=2, axis=False, endnote_height=0.05)
heatmap_passes_messi.set_facecolor('#46494d')

#2020
for ind in pass_df.index:
    if pass_df['player'][ind] == 'Lionel Andrés Messi Cuccittini' and pass_df['pass_outcome'][ind] == 'Complete':
         pitch.arrows((pass_df['xstart'][ind]),(pass_df['ystart'][ind]),
                      (pass_df['xend'][ind]) ,(pass_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#2cab3d',
                       ax=axs['pitch'][0], label='completed passes')

    if pass_df['player'][ind] == 'Lionel Andrés Messi Cuccittini' and pass_df['pass_outcome'][ind] == 'Incomplete':
         pitch.arrows((pass_df['xstart'][ind]),(pass_df['ystart'][ind]),
                      (pass_df['xend'][ind]) ,(pass_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#bd2924',
                       ax=axs['pitch'][0], label='other passes')

#2009
for ind in pass2_df.index:
    if pass2_df['player'][ind] == 'Lionel Andrés Messi Cuccittini' and pass2_df['pass_outcome'][ind] == 'Complete':
         pitch.arrows((pass2_df['xstart'][ind]),(pass2_df['ystart'][ind]),
                      (pass2_df['xend'][ind]) ,(pass2_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#2cab3d',
                       ax=axs['pitch'][1], label='completed passes')

    if pass2_df['player'][ind] == 'Lionel Andrés Messi Cuccittini' and pass2_df['pass_outcome'][ind] == 'Incomplete':
         pitch.arrows((pass2_df['xstart'][ind]),(pass2_df['ystart'][ind]),
                      (pass2_df['xend'][ind]) ,(pass2_df['yend'][ind]),
                       width=2,headwidth=10, headlength=10, color='#bd2924',
                       ax=axs['pitch'][1], label='other passes')
         
sns.kdeplot(messi_carries_df['carry_xstart'], messi_carries_df['carry_ystart'], shade = True, alpha=0.3, ax = axs['pitch'][0])
sns.kdeplot(messi_carries2_df['carry_xstart'], messi_carries2_df['carry_ystart'], shade = True, alpha=0.3, ax = axs['pitch'][1])

axs['pitch'][0].set_title('Messi passages 2020' ,color='white',size=25)
axs['pitch'][1].set_title('Messi passages 2009' ,color='white',size=25)



#streamlit section
with st.expander('Carries heatmap'):
    st.write("Data wrangling")
    st.code(dw_heatmap_code)
    st.write("creating the  Heamap")
    st.code(heatmap_code)
    st.write(heatmap)
    st.write("Messi Focus")
    st.write(messi_heatmap)
    st.write(heatmap_passes_messi)



#SHOTS

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

#retrieving the data of the whole season
grouped_events = sb.competition_events(
    country="Spain",
    division= "La Liga",
    season="2020/2021",
    split=True
)
shots_df = grouped_events["shots"]

#deleting shots registered from penalties or free kicks
shots_df = shots_df.loc[~((shots_df['shot_type'] == 'Penalty'))]
shots_df = shots_df.loc[~((shots_df['shot_type'] == 'Free Kick'))]

#transforming the shot_outcome to reduce the number of possible outcomes --> goal = 1 | other = 0
shots_df['shot_outcome'] = shots_df['shot_outcome'].replace({'Goal':'1', 'Off T':'0', 'Post':'0','Blocked':'0',
                                                             'Saved':'0','Wayward':'0', 'Saved Off Target':'0',
                                                             'Saved to Post':'0'})

shots_df = shots_df[['shot_aerial_won', 'shot_deflected', 'shot_one_on_one', 
                     'shot_open_goal','under_pressure','shot_outcome','location',
                     'shot_end_location']].copy()

#transforming the shot_end_location coordinates to unpack them
shots_df['shot_end_location'] = shots_df['shot_end_location'].str.slice(0,2)

shots_df['shot_xstart'] = [x for x,y in shots_df['location']]
shots_df['shot_ystart'] = [y for x,y in shots_df['location']]
shots_df['shot_xend'] = [x for x,y in shots_df['shot_end_location']]
shots_df['shot_yend'] = [y for x,y in shots_df['shot_end_location']]

#calculating the euclidean distance
shots_df['shot_distance'] = np.sqrt((shots_df.shot_xstart-shots_df.shot_xend)**2 + (shots_df.shot_ystart-shots_df.shot_yend)**2)

distance_goal_df = shots_df[['shot_outcome','shot_distance']]

fig, ax = plt.subplots()
shot_distance = distance_goal_df.hist("shot_distance", ax = ax)

dw_shots_code = '''
#retrieving the data of the whole season
grouped_events = sb.competition_events(
    country="Spain",
    division= "La Liga",
    season="2020/2021",
    split=True
)
shots_df = grouped_events["shots"]

#deleting shots registered from penalties or free kicks
shots_df = shots_df.loc[~((shots_df['shot_type'] == 'Penalty'))]
shots_df = shots_df.loc[~((shots_df['shot_type'] == 'Free Kick'))]

#transforming the shot_outcome to reduce the number of possible outcomes --> goal = 1 | other = 0
shots_df['shot_outcome'] = shots_df['shot_outcome'].replace({'Goal':'1', 'Off T':'0', 'Post':'0','Blocked':'0',
                                                             'Saved':'0','Wayward':'0', 'Saved Off Target':'0',
                                                             'Saved to Post':'0'})

shots_df = shots_df[['shot_aerial_won', 'shot_deflected', 'shot_one_on_one', 
                     'shot_open_goal','under_pressure','shot_outcome','location',
                     'shot_end_location']].copy()

#transforming the shot_end_location coordinates to unpack them
shots_df['shot_end_location'] = shots_df['shot_end_location'].str.slice(0,2)

shots_df['shot_xstart'] = [x for x,y in shots_df['location']]
shots_df['shot_ystart'] = [y for x,y in shots_df['location']]
shots_df['shot_xend'] = [x for x,y in shots_df['shot_end_location']]
shots_df['shot_yend'] = [y for x,y in shots_df['shot_end_location']]

#calculating the euclidean distance
shots_df['shot_distance'] = np.sqrt((shots_df.shot_xstart-shots_df.shot_xend)**2 + (shots_df.shot_ystart-shots_df.shot_yend)**2)

distance_goal_df = shots_df[['shot_outcome','shot_distance']]
'''


with st.expander('Shots Analysis'):
    st.write("Data wrangling")
    st.code(dw_shots_code)
    st.write("First view of the shooting distance")
    st.write(shot_distance)