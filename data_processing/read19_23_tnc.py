# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 12:47:00 2024

@author: Zhihua
"""
#%% imports
#basics
import os
import time
import timeit
import csv
import numpy as np
import pandas as pd
import array as arr
import sys

#maps
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
from mpl_toolkits.axes_grid1 import make_axes_locatable
import plotly.express as px

import plotly.graph_objects as go
import statistics
import itertools
from math import radians, sin, cos, sqrt, atan2

import heapq
import cartopy.crs as ccrs
import mpu
#%% read 2019 tnc data
os.chdir('C:\\Users\\Zhihua\\Documents\\MyResearch\\ChicagoData\\trips')
df02 = pd.read_csv("2019_data/19_02.csv",
                   names = ["id", "startts", "endts", "second","mile",
                             "p_cen","d_cen","p_com","d_com","fare_f","fare_t","fare_a","fare",
                             "share_a","share_p","p_cla","p_clo","p_cl","d_cla","d_clo","d_cl"])
df02 = df02.drop(index=0).reset_index(drop=True)
df06 = pd.read_csv("2019_data/19_06.csv",
                   names = ["id", "startts", "endts", "second","mile",
                             "p_cen","d_cen","p_com","d_com","fare_f","fare_t","fare_a","fare",
                             "share_a","share_p","p_cla","p_clo","p_cl","d_cla","d_clo","d_cl"])
df06 = df06.drop(index=0).reset_index(drop=True)
df09 = pd.read_csv("2019_data/19_09.csv",
                   names = ["id", "startts", "endts", "second","mile",
                             "p_cen","d_cen","p_com","d_com","fare_f","fare_t","fare_a","fare",
                             "share_a","share_p","p_cla","p_clo","p_cl","d_cla","d_clo","d_cl"])
df09 = df09.drop(index=0).reset_index(drop=True)
df12 = pd.read_csv("2019_data/19_12.csv",
                   names = ["id", "startts", "endts", "second","mile",
                             "p_cen","d_cen","p_com","d_com","fare_f","fare_t","fare_a","fare",
                             "share_a","share_p","p_cla","p_clo","p_cl","d_cla","d_clo","d_cl"])
df12 = df12.drop(index=0).reset_index(drop=True)
#combine the data sets into one
df = pd.concat([df02, df06, df09, df12], ignore_index=True)
#%% cleanse data
df3 = df.drop(['p_cla', 'p_clo','p_cl','d_cla','d_clo','d_cl','share_a'], axis=1)
df2 = df
df = df3
df['sdate'] = df.startts.str[:10]
df['edate'] = df.endts.str[:10]
df['stime'] = df.startts.str[10:]
df['etime'] = df.endts.str[10:]
df['tnc_min'] = pd.to_numeric(df['second']) *1/60
df4 = df
#%% drop empty, create od
df = df[df['p_cen'].notna()]
df = df[df['d_cen'].notna()]
df5= df
df['o'] = df['p_cen'].astype("string").str[:11]
df['d'] = df['d_cen'].astype("string").str[:11]
df['od']=df.o+df.d
df.to_csv("tncFJSD_19.csv", sep=',', index=True, encoding='utf-8') #output
df19 = df
#%% 23
file_paths = ["2023_data/23_02.csv", "2023_data/23_06.csv", "2023_data/23_09.csv", "2023_data/23_12.csv"]
df = pd.concat([pd.read_csv(file, header=None, names =  ["id", "startts", "endts", "second","mile","pertime","perdis",
         "p_cen","d_cen","p_com","d_com","fare_f","fare_t","fare_a","fare",
         "share_a","share_m","share_p","p_cla","p_clo","p_cl","d_cla","d_clo","d_cl"], skiprows=1) for file in file_paths], ignore_index=True)
df3 = df.drop(['p_cla', 'p_clo','p_cl','d_cla','d_clo','d_cl','share_a', 'p_com','d_com'], axis=1)
df2 = df
df = df3
df['sdate'] = df.startts.str[:10]
df['edate'] = df.endts.str[:10]
df['stime'] = df.startts.str[10:]
df['etime'] = df.endts.str[10:]
df['tnc_min'] = pd.to_numeric(df['second']) *1/60
df4 = df
# drop empty, create od 23
df = df[df['p_cen'].notna()]
df = df[df['d_cen'].notna()]
df5= df
df['o'] = df['p_cen'].astype("string").str[:11]
df['d'] = df['d_cen'].astype("string").str[:11]
df['od']=df.o+df.d
df.to_csv("tncFJSD_23.csv", sep=',', index=True, encoding='utf-8') #output
df23 = df
#%% 19 wkdy
wd19 = pd.read_csv("wdlist2019_FJSD.csv")
wd19 = pd.to_datetime(wd19.Date)
df19['sdate'] = df19['startts'].str[:10]
df19['sdate'] = pd.to_datetime(df19['sdate'], format='%m/%d/%Y')
df19wkdy= df19[df19['sdate'].isin(wd19)]
df19 = df19wkdy
df19.to_csv("tncFJSD_19_wkdy.csv", sep=',', index=True, encoding='utf-8') #output
df19['st_hr'] = df19['startts'].str[:13].str[-2:] + df19['startts'].str[-2:]
df19_t3 = df19wkdy[df19wkdy['st_hr'].isin(['07AM','08AM'])]
df19_t7 = df19wkdy[df19wkdy['st_hr'].isin(['04PM','05PM'])]
df19_t3.to_csv("trips/tncFJSD_19_wkdy_ampk.csv", sep=',', index=True, encoding='utf-8') #output
df19_t7.to_csv("trips/tncFJSD_19_wkdy_pmpk.csv", sep=',', index=True, encoding='utf-8') #output
#%% 23 wkdy
wd23 = pd.read_csv("wdlist2023_FJSD.csv")
wd23 = pd.to_datetime(wd23.Date)
df23['sdate'] = df23['startts'].str[:10]
df23['sdate'] = pd.to_datetime(df23['sdate'], format='%m/%d/%Y')
df23wkdy= df23[df23['sdate'].isin(wd23)]
df23 = df23wkdy
df23.to_csv("tncFJSD_23_wkdy.csv", sep=',', index=True, encoding='utf-8') #
df23['st_hr'] = df23['startts'].str[:13].str[-2:] + df23['startts'].str[-2:]
df23_t3 = df23wkdy[df23wkdy['st_hr'].isin(['07AM','08AM'])]
df23_t7 = df23wkdy[df23wkdy['st_hr'].isin(['04PM','05PM'])]
df23_t3.to_csv("trips/tncFJSD_23_wkdy_ampk.csv", sep=',', index=True, encoding='utf-8') #output
df23_t7.to_csv("trips/tncFJSD_23_wkdy_pmpk.csv", sep=',', index=True, encoding='utf-8') #output
#%%
