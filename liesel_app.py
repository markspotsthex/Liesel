import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_folium import st_folium, folium_static
import plotly.graph_objects as go

import urllib.request
import json
from datetime import datetime, date, timedelta

import pandas as pd
import numpy as np
import folium
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

code_FRED="""
fred= Fred(api_key=st.secrets["FRED_API_KEY"])
data={}
data['gas']=fred.get_series('GASREGW',observation_start=liesel_buy)
data=pd.DataFrame(data)
"""
# -----------------------

# ---- internal data ----
fpath = "https://raw.githubusercontent.com/markspotsthex/Liesel/main/Liesel_Fuel_History.json"
with urllib.request.urlopen(fpath) as url:
    fh = json.load(url)

#df_stations = pd.DataFrame(fh['stations'])

loc_name=[station['stationName'] for station in fh['stations'] if station['attributes']['location']['address']!="Unknown"]
loc_latitude=[station['attributes']['location']['latitude'] for station in fh['stations'] if station['attributes']['location']['address']!="Unknown"]
loc_longitude=[station['attributes']['location']['longitude'] for station in fh['stations'] if station['attributes']['location']['address']!="Unknown"]
loc_data={"Name": loc_name, "Latitude": loc_latitude, "Longitude": loc_longitude}
loc_df = pd.DataFrame(data=loc_data)
code_LL = """
          fpath = "https://raw.githubusercontent.com/markspotsthex/Liesel/main/Liesel_Fuel_History.json"
          with urllib.request.urlopen(fpath) as url:
              fh = json.load(url)
          loc_name=[station['stationName'] for station in fh['stations'] if station['attributes']['location']['address']!="Unknown"]
          loc_latitude=[station['attributes']['location']['latitude'] for station in fh['stations'] if station['attributes']['location']['address']!="Unknown"]
          loc_longitude=[station['attributes']['location']['longitude'] for station in fh['stations'] if station['attributes']['location']['address']!="Unknown"]
          loc_data={"Name": loc_name, "Latitude": loc_latitude, "Longitude": loc_longitude}
          loc_df = pd.DataFrame(data=loc_data)
          """
map_osm = folium.Map(location=st.secrets["s_LOCATION"],zoom_start=8)
loc_df.apply(lambda row:folium.CircleMarker(location=[row["Latitude"], row["Longitude"]]).add_to(map_osm),axis=1)
code_Map="""
         map_osm = folium.Map(location=[LAT, LONG],zoom_start=8)
         loc_df.apply(lambda row:folium.CircleMarker(location=[row["Latitude"], row["Longitude"]]).add_to(map_osm),axis=1)
         """

df_stops = pd.DataFrame(fh['stops']).sort_values(by=['datetime'])
df_stops['date']=pd.to_datetime(df_stops['datetime'])
df_stops['dtindex']=(df_stops['date']-liesel_buy).dt.days
df_stops['mpg']=df_stops['trip']/df_stops['gal']
df_stops['fcost']=df_stops['credit'].cumsum()
df_stops['ttrip']=df_stops['trip'].cumsum()

code_PD="""
df_stops = pd.DataFrame(fh['stops']).sort_values(by=['datetime'])
df_stops['date']=pd.to_datetime(df_stops['datetime'])
df_stops['dtindex']=(df_stops['date']-liesel_buy).dt.days
df_stops['mpg']=df_stops['trip']/df_stops['gal']
df_stops['fcost']=df_stops['credit'].cumsum()
df_stops['ttrip']=df_stops['trip'].cumsum()
"""
# -----------------------

st.set_page_config(page_title=page_title,layout=layout)
st.header("Data Analytics on Real World Data: Gas Receipts")

story = st.container()
with story:
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
        
# ---- Data Analytics Processing section ----


# ---- Data Analytics Visualization section ----
dataviz = st.container()
with dataviz:
    # TODO: add visualizations
    tab21, tab22, tab23 = st.tabs(["Total Mileage","Location Analysis","Gas Prices"])
    with tab21:
        st.subheader("Total Mileage Traveled and Cost Incurred")
        st.write("""
                 The first thing I wanted to look at cumulative mileage and costs. Mileage is already a cumulative data element, and it's pretty easy to create the cumulative sums of costs.
                 """)
        st.code(code_PD,language="python")
        fig, ax1 = plt.subplots()
        ax1.scatter(df_stops['date'], df_stops['miles'])
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
        for label in ax1.get_xticklabels(which='major'):
            label.set(rotation=30,horizontalalignment='right')

        ax2 = ax1.twinx()
        ax2.scatter(df_stops['date'], df_stops['fcost'],color='tab:red')
        st.pyplot(fig)
        st.write("""
                 The blue series represents the cumulative mileage traveled at each refill. The red series represents the cumulative cost paid for gas.
                 """)
        st.code(code_PD,language="python")

    with tab22:
        st.subheader("Refueling Location Analysis")
        st.write("""
                 One of the data elements I captured was the location where I filled my tank. I didn't intend to be selective, but I have only pumped gas at about a dozen gas stations. The code below will show how I created a Pandas DataFrame for analysis.
                 """)
        st.code(code_LL)
        st.write("""
                 As you can see in the map below, I haven't driven my car on any long distance trips. It's a comfortable ride, but the trunk is small, and my family doesn't pack light. The furthest my car has driven is to Normal, IL (not shown on map).
                 """)
        folium_static(map_osm, width=700)
        st.write("""
                 Folium is a pretty powerful mapping tool for Python, but it doesn't require a lot of code to create a map.
                 """)
        st.code(code_Map)
    with tab23:
        st.subheader("Gas Price Benchmarking")
        st.write("""
                 Since I did most of my driving within 150 miles of Chicago, I wanted to know if the prices I paid for gas tracked well with gas prices nationwide. So I pulled the series of gas prices from the Federal Reserve Economics Database (FRED).
                 """)
        st.code(code_FRED,language="python")
        st.write("""
                 Now that I have gas prices for my transactions and for the nation, I can plot to compare them.
                 """)
        fig, ax1 = plt.subplots()
        ax1.scatter(df_stops['date'], df_stops['price'])
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
        for label in ax1.get_xticklabels(which='major'):
            label.set(rotation=30,horizontalalignment='right')

        ax2 = ax1.twinx()
        ax2.scatter(data.index, data['gas'],color='tab:red')

        ax1.set_ylim([0, None])
        ax2.set_ylim([0, None])
        st.pyplot(fig)
        st.write("""
                 Plotting what I paid in blue against what prices were nationally in red, looks pretty consistent.
                 """)

    # with tab23:
    #     st.subheader("Total Mileage Traveled")

    #     xx=np.array(df_stops['dtindex'])
    #     yy=np.array(df_stops['miles'])
    #     pw_fit=pwr.Fit(xx,yy,n_breakpoints=2)
    #     pw_fit.summary()

    #     pw_fit.plot_data(color="grey", s=20)
    #     pw_fit.plot_fit(color="red", linewidth=4) 
    #     pw_fit.plot_breakpoints()
    #     pw_fit.plot_breakpoint_confidence_intervals()
    #     plt.xlabel("xx")
    #     plt.ylabel("yy")
    #     st.pyplot(pw_fit)

    #     # Get the key results of the fit 
    #     pw_results = pw_fit.get_results()
    #     pw_estimates = pw_results["estimates"]
    #     bp1 = liesel_buy+timedelta(days=pw_estimates['breakpoint1']['estimate'])
    #     bp2 = liesel_buy+timedelta(days=pw_estimates['breakpoint2']['estimate'])
    #     st.write("Driving habits changed on {} and again on {}".format(bp1.strftime('%m/%d/%Y'),bp2.strftime('%m/%d/%Y')))
