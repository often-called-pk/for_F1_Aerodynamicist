import os
import json
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
import numpy as np
import matplotlib
from matplotlib.ticker import MultipleLocator

# Ensure we are using an interactive backend (TkAgg)
matplotlib.use('TkAgg')

# Set dark background for plots
plt.style.use('dark_background')

# Read input data from the JSON file
with open("input_data.json", "r") as file:
    input_data = json.load(file)

year = input_data["year"]
grand_prix = input_data["grand_prix"]
drivers = input_data["drivers"]

# Create the cache directory if it doesn't exist
cache_directory = 'cache/'
if not os.path.exists(cache_directory):
    os.makedirs(cache_directory)

ff1.Cache.enable_cache('cache/')

# Plotting setup
col_dict = {
    "PER": "Blue", "VER": "Blue", "LEC": "Red", "SAI": "Red", "RUS": "Cyan",
    "HAM": "Cyan", "ALO": "Green", "STR": "Green", "PIA": "#ff8700", 
    "NOR": "#ff8700", "ALB": "#005aff", "GAS": "#0090ff", "OCO": "#0090ff"
}

distance_min, distance_max = 1140, 2400
turn_nos = {"Turn-1": 1520, "Turn-2": 2000}

telemetry_colors = {
    'Full Throttle': 'green', 'Turning': 'yellow', 'Brake': 'red'
}

# Load the selected session data
session = ff1.get_session(year, grand_prix, 'RACE')
session.load(weather=False)

# Create figure window with Matplotlib
fig, ax = plt.subplots(2, figsize=(20, 12), gridspec_kw={'height_ratios': [3, 1]})

# Synchronize zoom functionality between both subplots with a flag to prevent recursion
syncing = False

def on_xlims_change(event_ax):
    global syncing
    if not syncing:  # Only sync when not already syncing
        syncing = True
        new_xlim = event_ax.get_xlim()
        ax[0].set_xlim(new_xlim)
        ax[1].set_xlim(new_xlim)
        fig.canvas.draw_idle()
        syncing = False  # Reset the flag after syncing

# Loop over selected drivers and extract telemetry data
for dr in drivers:
    laps_driver = session.laps.pick_driver(dr).pick_fastest()
    driver_color = col_dict[dr]
    telemetry_driver = laps_driver.get_car_data().add_distance()

    # Label actions: Brake, Full Throttle, and Turning
    telemetry_driver.loc[telemetry_driver['Brake'] > 0, 'CurrentAction'] = 'Brake'
    telemetry_driver.loc[telemetry_driver['Throttle'] > 96, 'CurrentAction'] = 'Full Throttle'
    telemetry_driver.loc[(telemetry_driver['Brake'] == 0) & (telemetry_driver['Throttle'] < 96), 'CurrentAction'] = 'Turning'

    telemetry_driver['ActionID'] = (telemetry_driver['CurrentAction'] != telemetry_driver['CurrentAction'].shift(1)).cumsum()
    actions_driver = telemetry_driver[['ActionID', 'CurrentAction', 'Distance']].groupby(['ActionID', 'CurrentAction']).max('Distance').reset_index()

    actions_driver['Driver'] = dr
    actions_driver['DistanceDelta'] = actions_driver['Distance'] - actions_driver['Distance'].shift(1)
    actions_driver.loc[0, 'DistanceDelta'] = actions_driver.loc[0, 'Distance']

    # Plot speed on the first subplot
    ax[0].plot(telemetry_driver['Distance'], telemetry_driver['Speed'], label=dr, color=driver_color, linewidth=3)

    # Add turns to the first plot
    for g in turn_nos:
        ax[0].axvline(x=turn_nos[g], color='yellow', linestyle='--', zorder=1)
        ax[0].text(turn_nos[g], 0, g, color='black', fontsize=17, fontweight='bold', backgroundcolor='white')

ax[0].set_ylabel('Speed', fontweight='bold', fontsize=25)
ax[0].legend(loc="lower right", fontsize=20)
ax[0].set_xlim(distance_min, distance_max)

# Enable grid for the first subplot with a less prominent appearance
ax[0].grid(True, which='both', color='gray', alpha=0.3, linewidth=0.5, zorder=0)  # Grid behind the plot

# Increase x-axis grid frequency by setting minor ticks and grid lines
ax[0].xaxis.set_minor_locator(MultipleLocator(50))  # More frequent minor ticks
ax[0].grid(True, which='minor', color='gray', alpha=0.3, linewidth=0.3, zorder=0)  # Finer grid for minor ticks

# Horizontal bar plot for telemetry actions in the second subplot
y_positions = [0, 1, 2]  # We will display drivers in order of selection
for i, dr in enumerate(drivers):  # Enumerate to maintain selection order
    laps_driver = session.laps.pick_driver(dr).pick_fastest()
    telemetry_driver = laps_driver.get_car_data().add_distance()

    telemetry_driver.loc[telemetry_driver['Brake'] > 0, 'CurrentAction'] = 'Brake'
    telemetry_driver.loc[telemetry_driver['Throttle'] > 96, 'CurrentAction'] = 'Full Throttle'
    telemetry_driver.loc[(telemetry_driver['Brake'] == 0) & (telemetry_driver['Throttle'] < 96), 'CurrentAction'] = 'Turning'

    telemetry_driver['ActionID'] = (telemetry_driver['CurrentAction'] != telemetry_driver['CurrentAction'].shift(1)).cumsum()
    actions_driver = telemetry_driver[['ActionID', 'CurrentAction', 'Distance']].groupby(['ActionID', 'CurrentAction']).max('Distance').reset_index()

    actions_driver['Driver'] = dr
    actions_driver['DistanceDelta'] = actions_driver['Distance'] - actions_driver['Distance'].shift(1)
    actions_driver.loc[0, 'DistanceDelta'] = actions_driver.loc[0, 'Distance']

    previous_action_end = 0
    for _, action in actions_driver.iterrows():
        ax[1].barh(y_positions[i], action['DistanceDelta'], left=previous_action_end, color=telemetry_colors[action['CurrentAction']], zorder=2)
        previous_action_end += action['DistanceDelta']

ax[1].set_xlim(distance_min, distance_max)
ax[1].set_yticks(y_positions)
ax[1].set_yticklabels(drivers)  # Make sure y-tick labels match driver order
ax[1].invert_yaxis()  # Invert to match standard telemetry view
plt.xlabel('Distance', fontweight='bold', fontsize=25)

# Enable grid for the second subplot with a less prominent appearance
ax[1].grid(True, which='both', color='gray', alpha=0.3, linewidth=0.5, zorder=0)  # Grid behind the plot

# Increase x-axis grid frequency in the second subplot
ax[1].xaxis.set_minor_locator(MultipleLocator(50))  # More frequent minor ticks
ax[1].grid(True, which='minor', color='gray', alpha=0.3, linewidth=0.3, zorder=0)  # Finer grid for minor ticks

# Title for the plot
plt.suptitle(f"{session.event.year} {session.event['EventName']} (RACE)\n Corner Analysis {drivers[0]} vs {drivers[1]} vs {drivers[2]}", fontsize=20, fontweight='bold')

# Add the legend for telemetry actions, making it smaller and ensuring it doesn't overlap
labels = list(telemetry_colors.keys())
handles = [plt.Rectangle((0, 0), 1, 1, color=telemetry_colors[label]) for label in labels]
ax[1].legend(handles, labels, fontsize=10, ncol=3, bbox_to_anchor=(0.0, -0.3), loc='upper left', borderaxespad=0.1)

# Add x-axis change event listener for synchronized zoom
ax[0].callbacks.connect('xlim_changed', on_xlims_change)
ax[1].callbacks.connect('xlim_changed', on_xlims_change)

# Adjust layout to ensure there's enough space between subplots and the legend
plt.subplots_adjust(hspace=0.5)

# Show the plot in an interactive Matplotlib window
plt.show()
