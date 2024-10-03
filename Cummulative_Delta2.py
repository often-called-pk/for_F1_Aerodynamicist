# -*- coding: utf-8 -*-
"""
Created on Mon May 15 19:01:19 2023

@author: msrms
"""


import fastf1 as ff1
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

pd.options.mode.chained_assignment = None
ff1.Cache.enable_cache('cache/')

# Inputs ---------------------------------------
event = 'RACE'
session = ff1.get_session(2023, 'MIAMI', event)
laps = session.load_laps()
drivers = ['VER', 'PER', 'ALO', 'RUS', 'SAI', 'HAM', 'LEC', 'GAS', 'OCO',
           'MAG','TSU','STR','BOT','ALB','HUL']
Baseline = 90
Reference_driver = 'VER'
# --------------------------------------------

dr_colours = []
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
ls=[]
lin_style={
    "PER":"-",
    "VER":"--",
    "LEC":"-",
    "SAI":"--",
    "RUS":"-",
    "HAM":"--",
    "ALO":"-",
    "STR":"--",
    "PIA":"-",
    "NOR":"--",
    "ALB":"-",
    "SAR":"--",
    "GAS":"-",
    "OCO":"--",
    "HUL":"-",
    "MAG":"--",
    "TSU":"-",
    "DEV":"--",
    "BOT":"-",
    "ZHO":"--",
    }
for col in drivers:
    dr_colours.append(col_dict[col])
    ls.append(lin_style[col])
    
laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()
laps = laps.loc[(laps['PitOutTime'].isnull() & laps['PitInTime'].isnull())]
laps_1 = pd.DataFrame().assign(Driver=laps['Driver'], LapTimeSeconds=laps['LapTimeSeconds'],
                               Compound=laps['Compound'],LapNumber=laps['LapNumber'],
                               LapStartTime=laps['LapStartTime'])
laps_1['LapStartTime'] = laps_1['LapStartTime'].dt.total_seconds()


# Reference Driver data
Ref_laps=laps_1.loc[laps_1['Driver']==Reference_driver].LapNumber.tolist()
Ref_timings=laps_1.loc[laps_1['Driver']==Reference_driver].LapTimeSeconds.tolist()
Ref_St_time=laps_1.loc[laps_1['Driver']==Reference_driver].LapStartTime.tolist()

for L in range(len(Ref_laps)):
    X1=laps_1.loc[laps_1['LapNumber']==Ref_laps[L]]
    X1['LapTimeSeconds']-=Ref_timings[L]
    X1['LapStartTime']-=Ref_St_time[L]
    X1['GapToRefDr']=X1['LapStartTime']+X1['LapTimeSeconds']
    if L == 0:
        X2=X1
    else:
        X2=pd.concat([X1,X2], ignore_index=True)
        
        
# ------------------------------------------------------------------------
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(19.20, 10.8), dpi=100)

for j in range(len(drivers)):
    driver_tel=X2.loc[X2['Driver']==drivers[j]]
    x=driver_tel['LapNumber']
    y=driver_tel['GapToRefDr']
        
    
    ax.plot(x,y,linewidth=3,label=drivers[j],color=dr_colours[j],linestyle=ls[j])
    
plt.grid(which='both', color='0.65', linestyle='-')
ax.invert_yaxis()
ax.set_xticks(np.arange(0,57,4))
ax.xaxis.set_tick_params(labelsize=25)
ax.yaxis.set_tick_params(labelsize=25)
ax.legend(fontsize=20,markerscale=2,bbox_to_anchor=(1.01, 1.0), loc='upper left')
plt.ylabel('Laptime (s)', fontweight='bold', fontsize=26)
plt.xlabel('Laps', fontweight='bold', fontsize=26)
plt.suptitle(
    f" Cumulative Delta \n"
    f"{session.event.year} {session.event['EventName']} ({event}) ", fontsize=25, fontweight='bold')