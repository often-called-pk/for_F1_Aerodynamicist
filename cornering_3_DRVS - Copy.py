import os
import streamlit as st
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.widgets import RectangleSelector
import numpy as np

plotting.setup_mpl(misc_mpl_mods=False)

# Create the cache directory if it doesn't exist
cache_directory = 'cache/'
if not os.path.exists(cache_directory):
    os.makedirs(cache_directory)

ff1.Cache.enable_cache('cache/')

# Streamlit Web App Layout
st.title("F1 Telemetry Cornering Analysis")
st.write("Select the race details and drivers to generate the telemetry data.")

# Dropdown for Year Selection
year = st.selectbox('Select Year', list(range(2020, 2024)))

# Get all available grand prix sessions for the selected year
available_grands_prix = ff1.get_event_schedule(year)
gp_names = available_grands_prix['EventName'].unique()

# Dropdown for Grand Prix selection
grand_prix = st.selectbox('Select Grand Prix', gp_names)

# Driver Selection
all_drivers = ['HAM', 'VER', 'NOR', 'LEC', 'SAI', 'RUS', 'ALO', 'STR', 'PIA', 'ALB', 'GAS', 'OCO']  # Shortened for simplicity

# Driver 1 Selection
driver_1 = st.selectbox('Select Driver 1', all_drivers)

# Remove the selected driver from the choices for the next driver
remaining_drivers = [d for d in all_drivers if d != driver_1]

# Driver 2 Selection
driver_2 = st.selectbox('Select Driver 2', remaining_drivers)

# Remove the selected driver from the choices for the next driver
remaining_drivers = [d for d in remaining_drivers if d != driver_2]

# Driver 3 Selection
driver_3 = st.selectbox('Select Driver 3', remaining_drivers)

# Synchronize zoom functionality
def on_xlims_change(event_ax):
    new_xlim = event_ax.get_xlim()
    ax[0].set_xlim(new_xlim)
    ax[1].set_xlim(new_xlim)
    fig.canvas.draw_idle()

# Proceed to load data and generate plot once selections are done
if st.button('Generate Telemetry Plot'):
    # Load the selected session data
    try:
        session = ff1.get_session(year, grand_prix, 'RACE')
        session.load(weather=False)
    except Exception as e:
        st.error(f"Error loading session data: {e}")
        st.stop()
    
    drivers = [driver_1, driver_2, driver_3]
    
    # Plotting setup
    col_dict = {
        "PER": "Blue", "VER": "Blue", "LEC": "Red", "SAI": "Red", "RUS": "Cyan",
        "HAM": "Cyan", "ALO": "Green", "STR": "Green", "PIA": "#ff8700", 
        "NOR": "#ff8700", "ALB": "#005aff", "GAS": "#0090ff", "OCO": "#0090ff"
    }
    
    distance_min, distance_max = 1140, 2400
    turn_nos = {"Turn-1": 1520, "Turn-2": 2000}
    
    telemetry_colors = {
        'Full Throttle': 'green', 'Turning': 'Yellow', 'Brake': 'red'
    }

    # Create figure window with Matplotlib
    fig, ax = plt.subplots(2, figsize=(20, 11.25), gridspec_kw={'height_ratios': [3, 1]})

    # Loop over selected drivers and extract telemetry data
    for dr in drivers:
        try:
            laps_driver = session.laps.pick_driver(dr).pick_fastest()
            driver_color = col_dict[dr]
            telemetry_driver = laps_driver.get_car_data().add_distance()

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

            for g in turn_nos:
                ax[0].axvline(x=turn_nos[g], color='yellow', linestyle='--')
                ax[0].text(turn_nos[g], 0, g, color='black', fontsize=17, fontweight='bold', backgroundcolor='white')

        except Exception as e:
            st.warning(f"Telemetry data for driver {dr} could not be loaded: {e}")
            continue

    ax[0].set_ylabel('Speed', fontweight='bold', fontsize=25)
    ax[0].legend(loc="lower right", fontsize=23)
    ax[0].set_xlim(distance_min, distance_max)

    # Horizontal bar plot for telemetry actions
    y_positions = [0, 1, 2]  # Three rows for three drivers
    for i, driver in enumerate(drivers):
        driver_actions = actions_driver[actions_driver['Driver'] == driver]
        previous_action_end = 0
        
        for _, action in driver_actions.iterrows():
            ax[1].barh(y_positions[i], action['DistanceDelta'], left=previous_action_end, color=telemetry_colors[action['CurrentAction']])
            previous_action_end += action['DistanceDelta']

    ax[1].set_xlim(distance_min, distance_max)
    ax[1].set_yticks(y_positions)
    ax[1].set_yticklabels(drivers)
    ax[1].invert_yaxis()  # Invert to match standard telemetry view
    plt.xlabel('Distance', fontweight='bold', fontsize=25)
    plt.suptitle(f"{session.event.year} {session.event['EventName']} (RACE)\n Corner Analysis {driver_1} vs {driver_2} vs {driver_3}", fontsize=20, fontweight='bold')

    # Add x-axis change event listener for synchronized zoom
    ax[0].callbacks.connect('xlim_changed', on_xlims_change)
    ax[1].callbacks.connect('xlim_changed', on_xlims_change)

    # Display the plot in a Matplotlib window
    plt.show()
