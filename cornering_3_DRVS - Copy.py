import os
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from fastf1 import utils
import pandas as pd
from timple.timedelta import strftimedelta
import numpy as np
plotting.setup_mpl()

# Create the cache directory if it doesn't exist
cache_directory = 'cache/'
if not os.path.exists(cache_directory):
    os.makedirs(cache_directory)


ff1.Cache.enable_cache('cache/')
#=============================================================
ssn='RACE'
session = ff1.get_session(2023, 'British Grand Prix', ssn)
session.load(weather=False)
Fastestlap_Flag=1
drivers=['NOR','HAM','VER','PER','LEC','SAI','RUS','ALO','STR','PIA']
lapnos=46,46,46
distance_min, distance_max = 1140, 2400
turn_nos={"Turn-1":1520,"Turn-2":2000}
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

plt.rcParams["figure.autolayout"] = True

telemetry_colors = {
    'Full Throttle': 'green',
    'Turning': 'Yellow',
    'Brake': 'red',
    }
plt.style.use('dark_background')

fig, ax = plt.subplots(2, figsize=(20, 11.25), gridspec_kw={'height_ratios': [
                           3, 1]})
    
for dr in drivers:
    # Extracting the laps
    if Fastestlap_Flag == 1:
        laps_driver=session.laps.pick_driver(dr).pick_fastest()
    else:
        laps_driver=session.laps.pick_driver(dr).pick_lap(lapnos[0])

    driver_color = col_dict[dr]
    telemetry_driver = laps_driver.get_car_data().add_distance()


    # Assigning labels to what the drivers are currently doing
    telemetry_driver.loc[telemetry_driver['Brake']
                           > 0, 'CurrentAction'] = 'Brake'
    telemetry_driver.loc[telemetry_driver['Throttle']
                           > 96, 'CurrentAction'] = 'Full Throttle'
    telemetry_driver.loc[(telemetry_driver['Brake'] == 0) & (
        telemetry_driver['Throttle'] < 96), 'CurrentAction'] = 'Turning'

    # Numbering each unique action to identify changes
    telemetry_driver['ActionID'] = (
        telemetry_driver['CurrentAction'] != telemetry_driver['CurrentAction'].shift(1)).cumsum()
    actions_driver = telemetry_driver[['ActionID', 'CurrentAction', 'Distance']].groupby(
        ['ActionID', 'CurrentAction']).max('Distance').reset_index()
    
    actions_driver['Driver'] = dr

    # Calculating the distance between each action
    actions_driver['DistanceDelta'] = actions_driver['Distance'] - \
        actions_driver['Distance'].shift(1)
    actions_driver.loc[0, 'DistanceDelta'] = actions_driver.loc[0, 'Distance']

    if dr==drivers[0]:
        all_actions=actions_driver
    else:
        all_actions = all_actions._append(actions_driver)

    # Lineplot for speed
    ax[0].tick_params(bottom = False)

    ax[0].plot(telemetry_driver['Distance'], telemetry_driver['Speed'],
               label=dr, color=driver_color, linewidth=3)

ax[0].set_ylabel('Speed', fontweight='bold', fontsize=25)
ax[0].legend(loc="lower right", fontsize=23)
ax[0].tick_params(axis='y', which='major', labelsize=22)
ax[0].set_xlim(distance_min, distance_max)

y1=ax[0].get_ylim()
for g in turn_nos:
    ax[0].axvline(x = turn_nos[g], color = 'yellow', linestyle = '--')
    k1 = [k0 for k0, v0 in turn_nos.items() if v0 == turn_nos[g]][0]
    ax[0].text(turn_nos[g],y1[0]+20,k1,color='black',
               fontsize=17, fontweight='bold',backgroundcolor='white')
    
# Horizontal barplot for telemetry
for driver in drivers:
    driver_actions = all_actions.loc[all_actions['Driver'] == driver]

    previous_action_end = 0
    for _, action in driver_actions.iterrows():
        ax[1].barh(
            [driver],
            action['DistanceDelta'],
            left=previous_action_end,
            color=telemetry_colors[action['CurrentAction']]
        )

        previous_action_end = previous_action_end + action['DistanceDelta']

# Set x-label
plt.xlabel('Distance', fontweight='bold', fontsize=25)

# Invert y-axis
plt.gca().invert_yaxis()

# Remove frame from plot
ax[1].spines['top'].set_visible(False)
ax[1].spines['right'].set_visible(False)
ax[1].spines['left'].set_visible(False)
# ax[0].tick_params(axis='y', which='major', labelsize=22)
# ax[0].tick_params(axis='x', which='major', labelsize=15)

# Add legend
labels = list(telemetry_colors.keys())
handles = [plt.Rectangle((0, 0), 1, 1, color=telemetry_colors[label])
           for label in labels]
ax[1].legend(handles, labels, fontsize=20,ncol=3,bbox_to_anchor=(0.0, 1.00))
ax[1].tick_params(axis='both', which='major', labelsize=22)

# Zoom in on the specific part we want to see
ax[1].set_xlim(distance_min, distance_max)
plt.suptitle(
    f"{session.event.year} {session.event['EventName']}({ssn})\n"
    f"Corner Analysis {drivers[0]} vs {drivers[1]} vs {drivers[2]}", fontsize=20, fontweight='bold')
# Save the plot
plt.show()
