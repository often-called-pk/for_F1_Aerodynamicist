import os
import streamlit as st
import json
import subprocess

# Streamlit Web App Layout
st.title("F1 Telemetry Cornering Analysis")
st.write("Select the race details and drivers to generate the telemetry data.")

# Dropdown for Year Selection
year = st.selectbox('Select Year', list(range(2020, 2024)))

# Dropdown for Grand Prix selection
grand_prix = st.selectbox('Select Grand Prix', ['British Grand Prix', 'Monaco Grand Prix', 'Belgian Grand Prix'])  # Example list

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

# Save the inputs to a file for the second script to read
if st.button('Save Selection and Generate Plot'):
    input_data = {
        "year": year,
        "grand_prix": grand_prix,
        "drivers": [driver_1, driver_2, driver_3]
    }
    
    with open("input_data.json", "w") as file:
        json.dump(input_data, file)
    
    st.success("Input data saved! Generating the plot...")

    # Run the generate_plot.py script automatically in a new process
    try:
        # Call the generate_plot.py script using subprocess
        subprocess.Popen(['python', 'generate_plot.py'], shell=True)
        st.success("Plot is being generated in a separate window.")
    except Exception as e:
        st.error(f"Failed to run the plot generation script: {e}")
