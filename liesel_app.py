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

st.set_page_config(page_title=page_title,layout=layout)
st.header("Data Analytics on Real World Data: Gas Receipts")

container = st.container()
with container:
    tab1, tab2, tab3 = st.tabs(["Background", "Enter Liesel", "Full Circle"])

    with tab1:
        st.subheader("Background")
        st.markdown("""
                    When I was younger, I had a co-worker that kept a log of every time he put gas in his truck. He logged the mileage, the gas consumption, dates, everything. At the time, it seemed weird. Why go to the trouble? What could you possibly do with all of that information? _How could that possibly be worth the effort?_

                    Later that year, I got a graphing calculator for my high school Calculus class. We had to enter coefficients and formulas and out popped these wonky, monochrome graphs. _And it blew my mind._ Functions translated inputs into outputs. I wasn't the best Math student up to that point, but once I began to see how functions explained everything, I was hooked.

                    I went to college and earned a Bachelor of Science and Master of Science, both in Mathematics. For the past 25 years, I have been doing data science in one form or another. It wasn't even called _\"data science\"_ back when I started.
                    """)
    with tab2:
        st.subheader("Enter Liesel")
        st.markdown("""
                    I bought my car, a Grey 2019 Volkswagen Golf, in June 2019. My prior car was also a Volkswagen, a 2001 Blue Lagoon Jetta 1.8T that I named _Lorelei_ after a Siren in German mythology. I'm a sentimental person, and I name inanimate objects with which I spent a lot of time, so obviously I was naming the Golf, too. Just like with boats, I feel cars have feminine spirits. I also name things based on their origin. _Lorelei_ was a German car and needed a German name. I had a Ducati Monster 695 Dark named _Minerva_ after the Roman goddess. So the Golf needed a feminine German name.
                    
                    Originally, we planned to lease the Golf, so I jokingly referred to it as _Liesel_. We ended up buying it, but at that point I was enamored with the name, so it stuck.

                    _Liesel_ was purchased to be a second car for our household. I didn't need to use it that often to commute to my job, maybe once or twice a week. We have offices out in the suburbs and downtown Chicago, both not far from the train that runs near my house. Then the pandemic struck. I had been using it infrequently before; at that point, I wasn't using it at all. It took a long time for things to get back to anything resembling normalcy.
                    """)            
    with tab3:
        st.subheader("Full Circle")
        st.markdown("""
                    When I drove Liesel home, I remembered my co-worker and his logging of gas receipts. My view of the whole process had completely turned around. Gas receipts are reflections of a life in motion. Where have you been, and where are you now? Are you moving more or less than last week, last month, or last year? Do you move less when it costs more to do so?

                    Data analytics may not be able to answer those questions. But it can provide some insights into life that you may not realize are right in front of you. You just have to look, so look we shall.
                    """)