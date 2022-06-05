from asyncio import events
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from mplsoccer.pitch import Pitch
from statsbombpy import sb
import streamlit as st

st.header('StatsBomb Analysis')
st.write('**Barcelona** - Real Madrid 2020')

events_df = sb.events(match_id=3773585)

#data wrangling
events_df = events_df.fillna(0)
pass_df = events_df[events_df.type == 'Pass']

new_pass_df = pass_df.iloc[:,[17,31,32,35,37,85]]
new_pass_df2 = pass_df.iloc[:,40:71]

pass_df = pd.concat([new_pass_df, new_pass_df2], axis=1, join='inner')

pass_df['xstart'] = [x for x,y in pass_df['location']]
pass_df['ystart'] = [y for x,y in pass_df['location']]
pass_df['xend'] = [x for x,y in pass_df['pass_end_location']]
pass_df['yend'] = [y for x,y in pass_df['pass_end_location']]

pass_df['pass_outcome'].replace(0,'Complete', inplace=True)

#pitch setup
pitch = Pitch(pitch_type='statsbomb', pitch_color='#ffffff', line_color='#000000')
fig, ax = pitch.draw(figsize=(12, 6), constrained_layout=True, tight_layout=False)
fig.set_facecolor('#769176')

#Completed passes
for ind in pass_df.index:
    if pass_df['pass_outcome'][ind] == 'Complete':
         plt.plot((pass_df['xstart'][ind],pass_df['xend'][ind]),(pass_df['ystart'][ind],pass_df['yend'][ind]), color='green')
         plt.scatter(pass_df['xstart'][ind],pass_df['ystart'][ind], color='green')

#Incompleted passes
    if pass_df['pass_outcome'][ind] == 'Incomplete':
         plt.plot((pass_df['xstart'][ind],pass_df['xend'][ind]),(pass_df['ystart'][ind],pass_df['yend'][ind]), color='red')
         plt.scatter(pass_df['xstart'][ind],pass_df['ystart'][ind], color='green')
st.write(fig)

#Busquets focus
pitch = Pitch(pitch_type='statsbomb', pitch_color='#565c5e', line_color='#ffffff')
fig, ax = pitch.draw(figsize=(12, 6), constrained_layout=True, tight_layout=False)
fig.set_facecolor('#769176')

for ind in pass_df.index:
    if pass_df['player'][ind] == 'Sergio Busquets i Burgos':
         plt.plot((pass_df['xstart'][ind],pass_df['xend'][ind]),(pass_df['ystart'][ind],pass_df['yend'][ind]), color='#1724bd')
         plt.scatter(pass_df['xstart'][ind],pass_df['ystart'][ind], color='#1724bd')
         plt.title('Busquets passages',color='white',size=16)
st.write(fig)

#NETWORK MAP
barca_pass_df = pass_df[pass_df['team']=='Barcelona']

#considering only completed passes
barca_pass_df = barca_pass_df[barca_pass_df['pass_outcome']=='Complete']

#creating two columns for the passer and the recipient (the latter by using .shift)
barca_pass_df['passer'] = barca_pass_df['player']
barca_pass_df['recipient'] = barca_pass_df['player'].shift(-1)

substitution_df = events_df[events_df['type']=='Substitution']
subs_minute_df = substitution_df['minute']
first_subs = subs_minute_df.min()

barca_pass_df = barca_pass_df[barca_pass_df['minute'] < first_subs]

#grouping the passer, avrg value of the x, avrg value of the y + count
average_loc_df = barca_pass_df.groupby('passer').agg({'xstart':['mean'], 'ystart':['mean', 'count']})
average_loc_df.columns = ['x_loc', 'y_loc', 'count']
pass_network_barca_df = barca_pass_df.groupby(['passer', 'recipient']).index.count().reset_index()
pass_network_barca_df.rename({'index':'pass_count'}, axis='columns',inplace=True)

pass_network_barca_df = pass_network_barca_df.merge(average_loc_df, left_on='passer',right_index=True)
pass_network_barca_df = pass_network_barca_df.merge(average_loc_df, left_on='recipient',right_index=True,suffixes=['', '_end'])

pass_network_barca_df['width'] = (pass_network_barca_df.pass_count / pass_network_barca_df.pass_count.max() * 17) #setting max values of width
min_transparency = 0.3
c_transparency = pass_network_barca_df.pass_count / pass_network_barca_df.pass_count.max()
c_transparency = (c_transparency * (1 - min_transparency)) + min_transparency

network_map_field = Pitch(pitch_type='statsbomb', pitch_color='#565c5e', line_color='#ffffff')
fig, ax = pitch.draw(figsize=(12, 6), constrained_layout=True, tight_layout=False)
fig.set_facecolor('#769176')

links = network_map_field.lines(pass_network_barca_df.x_loc, pass_network_barca_df.y_loc, 
                                 pass_network_barca_df.x_loc_end, pass_network_barca_df.y_loc_end,
                                 linewidth = pass_network_barca_df.width, color = 'w', ax = ax, zorder = 1, alpha = 0.6)

nodes = network_map_field.scatter(average_loc_df.x_loc, average_loc_df.y_loc,
                     s = 300, color = 'blue', edgecolors = 'black', linewidth = 1.5, alpha = 1, zorder = 1, ax=ax)
plt.show()