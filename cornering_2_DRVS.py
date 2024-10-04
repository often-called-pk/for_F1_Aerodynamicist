
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
ssn='RACE'
session = ff1.get_session(2023, 'British Grand Prix', ssn)
session.load(weather=False)
Fastestlap_Flag=1
drivers=['NOR','HAM']
lapnos=46,46
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

# Extracting the laps
if Fastestlap_Flag == 1:
    laps_driver1=session.laps.pick_driver(drivers[0]).pick_fastest()
    laps_driver2=session.laps.pick_driver(drivers[1]).pick_fastest()
else:
    laps_driver1=session.laps.pick_driver(drivers[0]).pick_lap(lapnos[0])
    laps_driver2=session.laps.pick_driver(drivers[1]).pick_lap(lapnos[1])
    
driver1_color = col_dict[drivers[0]]
driver2_color = col_dict[drivers[1]]

telemetry_driver_1 = laps_driver1.get_car_data().add_distance()
telemetry_driver_2 = laps_driver2.get_car_data().add_distance()

# Assigning labels to what the drivers are currently doing
telemetry_driver_1.loc[telemetry_driver_1['Brake']
                       > 0, 'CurrentAction'] = 'Brake'
telemetry_driver_1.loc[telemetry_driver_1['Throttle']
                       > 96, 'CurrentAction'] = 'Full Throttle'
telemetry_driver_1.loc[(telemetry_driver_1['Brake'] == 0) & (
    telemetry_driver_1['Throttle'] < 96), 'CurrentAction'] = 'Turning'

telemetry_driver_2.loc[telemetry_driver_2['Brake']
                       > 0, 'CurrentAction'] = 'Brake'
telemetry_driver_2.loc[telemetry_driver_2['Throttle']
                       > 96, 'CurrentAction'] = 'Full Throttle'
telemetry_driver_2.loc[(telemetry_driver_2['Brake'] == 0) & (
    telemetry_driver_2['Throttle'] < 96), 'CurrentAction'] = 'Turning'

# Numbering each unique action to identify changes
telemetry_driver_1['ActionID'] = (
    telemetry_driver_1['CurrentAction'] != telemetry_driver_1['CurrentAction'].shift(1)).cumsum()
telemetry_driver_2['ActionID'] = (
    telemetry_driver_2['CurrentAction'] != telemetry_driver_2['CurrentAction'].shift(1)).cumsum()
actions_driver_1 = telemetry_driver_1[['ActionID', 'CurrentAction', 'Distance']].groupby(
    ['ActionID', 'CurrentAction']).max('Distance').reset_index()
actions_driver_2 = telemetry_driver_2[['ActionID', 'CurrentAction', 'Distance']].groupby(
    ['ActionID', 'CurrentAction']).max('Distance').reset_index()

actions_driver_1['Driver'] = drivers[0]
actions_driver_2['Driver'] = drivers[1]

# Calculating the distance between each action
actions_driver_1['DistanceDelta'] = actions_driver_1['Distance'] - \
    actions_driver_1['Distance'].shift(1)
actions_driver_1.loc[0, 'DistanceDelta'] = actions_driver_1.loc[0, 'Distance']

actions_driver_2['DistanceDelta'] = actions_driver_2['Distance'] - \
    actions_driver_2['Distance'].shift(1)
actions_driver_2.loc[0, 'DistanceDelta'] = actions_driver_2.loc[0, 'Distance']
all_actions = actions_driver_1.append(actions_driver_2)
# Calculating average speed
avg_speed_driver_1 = np.mean(telemetry_driver_1['Speed'].loc[
    (telemetry_driver_1['Distance'] >= distance_min) &
    (telemetry_driver_1['Distance'] <= distance_max)
])


avg_speed_driver_2 = np.mean(telemetry_driver_2['Speed'].loc[
    (telemetry_driver_2['Distance'] >= distance_min) &
    (telemetry_driver_2['Distance'] <= distance_max)
])

if avg_speed_driver_1 > avg_speed_driver_2:
    speed_text = f"{drivers[0]} {round(avg_speed_driver_1 - avg_speed_driver_2,2)}km/h faster"
else:
    speed_text = f"{drivers[1]} {round(avg_speed_driver_2 - avg_speed_driver_1,2)}km/h faster"

plt.rcParams["figure.autolayout"] = True

telemetry_colors = {
    'Full Throttle': 'green',
    'Turning': 'Yellow',
    'Brake': 'red',
}
plt.style.use('dark_background')

fig, ax = plt.subplots(2, figsize=(20, 11.25), gridspec_kw={'height_ratios': [
                       3, 1]})

# Lineplot for speed
ax[0].tick_params(bottom = False)

ax[0].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Speed'],
           label=drivers[0], color=driver1_color, linewidth=3)
ax[0].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Speed'],
           label=drivers[1], color=driver2_color, linewidth=3, linestyle='-')

y1=ax[0].get_ylim()
for g in turn_nos:
    ax[0].axvline(x = turn_nos[g], color = 'yellow', linestyle = '--')
    k1 = [k0 for k0, v0 in turn_nos.items() if v0 == turn_nos[g]][0]
    ax[0].text(turn_nos[g],y1[0]+20,k1,color='black',
               fontsize=17, fontweight='bold',backgroundcolor='white')

ax[0].set_ylabel('Speed', fontweight='bold', fontsize=25)
ax[0].legend(loc="lower right", fontsize=23)
ax[0].tick_params(axis='y', which='major', labelsize=22)
ax[0].set_xlim(distance_min, distance_max)

delta_time, ref_tel, compare_tel = utils.delta_time(
    laps_driver1, laps_driver2) 
twin = ax[0].twinx()
twin.plot(ref_tel['Distance'], delta_time, '--', linewidth=2.75, color='white')
twin.axhline(y = 0, color = 'r', linestyle = '-.')
twin.set_ylabel(f"Gap to fastest", fontweight='bold', fontsize=20)
# twin.set_ylim(0.0,0.5)
twin.yaxis.set_tick_params(labelsize=25)
# twin.text(0,100,'')

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
    f"Corner Analysis {drivers[0]} vs {drivers[1]} (TURN-2&3)", fontsize=20, fontweight='bold')
# Save the plot
plt.show()
