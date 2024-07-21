import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go

import urllib.request
import json
from datetime import datetime, date, timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from fredapi import Fred

from sklearn.linear_model import LinearRegression 
import piecewise_regression as pwr

# ---- Settings ----
page_title = "Data Analytics with Real World Data: Gas Receipts"
page_icon = ":automobile:"
layout = "centered"
# ------------------

# ---- Variables ----
liesel_buy = datetime(2019,6,21)
pandemic_st = datetime(2020,3,11)
pandemic_end= datetime(2022,4,13)
rto = datetime(2023,4,17)
# -------------------

# ---- external data ----
fred= Fred(api_key=st.secrets["FRED_API_KEY"])
data={}
data['gas']=fred.get_series('GASREGW',observation_start=liesel_buy)
data=pd.DataFrame(data)
# -----------------------

# ---- internal data ----
fpath = "https://raw.githubusercontent.com/markspotsthex/Liesel/main/Liesel_Fuel_History.json"
with urllib.request.urlopen(fpath) as url:
    fh = json.load(url)

df_stations = pd.DataFrame(fh['stations'])

df_stops = pd.DataFrame(fh['stops']).sort_values(by=['datetime'])
df_stops['date']=pd.to_datetime(df_stops['datetime'])
df_stops['dtindex']=(df_stops['date']-liesel_buy).dt.days
df_stops['mpg']=df_stops['trip']/df_stops['gal']
df_stops['fcost']=df_stops['credit'].cumsum()
df_stops['ttrip']=df_stops['trip'].cumsum()
# -----------------------

st.set_page_config(page_title=page_title,page_icon=page_icon,layout=layout)
st.title = (page_title + " " + page_icon)

st.text('I\'m not sure this works.')