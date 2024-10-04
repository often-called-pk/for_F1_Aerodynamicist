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
lapmin, lapmax = 1, 52
laps = session.load_laps()
laptymfilter_upper=200
laptymfilter_low=0
drivers_to_visualize = ['VER', 'PER', 'ALO', 'RUS', 'SAI', 'HAM', 'LEC', 'GAS', 'OCO']
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
for col in drivers_to_visualize:
    colours.append(col_dict[col])

laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()
laps = laps.loc[(laps['PitOutTime'].isnull() & laps['PitInTime'].isnull())]
# load_laps = np.array(laps['LapTimeSeconds'])
laps2 = laps['LapTimeSeconds']
filtered_laps = list()

for laps1 in laps2:
    if laps1 > lapmin and laps1 < lapmax:
        filtered_laps.append(laps1)
    else:
        filtered_laps.append(None)

laps['loaded'] = filtered_laps
q75, q25 = laps['loaded'].quantile(
    0.75), laps['loaded'].quantile(0.25)

intr_qr = q75-q25
print(intr_qr)
print(q75)
print(q25)
laptime_max = q75+(1.5*intr_qr)
laptime_min = q25-(1.5*intr_qr)
laps.loc[laps['loaded'] < laptime_min, 'loaded'] = np.nan
laps.loc[laps['loaded'] > laptime_max, 'loaded'] = np.nan

sns.set_palette(colours)
plt.style.use('dark_background')

laps.to_pickle("dummy.pkl")
laps.rename(columns = {'loaded':'Lap Time (s)'}, inplace = True)
laps=laps.loc[laps['Driver'].isin(drivers_to_visualize)]
DR_list=[]
DR1_list=['VER','HAM','LEC','GAS','ALO','NOR','TSU','HUL','BOT','ALB']
DR2_list=['PER','RUS','SAI','OCO','STR','PIA','DEV','MAG','ZHO','SAR']
for k in laps.Driver:
    if k in DR1_list:
        DR_list.append('Driver_1')
    elif k in DR2_list:
        DR_list.append('Driver_2')
laps['DR_cat']=DR_list
Dr_combo=[]
for k1 in laps.Team:
    if k1 == 'Red Bull Racing':
        Dr_combo.append('VER | PER')
    elif k1 == 'Aston Martin':
        Dr_combo.append('ALO | STR')
    elif k1 == 'Mercedes':
        Dr_combo.append('HAM | RUS')
    elif k1 == 'Ferrari':
        Dr_combo.append('LEC | SAI')
    elif k1 == 'Alpine':
        Dr_combo.append('GAS | OCO')
    elif k1 == 'Haas F1 Team':
        Dr_combo.append('HUL | MAG')
    elif k1 == 'AlphaTauri':
        Dr_combo.append('TSU | DEV')
    elif k1 == 'Alfa Romeo':
        Dr_combo.append('BOT | ZHO')
    elif k1 == 'McLaren':
        Dr_combo.append('NOR | PIA')
    elif k1 == 'Williams':
        Dr_combo.append('ALB | SAR')
laps['Dr_combo']=Dr_combo

        
laps=laps.dropna(subset=['LapTimeSeconds'])
laps=laps.loc[laps['LapTimeSeconds']<laptymfilter_upper]
laps=laps.loc[laps['LapTimeSeconds']>=laptymfilter_low]

titl = str(session.event.year) +' '+session.event['EventName']+' \n'+'Race Pace Distribution'
   
fig, ax = plt.subplots(figsize=(19.20, 10.8), dpi=100)

sns.violinplot(x="Driver", y="LapTimeSeconds",
                    data=laps, palette=colours, split=False,
                    scale="count", 
                    order = drivers_to_visualize, legend=False)
sns.stripplot(data=laps, x="Driver", y="LapTimeSeconds",hue="Compound",
              order = drivers_to_visualize,
              palette=['White','Yellow'], marker="o", 
              edgecolor="Black",linewidth=1,s=10)

plt.ylim(88,97)
ax.xaxis.set_tick_params(labelsize=25)
ax.yaxis.set_tick_params(labelsize=25)
ax.legend(fontsize=20,markerscale=2)
plt.ylabel('Laptime (s)', fontweight='bold', fontsize=26)
plt.xlabel('Drivers', fontweight='bold', fontsize=26)
plt.suptitle(
    f" Race Pace \n"
    f"{session.event.year} {session.event['EventName']} ({event}) ", fontsize=25, fontweight='bold')
plt.grid(alpha=1, which='both', color='0.65', linestyle='-')

# assign race strategy
RS=['H|M','M|H','M|H','M|H','M|H','H|M','M|H','M|H','H|M']
for j in range(len(RS)):
    ax.text(drivers_to_visualize[j],88.5,RS[j],color='black',
              fontsize=20, fontweight='bold',backgroundcolor='white', 
              bbox=dict(facecolor='white',boxstyle='round'))

resolution_value = 100
plt.savefig("ViolinPlots.png", format="png", dpi=resolution_value)
