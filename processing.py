import json
from datetime import datetime, date, timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from fredapi import Fred

from sklearn.linear_model import LinearRegression 
import piecewise_regression as pwr

liesel_buy = datetime(2019,6,21)
pandemic_st = datetime(2020,3,11)
pandemic_end= datetime(2022,4,13)
rto = datetime(2023,4,17)

fred= Fred(api_key=st.secrets["FRED_API_KEY"])
data={}
data['gas']=fred.get_series('GASREGW',observation_start=liesel_buy)
data=pd.DataFrame(data)

fpath = '/Users/mark/Projects/Liesel_Fuel_History.json'
f=open(fpath)
fh = json.load(f)
f.close

df_stations = pd.DataFrame(fh['stations'])
df_stops = pd.DataFrame(fh['stops']).sort_values(by=['datetime'])
df_stops.dtypes

df_stops.head(5)

df_stops['date']=pd.to_datetime(df_stops['datetime'])
df_stops['dtindex']=(df_stops['date']-liesel_buy).dt.days
df_stops['mpg']=df_stops['trip']/df_stops['gal']
df_stops['fcost']=df_stops['credit'].cumsum()
df_stops['ttrip']=df_stops['trip'].cumsum()
df_stops.head()

xx=np.array(df_stops['dtindex'])
yy=np.array(df_stops['miles'])
pw_fit=pwr.Fit(xx,yy,n_breakpoints=2)
pw_fit.summary()

pw_fit.plot_data(color="grey", s=20)
pw_fit.plot_fit(color="red", linewidth=4) 
pw_fit.plot_breakpoints()
pw_fit.plot_breakpoint_confidence_intervals()
plt.xlabel("xx")
plt.ylabel("yy")
plt.show()
plt.close()

# Get the key results of the fit 
pw_results = pw_fit.get_results()
pw_estimates = pw_results["estimates"]
bp1 = liesel_buy+timedelta(days=pw_estimates['breakpoint1']['estimate'])
bp2 = liesel_buy+timedelta(days=pw_estimates['breakpoint2']['estimate'])
print("Driving habits changed on {} and again on {}".format(bp1.strftime('%m/%d/%Y'),bp2.strftime('%m/%d/%Y')))

fig, ax1 = plt.subplots()
ax1.scatter(df_stops['date'], df_stops['miles'])
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
for label in ax1.get_xticklabels(which='major'):
    label.set(rotation=30,horizontalalignment='right')

ax2 = ax1.twinx()
ax2.scatter(df_stops['date'], df_stops['fcost'],color='tab:red')
    
plt.show()

fig, ax1 = plt.subplots()
ax1.scatter(df_stops['date'], df_stops['price'])
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
for label in ax1.get_xticklabels(which='major'):
    label.set(rotation=30,horizontalalignment='right')

ax2 = ax1.twinx()
ax2.scatter(data.index, data['gas'],color='tab:red')

ax1.set_ylim([0, None])
ax2.set_ylim([0, None])

plt.show()