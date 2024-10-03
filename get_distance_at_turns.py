# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 21:37:03 2023

@author: mvvsk
"""

import fastf1 as ff1
import numpy as np
import matplotlib as mpl
import pandas as pd
from matplotlib import pyplot as plt
import math

pd.options.mode.chained_assignment = None
ff1.Cache.enable_cache('cache/')

##############################################################################
# First, we define some variables that allow us to conveniently control what
# we want to plot.
year = 2022
wknd = 'Hungary'
ses = 'RACE'
driver1 = 'VER'
lap_no=27
Fastestlap_Flag=0
data_interval=15 #secs
turn_nos={"1":600,"2":1150,"3":1300,"4":1788,"5":1996,"6":2350,"7":2400,
          "8":2557,"9":2730,"10":2850,"11":3090,
          "12":3528,"13":3750,"14":4050,}
##############################################################################
# Next, we load the session and select the desired data.
session = ff1.get_session(year, wknd, ses)
weekend = session.event
session.load()

if Fastestlap_Flag == 1:
    Dr1_lap = session.laps.pick_driver(driver1).pick_fastest()
else:
    Dr1_lap = session.laps.pick_driver(driver1).pick_lap(lap_no)


# Get telemetry data
x1 = Dr1_lap.telemetry['X'].to_list()              # values for x-axis
y1 = Dr1_lap.telemetry['Y'].to_list()               # values for y-axis
color1 = Dr1_lap.telemetry['Speed'].to_list()      # value to base color gradient on
t1 = Dr1_lap.telemetry['Time'].dt.total_seconds().to_list()
D1=Dr1_lap.telemetry['Distance'].to_list()
##############################################################################
# After this, we can actually plot the data.

# We create a plot with title and adjust some setting to make it look good.
fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
fig.suptitle(f'{wknd} GP {year} - {driver1} - Distance from start', size=24, y=0.97)

# Adjust margins and turn of axis
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)

ax.plot(x1, y1, color='blue', linestyle='-', linewidth=4, zorder=0, label='track')
ax.scatter(x1[0], y1[0], color='red', marker='X', s=300)

# Adjust margins and turn of axis
ax.legend(fontsize='5',loc='best') 

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
for j in range(0,len(D1),data_interval):
    textstr=str(round(D1[j]))
    ax.text(x1[j],y1[j],textstr,fontsize=12,bbox=props)

############################################################ 
# We create a plot with title and adjust some setting to make it look good.
fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
fig.suptitle(f'{wknd} GP {year} - {driver1} - Turn nos', size=24, y=0.97)
ax.plot(x1, y1, color='blue', linestyle='-', linewidth=4, zorder=0, label='track')

# Add turn numbers
props3 = dict(boxstyle='round', facecolor='red', alpha=1)
arr = np.asarray(D1)

for j3 in turn_nos:
    i = (np.abs(arr - turn_nos[j3])).argmin()
    textstr3=j3
    ax.text(x1[i]*1.1,y1[i]*1.1,textstr3,fontsize=12,bbox=props3)
    ax.scatter(x1[i],y1[i], color='red', marker='D')
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
############################################################
plt.show
