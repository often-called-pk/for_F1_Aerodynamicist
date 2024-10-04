
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator

pd.options.mode.chained_assignment = None
ff1.Cache.enable_cache('cache/')

# Inputs
session = ff1.get_session(2023, 'Miami Grand Prix', 'FP2')
drivers=['VER','SAI','PER','ALO','NOR','HAM','STR','OCO','ALB']
year='2023'

weekend = session.event
laps = session.load_laps(with_telemetry=True)
# -----------------------------------------------
colours = []
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
for col in drivers:
    colours.append(col_dict[col])

DRS_on_max_speed=[]
DRS_off_max_speed=[]
Delta=[]

for j in drivers:
    laps_driver=laps.pick_driver(j)
    driver_tel=laps_driver.get_car_data().add_distance()
       
    DRS_on_data=driver_tel.loc[(driver_tel['DRS']==12) | (driver_tel['DRS']==14) | (driver_tel['DRS']==10) ]
    DRS_off_data=driver_tel.loc[(driver_tel['DRS']==9) | (driver_tel['DRS']==13) | (driver_tel['DRS']==11) | (driver_tel['DRS']==8)]
    
    print(j)
    print(driver_tel.DRS.unique())
    print(DRS_on_data['Speed'].max(),DRS_off_data['Speed'].max())
    
    DRS_on_max_speed.append(DRS_on_data['Speed'].max())
    DRS_off_max_speed.append(DRS_off_data['Speed'].max())
    Delta.append(round(DRS_on_data['Speed'].max()-DRS_off_data['Speed'].max(),1))
 
fig, ax = plt.subplots(figsize=(19.20, 10.80), dpi=100)
x = np.arange(len(drivers))  # the label locations
w = 0.25  # the width of the bars

ax.bar(x, DRS_on_max_speed, width=0.25, color = 'b',
        edgecolor = 'black',
        label='DRS ON SPEED')
ax.bar(x+w, DRS_off_max_speed, width=0.25, color = 'g',
        edgecolor = 'black',
        label='DRS OFF SPEED')

ax.set_ylabel('Max Speed (Kmph)', fontsize=25, fontweight='bold')
ax.set_title(f" MAX SPEED COMPARISON : DRS-ON & DRS-OFF  \n"
    f"{session.event.year} {session.event['EventName']} {'- FP2'} ", fontsize=25, fontweight='bold')
ax.legend(loc='upper left',fontsize=20)
ax.set_ylim(320, 360)
ax.yaxis.set_minor_locator(MultipleLocator(5))
# Customize the major grid
#ax.grid(which='major', linestyle='-', linewidth='0.5', color='black')
# Customize the minor grid
#ax.grid(which='minor', linestyle='-.', linewidth='0.5', color='black')
ax.xaxis.set_tick_params(labelsize=25)
ax.yaxis.set_tick_params(labelsize=25)

for k in range(len(drivers)):
    ax.text(x[k], DRS_on_max_speed[k]+1, r'$\Delta$'+str(Delta[k]), ha='center',fontsize=20, fontweight='bold')

ax.set_xticks(list(x))
ax.set_xticklabels(drivers)