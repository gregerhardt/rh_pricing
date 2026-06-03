# -*- coding: utf-8 -*-
"""
Created on Thu May 15 15:02:32 2025

@author: Zhihua
"""
import os
import time
import timeit
import csv
import numpy as np
import pandas as pd
import array as arr
import glob
import re
os.chdir('C:\\Users\\Zhihua\\Documents\\MyResearch\\ChicagoData\\trips')
datawd = pd.read_csv("tncFJSD_23_wkdy.csv")
#%%
datawd["month"] = datawd.sdate.str[:7]
junwd = datawd[datawd.month.isin(["2023-06"])]
junwd.drop('month', axis=1, inplace=True)
junwd.to_csv("2023junwd.csv", sep=',', index=False, encoding='utf-8')
#%% read and seperate data by time slot
os.chdir('C:\\Users\\Zhihua\\Documents\\MyResearch\\ChicagoData\\TravelTimeAlex\\python\\Chi_Data_Wrangler\\Outputs\\OTP Travel Times\\Transit\\20190605\\all')
time_dfs = {}
files = glob.glob("traveltime_matrix_*-*.csv")
# Loop through files and assign them as time0, time1, etc.
for i, file in enumerate(sorted(files)):
    os.chdir('C:\\Users\\Zhihua\\Documents\\MyResearch\\ChicagoData\\TravelTimeAlex\\python\\Chi_Data_Wrangler\\Outputs\\OTP Travel Times\\Transit\\20190605\\all')
    df = pd.read_csv(file)#time_dfs[f'time{i}'] 
    df['tran_time'] = df['travel_time'] + df['walk_distance']/5
    df.drop('year', axis=1, inplace=True)
    df['od'] = df.origin.astype(str)+df.destination.astype(str)
    os.chdir('C:\\Users\\Zhihua\\Documents\\MyResearch\\ChicagoData\\trips\\alextime')
    df.to_csv(f'tt_{i}.csv', sep=',', index=True, encoding='utf-8')
os.chdir('C:\\Users\\Zhihua\\Documents\\MyResearch\\ChicagoData\\trips\\alextime')
time_dfs = {}
for i in range(24):
    time_dfs[f'time{i}'] = pd.read_csv(f"tt_{i}.csv")
#%% define slot
# transitTimePeriod: transit assignment time-of-day period
#  		- 1 = overnight/early morning (10pm - 6am)
# 		- 3 = AM peak (6am - 8am)
#  		- 5 = midday (9am - 4pm)
#  		- 7 = PM peak (4pm - 6pm) 
slot6 = [' 06:45:00 AM', ' 06:30:00 AM', ' 06:15:00 AM', ' 06:00:00 AM']
slot5 = [' 05:45:00 AM', ' 05:30:00 AM', ' 05:15:00 AM', ' 05:00:00 AM']
slot4 = [' 04:45:00 AM', ' 04:30:00 AM', ' 04:15:00 AM', ' 04:00:00 AM']
slot3 = [' 03:45:00 AM', ' 03:30:00 AM', ' 03:15:00 AM', ' 03:00:00 AM']
slot2 = [' 02:45:00 AM', ' 02:30:00 AM', ' 02:15:00 AM', ' 02:00:00 AM']
slot1 = [' 01:45:00 AM', ' 01:30:00 AM', ' 01:15:00 AM', ' 01:00:00 AM']
slot0 = [' 12:45:00 AM', ' 12:30:00 AM', ' 12:15:00 AM', ' 12:00:00 AM']
slot23 = [' 11:45:00 PM', ' 11:30:00 PM', ' 11:15:00 PM', ' 11:00:00 PM'] 
slot22 = [' 10:45:00 PM', ' 10:30:00 PM', ' 10:15:00 PM', ' 10:00:00 PM'] 
slot21 = [' 09:45:00 PM', ' 09:30:00 PM', ' 09:15:00 PM', ' 09:00:00 PM']
slot20 = [' 08:45:00 PM', ' 08:30:00 PM', ' 08:15:00 PM', ' 08:00:00 PM']
slot19 = [' 07:45:00 PM', ' 07:30:00 PM', ' 07:15:00 PM', ' 07:00:00 PM']
slot18 = [' 06:45:00 PM', ' 06:30:00 PM', ' 06:15:00 PM', ' 06:00:00 PM']
slot17 = [' 05:45:00 PM', ' 05:30:00 PM', ' 05:15:00 PM', ' 05:00:00 PM']
slot16 = [' 04:45:00 PM', ' 04:30:00 PM', ' 04:15:00 PM', ' 04:00:00 PM']
slot15 = [' 03:45:00 PM', ' 03:30:00 PM', ' 03:15:00 PM', ' 03:00:00 PM']
slot14 = [' 02:45:00 PM', ' 02:30:00 PM', ' 02:15:00 PM', ' 02:00:00 PM']
slot13 = [' 01:45:00 PM', ' 01:30:00 PM', ' 01:15:00 PM', ' 01:00:00 PM']
slot12 = [' 12:45:00 PM', ' 12:30:00 PM', ' 12:15:00 PM', ' 12:00:00 PM']
slot11 = [' 11:45:00 AM', ' 11:30:00 AM', ' 11:15:00 AM', ' 11:00:00 AM']
slot10 = [' 10:45:00 AM', ' 10:30:00 AM', ' 10:15:00 AM', ' 10:00:00 AM']
slot9 = [' 09:45:00 AM', ' 09:30:00 AM', ' 09:15:00 AM', ' 09:00:00 AM']
slot8 = [' 08:45:00 AM', ' 08:30:00 AM', ' 08:15:00 AM', ' 08:00:00 AM']
slot7 = [' 07:45:00 AM', ' 07:30:00 AM', ' 07:15:00 AM', ' 07:00:00 AM']
# seperate data by slot
slots = [slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slot10, slot11,slot12,
         slot13,slot14,slot15,slot16,slot17,slot18,slot19,slot20,slot21,slot22,slot23,slot0]
junwd_dict = {}
jun06 = junwd[junwd.sdate == '2023-06-06']
for i, slot in enumerate(slots, start=0):
    junwd_dict[f'junwd{i}'] = jun06[jun06.stime.isin(slot)]

for i in range(len(time_dfs)):
    mapping_dict = time_dfs[f'time{i}'].set_index('od')['tran_time'].to_dict()
    junwd_dict[f'junwd{i}']['trantt'] = junwd_dict[f'junwd{i}']['od'].map(mapping_dict)
jun06_out = pd.concat([junwd_dict[f'junwd{i}'] for i in range(len(time_dfs))], ignore_index=True)
os.chdir('C:\\Users\\Zhihua\\Documents\\MyResearch\\ChicagoData\\trips')
jun06_out.to_csv('2023Triptt_Jun06.csv', sep=',', index=True, encoding='utf-8')
