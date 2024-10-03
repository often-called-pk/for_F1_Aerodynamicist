# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 09:13:27 2023

@author: mvvsk
"""

import fastf1 as ff1
import numpy as np
import matplotlib as mpl
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import math

pd.options.mode.chained_assignment = None
ff1.Cache.enable_cache('cache/')

##############################################################################
# First, we define some variables that allow us to conveniently control what
# we want to plot.
year = 2023
wknd = 'Austrian'
ses = 'Qualifying'
driver1 = 'VER'
driver2 = 'LEC'
lap_no=26
colormap = mpl.cm.plasma
rotate_map = 60 # degrees in anti-clockwise direction
rotate_flag=0
##############################################################################
# Next, we load the session and select the desired data.
session = ff1.get_session(year, wknd, ses)
weekend = session.event
session.load()

# Dr1_lap = session.laps.pick_driver(driver1).pick_lap(lap_no)
# Dr2_lap = session.laps.pick_driver(driver2).pick_lap(lap_no)

Dr1_lap = session.laps.pick_driver(driver1).pick_fastest()
Dr2_lap = session.laps.pick_driver(driver2).pick_fastest()

# Get telemetry data
x1 = Dr1_lap.telemetry['X'].to_list()              # values for x-axis
y1 = Dr1_lap.telemetry['Y'].to_list()               # values for y-axis
color1 = Dr1_lap.telemetry['Speed'].to_list()      # value to base color gradient on
t1 = Dr1_lap.telemetry['Time'].dt.total_seconds().to_list()

x2 = Dr2_lap.telemetry['X'].to_list()                # values for x-axis
y2 = Dr2_lap.telemetry['Y'].to_list()                # values for y-axis
color2 = Dr2_lap.telemetry['Speed'].to_list()      # value to base color gradient on
t2 = Dr2_lap.telemetry['Time'].dt.total_seconds().to_list()

if rotate_flag !=0:
    x1_rot=[]
    y1_rot=[]
    x2_rot=[]
    y2_rot=[]
    theta=rotate_map*math.pi/180

    for i in range(len(x1)):
        rx1 = x1[i]*math.cos(theta) - y1[i]*math.sin(theta)
        ry1 = x1[i]*math.sin(theta) + y1[i]*math.cos(theta)
        x1_rot.append(rx1)
        y1_rot.append(ry1)
    
    for j in range(len(x2)):
        rx2 = x2[j]*math.cos(theta) - y2[j]*math.sin(theta)
        ry2 = x2[j]*math.sin(theta) + y2[j]*math.cos(theta)
        x2_rot.append(rx2)
        y2_rot.append(ry2)
    
col_dict={
    "PER":"Blue",
    "VER":"Blue",
    "LEC":"Red",
    "SAI":"Red",
    "RUS":"Cyan",
    "HAM":"Cyan",
    "ALO":"Green",
    "STR":"Green",
    "PIA":"#ff8700",
    "NOR":"#ff8700",
    "ALB":"#005aff",
    "SAR":"#005aff",
    "GAS":"#0090ff",
    "OCO":"#0090ff",
    "HUL":"#ffffff",
    "MAG":"#ffffff",
    "TSU":"#2b4562",
    "DEV":"#2b4562",
    "BOT":"#900000",
    "ZHO":"#900000",
    }
c1 = col_dict[driver1]
c2 = col_dict[driver2]
##############################################################################
# After this, we can actually plot the data.

# We create a plot with title and adjust some setting to make it look good.
fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
fig.suptitle(f'{wknd} GP {year} - {driver1} - Racing Lines', size=24, y=0.97)

# Adjust margins and turn of axis
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)

ax.plot(x1, y1, color=c1, linestyle='-', linewidth=4, zorder=0, label='Original track')
if rotate_flag !=0:
    ax.plot(x1_rot, y1_rot, color=c1, linestyle='--', linewidth=4, zorder=0, 
            label='Rotated by '+str(rotate_map)+' deg')
ax.legend(fontsize='20')
plt.show

fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
fig.suptitle(f'{wknd} GP {year} - {driver2} - Racing Lines', size=24, y=0.97)

# Adjust margins and turn of axis
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)

ax.plot(x2, y2, color=c2, linestyle='-', linewidth=4, zorder=0, label='Original track')
if rotate_flag !=0:
    ax.plot(x2_rot, y2_rot, color=c2, linestyle='--', linewidth=4, zorder=0, 
            label='Rotated by '+str(rotate_map)+' deg')
ax.legend(fontsize='20')
plt.show    
    
##############################################################################
if rotate_flag !=0:
    dict1={'Dr1_X_Pos':x1,'Dr1_Y_Pos':y1,'Dr1_Time':t1,'Dr1_X_Pos_Rot':x1_rot,
           'Dr1_Y_Pos_Rot':y1_rot,'Dr1_Speed':color1}
    dict2={'Dr2_X_Pos':x2,'Dr2_Y_Pos':y2,'Dr2_Time':t2,'Dr2_X_Pos_Rot':x2_rot,
           'Dr2_Y_Pos_Rot':y2_rot,'Dr2_Speed':color2}
else:
    dict1={'Dr1_X_Pos':x1,'Dr1_Y_Pos':y1,'Dr1_Time':t1,'Dr1_Speed':color1}
    dict2={'Dr2_X_Pos':x2,'Dr2_Y_Pos':y2,'Dr2_Time':t2,'Dr2_Speed':color2}    


df_2 = pd.DataFrame.from_dict(dict2) 
df_1 = pd.DataFrame.from_dict(dict1) 
df_1.to_excel(driver1+'_'+wknd+'_'+ses+'_data.xlsx')
df_2.to_excel(driver2+'_'+wknd+'_'+ses+'_data.xlsx')

   