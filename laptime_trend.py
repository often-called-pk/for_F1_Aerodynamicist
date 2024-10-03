# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 09:29:45 2023

@author: mvvsk
"""

import fastf1 as ff1
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np 

pd.options.mode.chained_assignment = None
ff1.Cache.enable_cache('cache/')

session = ff1.get_session(2023, "British", 'RACE')
session.load(telemetry=False, weather=False)
l1=list(range(1,20))
l2=list(range(30,53))
delete_laps=l1+l2
laptimemin, laptimemax = 80, 100
drvs=['NOR' , 'LEC' , 'RUS']

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

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(19.20, 10.8), dpi=100)

for drv in drvs:
    drv_laps=session.laps.pick_driver(drv)
    abb = drv_laps['Driver'].iloc[0]
    print(abb)
    drv_col=col_dict[drv]
    LN=drv_laps['LapNumber'].tolist()
    Lap_tym=drv_laps['LapTime'].dt.total_seconds().tolist()
    Comp=drv_laps['Compound'].tolist()
    cols=[]
    m=[]
    for C in Comp:
        if C=='MEDIUM':
            cols.append('Yellow')
            m.append("o")
        if C=='HARD':
            cols.append('White')
            m.append("D")
        if C=='SOFT':
            cols.append('Red')
            m.append("s")
    df=pd.DataFrame(list(zip(LN, Lap_tym,Comp,cols,m)),
               columns =['LapNumber', 'LapTime','Compound','TyreColor','Marker'])
    
    # Filter Based on Laptimes
    df=df[df['LapTime']>laptimemin]
    df=df[df['LapTime']<laptimemax]
    
    # Delete laps
    for L in delete_laps:
        df2=df.drop(df[df['LapNumber']==L].index, inplace = True)
    
    x=df['LapNumber']
    y=df['LapTime']
    xnew = np.linspace(df['LapNumber'].min(), df['LapNumber'].max(), 
                       num=3*len(df['LapNumber']), endpoint=True)
    # f_cubic = interp1d(x, y, kind=3)
    
    ax.plot(df['LapNumber'],df['LapTime'],linewidth=3, label=abb, color=drv_col)
    # ax.plot(xnew,f_cubic(xnew),label=abb, color=drv_col)
    ax.scatter(x=x,y=y,s=400,c=df['TyreColor'],
               edgecolor=drv_col, marker='D', linewidths=3)
    
ax.set_ylabel('Lap Time, s',fontsize=26)
ax.set_xlabel('Lap Number',fontsize=26)
ax.xaxis.set_tick_params(labelsize=25)
ax.yaxis.set_tick_params(labelsize=25)
ax.legend(ncol=3,fontsize='32',loc='lower left')#bbox_to_anchor=(1.0, 1.02),
    
plt.xticks(np.arange(20, 30, 2))
plt.xlim([19,30])
plt.ylim([92.4,93.2])

plt.suptitle(
    f" Lap Time Trend \n"
    f"{session.event.year} {session.event['EventName']} (RACE) ", fontsize=25, fontweight='bold')
resolution_value = 100

# Turn on major grid lines
plt.grid(color='w', which='major', axis='both', linestyle='--')
plt.tight_layout()

plt.show()    
