# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 20:26:11 2023

@author: mvvsk
"""

import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from fastf1 import utils
import pandas as pd
from timple.timedelta import strftimedelta
import numpy as np
plotting.setup_mpl()
ff1.Cache.enable_cache('cache/')
#=============================================================
ssn_name='RACE'
session = ff1.get_session(2023, 'British Grand Prix', ssn_name)
session.load(weather=False)
lapno=46
Fastestlap_Flag=1
drivers=['NOR','HAM']
turn_nos={"1":1020,"2":2000}
#=============================================================

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
fig, ax = plt.subplots(2, figsize=(19.20, 10.8), dpi=100, 
                       gridspec_kw={'height_ratios': [
                       3, 1]})
legs=[]
dict={}
for j in drivers:
    if Fastestlap_Flag == 1:
        driver_dat=session.laps.pick_driver(j).pick_fastest()
    else:
        driver_dat=session.laps.pick_driver(j).pick_lap(lapno)
    drv_tel=driver_dat.get_car_data().add_distance()
    laptime = driver_dat['LapTime']
    # formatlaptime = strftimedelta(laptime, "%m:%s.%ms")
    # lap_times.append(formatlaptime)
    if Fastestlap_Flag == 1:
        dict[j]=laptime.total_seconds()
    else:
        tmp=laptime.dt.total_seconds().to_list()
        dict[j]=tmp[0]
    driver_color = col_dict[j]
    ax[0].plot(drv_tel['Distance'], drv_tel['Speed'],
               linewidth=3, color=driver_color,label=j)
    legs.append(j+" ["+str(dict[j])+"s]")
    
ax[0].legend(legs, fontsize=23, loc=0)
# ax[0].legend(legs,bbox_to_anchor=(0.1, 1.05),fontsize=23)
ax[0].set_ylabel('Speed, km/h', fontweight='bold', fontsize=22)
ax[0].xaxis.set_tick_params(labelsize=25)
ax[0].yaxis.set_tick_params(labelsize=25)
for g in turn_nos:
    ax[0].axvline(x = turn_nos[g], color = 'yellow', linestyle = '--')

# find the fastest driver
lt=min(list(dict.values()))
fastest_dr = [k for k, v in dict.items() if v == lt][0]
if Fastestlap_Flag == 1:
    x1=session.laps.pick_driver(fastest_dr).pick_fastest()
else:
    x1=session.laps.pick_driver(fastest_dr).pick_lap(lapno)
x2=x1.get_car_data().add_distance()
zero_delta=[0]*len(x2)
for j2 in drivers:
    if j2 == fastest_dr:
        ax[1].plot(x2['Distance'].to_list(),zero_delta,linewidth=3, color=col_dict[fastest_dr])
    else:
        if Fastestlap_Flag == 1:
            driver_dat2=session.laps.pick_driver(j2).pick_fastest()
        else:
            driver_dat2=session.laps.pick_driver(j2).pick_lap(lapno)
        drv_tel2=driver_dat2.get_car_data().add_distance()
        delta_time, ref_tel, compare_tel = utils.delta_time(x1, driver_dat2)   
        ax[1].plot(ref_tel['Distance'],delta_time,linewidth=3, color=col_dict[j2])

ax[1].set_ylabel('Delta, s', fontweight='bold', fontsize=22)
ax[1].xaxis.set_tick_params(labelsize=25)
ax[1].yaxis.set_tick_params(labelsize=25)
ax[1].set_xlabel('Distance, m', fontweight='bold', fontsize=22)

if Fastestlap_Flag==1:
    plt.suptitle(f"Fastest Lap Comparison \n "
                 f"{session.event['EventName']} {session.event.year} {ssn_name}", 
                 fontsize=22, fontweight='bold')
else:
    plt.suptitle(f"One Lap Comparison \n "
                 f"{session.event['EventName']} {session.event.year} {ssn_name} - Lap 46", 
                 fontsize=22, fontweight='bold')
plt.show()




