# -*- coding: utf-8 -*-
"""
Created on Wed May 17 20:04:52 2023

@author: msrms
"""

import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

plotting.setup_mpl()
ff1.Cache.enable_cache('cache/')
# 1:1 - 1080x1080

# Inputs
Event_name='Bahrain Grand Prix'
Event_type='R'
year='2023'
drivers=['PER','HAM']

session = ff1.get_session(int(year), Event_name, Event_type)
curve_fit_flg=1 # 1-linear fit, 2-Quadratic fit
weekend = session.event
laps = session.load_laps(with_telemetry=True)
Dict_dr={}

    # Filter based on DRS zone distance
   
if Event_name=='Saudi Arabian Grand Prix':
    z1=[0,274]
    z2=[3653,3952]
    z3=[4679,5191]
    z4=[5833,10000]
    dict1={'z1':z1,
           'z2':z2,
           'z3':z3,
           'z4':z4}
    lap_nos=list(range(1,50))
    spd_filter_limit=75
    xlim1=[spd_filter_limit*3.6,340]
    ylim1=[0,6]
    xlim2=xlim1
    ylim2=[0,6]
    
elif Event_name=='Bahrain Grand Prix':
    z1=[0,525]
    z2=[1010, 1323]
    z3=[2801, 3165]
    z4=[5290, 10000]
    dict1={'z1':z1,
           'z2':z2,
           'z3':z3,
           'z4':z4}
    lap_nos=list(range(1,57))
    spd_filter_limit=55
    xlim1=[spd_filter_limit*3.6,340]
    ylim1=[0,10]
    xlim2=xlim1
    ylim2=[0,10]
    
elif Event_name=='Australian Grand Prix':
    z1=[0,232]
    z2=[676,954]
    z3=[2534,3112]
    z4=[3539,3914]
    z5=[4835,10000]
    dict1={'z1':z1,
           'z2':z2,
           'z3':z3,
           'z4':z4,
           'z5':z5}
    lap_nos=list(range(1,58))
    spd_filter_limit=66 #240 kmph
    xlim1=[spd_filter_limit*3.6,340]
    ylim1=[0,7]
    xlim2=xlim1
    ylim2=[0,7]
    
    
elif Event_name=='Azerbaijan Grand Prix':
    z1=[0,150]
    z2=[758,1297]
    z3=[5494,10000]
    dict1={'z1':z1,
           'z2':z2,
           'z3':z3}
    lap_nos=list(range(1,51))
    spd_filter_limit=55 #200kmph
    xlim1=[spd_filter_limit*3.6,350]
    ylim1=[0,11]
    xlim2=xlim1
    ylim2=[0,11]
    
    
elif Event_name=='Miami Grand Prix':
    z1=[0,170]
    z2=[2325,2874]
    z3=[4112,4564]
    z4=[5234,10000]
    dict1={'z1':z1,
           'z2':z2,
           'z3':z3,
           'z4':z4}
    lap_nos=list(range(1,57))
    spd_filter_limit=75
    xlim1=[spd_filter_limit*3.6,350]
    ylim1=[0,8]
    xlim2=xlim1
    ylim2=[0,5]
    
for j in drivers:
    laps_driver=laps.pick_driver(j)
   
    driver_tel=laps_driver.loc[laps_driver['LapNumber']==lap_nos[0]].get_car_data().add_distance()

    for L in lap_nos[1::]:
        dtl = laps_driver.loc[laps_driver['LapNumber']==L].get_car_data().add_distance()
        driver_tel=pd.concat([driver_tel,dtl],axis=0)
        tmp=driver_tel.loc[driver_tel['DRS']==12]
    #Covert spd to m/s
    driver_tel.Speed *= 0.2778

    # Estimate acceleration
    v1=driver_tel['Speed'].to_frame().drop([0]).to_numpy()
    dv1=driver_tel['Speed'].to_frame().diff(axis=0).dropna(axis=0)
    t1=driver_tel['Time'].to_frame().diff(axis=0).dropna(axis=0).Time.dt.total_seconds().to_frame()
    dv1.rename(columns = {'Speed':'X'}, inplace = True)
    t1.rename(columns = {'Time':'X'}, inplace = True)
    acc1=dv1.div(t1)
    acc1=acc1['X'].values.tolist()
    acc1.insert(0,0)
    driver_tel['Accel']=acc1

    # Speed filter
    driver_tel=driver_tel.loc[driver_tel['Speed']>spd_filter_limit]

    c=0
    for key in dict1:
        if c==0:
            dr_d=driver_tel.loc[(driver_tel['Distance']>dict1[key][0]) & (driver_tel['Distance']<dict1[key][1])]    
        else:
            dr_d2=driver_tel.loc[(driver_tel['Distance']>dict1[key][0]) & (driver_tel['Distance']<dict1[key][1])]
            dr_d=pd.concat([dr_d,dr_d2],axis=0)    
        c+=1
   
    # Remove Deceleration points
    dr_a=dr_d.loc[dr_d['Accel']>0]

    drtel_DRSoff=dr_a.loc[dr_a['DRS']==0]
    drtel_DRSon=dr_a.loc[dr_a['DRS']==12]
   
    drtel_DRSoff=drtel_DRSoff.sort_values(by=['Speed'], ascending=True)
    drtel_DRSon=drtel_DRSon.sort_values(by=['Speed'], ascending=True)
    min_DRSon_Spd = drtel_DRSon.Speed.min()
    drtel_DRSoff=drtel_DRSoff[drtel_DRSoff['Speed']>=min_DRSon_Spd]
   
    vel_DRSoff=drtel_DRSoff.Speed.to_numpy()
    acc_DRSoff=drtel_DRSoff.Accel.to_numpy()
   
    vel_DRSon=drtel_DRSon.Speed.to_numpy()
    acc_DRSon=drtel_DRSon.Accel.to_numpy()
       
    if curve_fit_flg == 1:
        def test(x, a, b):
            return a + b*x

        param1, _ = curve_fit(test, vel_DRSoff, acc_DRSoff)
        a1,b1=param1
        acc_Fit_DRSoff=test(vel_DRSoff, a1, b1)

        param2, _ = curve_fit(test, vel_DRSon, acc_DRSon)
        a2,b2=param2
        acc_Fit_DRSon=test(vel_DRSon, a2, b2)
   
    else:
         def test(x, a, b, c):
             return a*x + b*x**2 + c

         param1, _ = curve_fit(test, vel_DRSoff, acc_DRSoff)
         a1,b1,c1=param1
         acc_Fit_DRSoff=test(vel_DRSoff, a1, b1, c1)

         param2, _ = curve_fit(test, vel_DRSon, acc_DRSon)
         a2,b2,c2=param2
         acc_Fit_DRSon=test(vel_DRSon, a2, b2, c2)  
   
    # Estimate DRS Effectiveness

    # DRS on accel & speed @ Start
    acc_1 = test(vel_DRSoff[0], a2, b2)
    spd_1 = vel_DRSoff[0]
    # DRS on accel & speed @ End
    acc_2 = test(vel_DRSoff[-1], a2, b2)
    spd_2 = vel_DRSoff[-1]
    # DRS off accel & speed @ Start
    acc_3 = acc_Fit_DRSoff[0]
    spd_3 = vel_DRSoff[0]
    # DRS off accel & speed @ End
    acc_4 = acc_Fit_DRSoff[-1]
    spd_4 = vel_DRSoff[-1]
   
    acc_diff_start=round(acc_1-acc_3,2)
    acc_diff_end=round(acc_2-acc_4,2)
    avg_acc_diff = round((acc_diff_start+acc_diff_end)/2,2)
    print(j, acc_diff_start,acc_diff_end,avg_acc_diff)
    print(j, acc_1,acc_2,acc_3,acc_4)
    print(j, spd_1,spd_2,spd_3,spd_4)
   
    # Save to dictionary
    Dict_dr[j+'_1']=vel_DRSoff*3.6
    Dict_dr[j+'_2']=vel_DRSon*3.6
    Dict_dr[j+'_3']=acc_Fit_DRSoff
    Dict_dr[j+'_4']=acc_Fit_DRSon

    # Individual Driver Scatter plots
    fig, ax = plt.subplots(figsize=(12.5,12.5))
    driver_color = ff1.plotting.driver_color(j)

    ax.scatter(vel_DRSoff*3.6,acc_DRSoff,c=driver_color,marker='v',s=100,edgecolor='white')
    ax.scatter(vel_DRSon*3.6,acc_DRSon,c=driver_color,s=100,edgecolor='black')
    ax.plot(vel_DRSoff*3.6,acc_Fit_DRSoff,linewidth=5,color=driver_color)
    ax.plot(vel_DRSon*3.6,acc_Fit_DRSon,linestyle='dashed',
            dashes=[6, 2],linewidth=5,color='white')
    ax.set_title(f'{weekend.name} {year} - {j} - DRS Effectiveness',
                 fontsize=20, fontweight='bold')
    ax.set_xlabel('Speed, m/s',fontsize=20)
    ax.set_ylabel('Acceleration, m/s2',fontsize=20)
    ax.set_ylim(ylim1)
    ax.set_xlim(xlim1)
    ax.yaxis.set_tick_params(labelsize=18)
    ax.xaxis.set_tick_params(labelsize=18)
    ax.legend(['DRS OFF', 'DRS ON','Curve Fit DRS OFF','Curve Fit DRS ON'],handlelength=7)
    plt.text(xlim1[0],0.1,r'@f1_aerodynamicist',color='white',
             fontsize=18, fontweight='bold')
    plt.savefig(Event_name[:3]+'_'+j+'.png', dpi=100,bbox_inches="tight")

    del param2, param1, acc_Fit_DRSon, acc_Fit_DRSoff
plt.show()

# Compare across multiple Drivers
fig1, ax1 = plt.subplots(figsize=(12.5,12.5),dpi=100)
ax1.set_title(f'{weekend.name} {year} - DRS Effectiveness',
             fontsize=20, fontweight='bold')

for jj in drivers:
   
    driver_color1 = ff1.plotting.driver_color(jj)
   
    ax1.plot(Dict_dr[jj+'_1'],Dict_dr[jj+'_3'],c=driver_color1,
             label=jj+' DRS off',linewidth=5)
    ax1.plot(Dict_dr[jj+'_2'],Dict_dr[jj+'_4'],
             linestyle='dashed',c=driver_color1,label=jj+' DRS on',
             linewidth=5)

    ax1.set_xlabel('Speed, kmph',fontsize=20)
    ax1.set_ylabel('Acceleration, m/s2',fontsize=20)
    ax1.yaxis.set_tick_params(labelsize=20)
    ax1.xaxis.set_tick_params(labelsize=20)
    ax1.set_ylim(ylim2)
    ax1.set_xlim(xlim2)

plt.text(xlim2[0],0.15,r'@f1_aerodynamicist',color='white',
         fontsize=18, fontweight='bold')
plt.legend(fontsize=14, handlelength=5)
plt.savefig(Event_name[:3]+'_All.png', dpi=100,bbox_inches="tight")
plt.show()
