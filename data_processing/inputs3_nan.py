# -*- coding: utf-8 -*-
"""
Created on Fri May 16 16:29:15 2025

@author: zji244
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 15 16:24:12 2025

@author: zji244
"""

import os
import time
import timeit
import csv
import numpy as np
import math
import pandas as pd
import array as arr
import sys
import glob
from shapely.geometry import Point, Polygon
from shapely.ops import nearest_points
import geopandas as gpd
from geopandas import GeoDataFrame
import folium
from folium.plugins import MarkerCluster
import seaborn as sns
import contextily as ctx
import branca.colormap as cm
from branca.colormap import linear
import geopy.distance
#maths & figures
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.image as mpimg
from colour import Color
from mpl_toolkits.axes_grid1 import make_axes_locatable
import plotly.express as px
import plotly.graph_objects as go
import statistics
import itertools
from math import radians, sin, cos, sqrt, atan2
import heapq
import cartopy.crs as ccrs
import mpu
#%%
os.chdir('C:\\Users\\zji244\\Documents\\ZJ_TRB_FP\\input')
june = pd.read_csv("2023Triptt_Jun06_3nan.csv")
june = june.dropna()
june['speed'] = june.mile/june.second*3600
june = june[june.speed>=5]
june = june[june.mile<=20]
june = june[june.second<=5400]
june = june[june.fare_a<=20]

os.chdir('C:\\Users\\zji244\\Documents\\ZJ_TNC_CASPT\\input')
ttam = pd.read_csv('cmapt3_tt_.csv')
tracts = pd.read_csv('Income.csv', names = ["areaNo","areaName","crowded","belowPoverty","unemploy","noHighDip","laborAge","incomeCapita","hardshipIndex"], header = 0)
income = pd.to_numeric(tracts['incomeCapita'])/2000
boundary = pd.read_csv('CensusTractsTIGER2010.csv')

dictionary = tracts.set_index('areaNo')['incomeCapita'].to_dict()
boundary['income'] = boundary.COMMAREA_N.map(dictionary)/2000
geoidlist =boundary.GEOID10.astype(str).str[:11]
geoidincome = pd.DataFrame()
geoidincome['geoid'] = boundary.GEOID10.astype(str).str[:11]
geoidincome['income'] = boundary['income']
# cbd, airport, tour
censustract = pd.read_csv("DowntownCensusTracts_tourdel.csv") 
censustract['zone'] = 1
tour_df= pd.DataFrame({'geoid10': [17031081402, 17031330100, 17031841000]})
tour_df['zone'] = 2
airport = pd.DataFrame({'geoid10':[17031980000,17031770602,17031980100,17031640100,17031835200,17031560700]}) # 2 oHare, 4 midway
# transit vot
os.chdir('C:\\Users\\zji244\\Documents\\ZJ_TNC_CASPT\\output')
transitVOT = pd.read_csv("transitVOT_tall.csv") 
june['o_zone'] = june['o'].apply(lambda x: (1 if x in censustract['geoid10'].values else 0) + (2 if x in tour_df['geoid10'].values else 0))
june['d_zone'] = june['d'].apply(lambda x: (1 if x in censustract['geoid10'].values else 0) + (2 if x in tour_df['geoid10'].values else 0))
june['od_zone'] = june.o_zone*3+june.d_zone

june['tripcount'] = june.groupby('od')['od'].transform('count')
june['od_zone'] = june.o_zone*4+june.d_zone
june = june[~june['o'].isin(airport['geoid10'])]
june = june[~june['d'].isin(airport['geoid10'])]
#%% vot 
df_odlist = june.od.unique()
df_odlist = pd.DataFrame(df_odlist, columns = ['od']).reset_index()
dictionary = transitVOT.set_index('od')['high'].to_dict()
df_odlist['transitVOTh'] = df_odlist.od.map(dictionary)
dictionary = transitVOT.set_index('od')['low'].to_dict()
df_odlist['transitVOTl'] = df_odlist.od.map(dictionary)
df_odlist['transitVOTa'] = df_odlist.transitVOTh+df_odlist.transitVOTl
df_odlist = df_odlist[df_odlist['transitVOTa'] != 0]
df_odlist['high'] = df_odlist.transitVOTh/df_odlist.transitVOTa
df_odlist['low'] = df_odlist.transitVOTl/df_odlist.transitVOTa
df_odlist = df_odlist.dropna()
#%% process and save
june = june.dropna()
june = june[june['trantt'] != 0]
june['walktt'] = june.mile/3 # 3mph of walking speed
june['basefare'] = june.fare_f+june.fare_t
os.chdir('C:\\Users\\zji244\\Documents\\ZJ_TRB_FP\\input')
june.to_csv("june_tillVOT.csv", sep=',', index=True, encoding='utf-8') #output 
june06 = june[june.sdate.isin(["2023-06-06"])]
june06.to_csv("june06.csv", sep=',', index=True, encoding='utf-8') #output
#%% random vot setting following od
import time
st = time.time()
for i in df_odlist.index:
    mask = june06['od'] == df_odlist.od[i]
    high = df_odlist.high[i]
    vots = np.random.choice([30, 10], size = mask.sum(), p=[high, 1 - high]) #mask.sum() : num of rows
    # Assign these random vots to column 'k' for the filtered rows
    june06.loc[mask, 'vot'] = vots
et = time.time()
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
june06.vot = june06.vot.fillna(30)
dummy = june06[june06.vot.isna()]
dummy1 = dummy.od.unique()
dummy2 = dummy.groupby('od')['share_p'].sum()
# Execution time: 390.4934141635895 seconds
#%% gc calculation
os.chdir('C:\\Users\\zji244\\Documents\\ZJ_TRB_FP\\input')
june06.to_csv("june06vot_v2.csv", sep=',', index=True, encoding='utf-8') #output
df = pd.read_csv("june06vot_v2.csv")
def calculate_disgc(df):
    df['trangc'] = df['trantt']/60 +2/df['vot']*60
    df['autogc'] = df['second']/60 +df.basefare/df['vot']*60
    df['tncgc'] = df['second']/60 +df.fare/df['vot']*60
    df['walkgc'] = df['walktt']*60
    df['ecogc'] = df[['walkgc', 'trangc']].min(axis=1)
for df in [df]:
    calculate_disgc(df)
