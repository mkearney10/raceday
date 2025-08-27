import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from datetime import time, timedelta, datetime
import matplotlib.dates as mdates

st. set_page_config(layout="wide")

# Load Data -> .csvs from load_databases.py
df_raw = pd.read_csv('df_database_2025.csv')
    
## Sort based on category for plotting
df_raw = df_raw.sort_values(by = 'CatID')

dflt_strt = { 
    101: time(9,0),
    102: time(9,5),
    103: time(9,10),
    104: time(9,15),
    201: time(10,30),
    202: time(10,35),
    203: time(10,40),
    301: time(12,0),
    302: time(12,5),
    401: time(13,0),
    402: time(13,5),
    403: time(13,10),
    501: time(14,0),
    502: time(14,5),
    503: time(14,10),
    504: time(14,15),
    601: time(14,0),
    602: time(14,5),
    603: time(14,10),
    701: time(14,50),
    702: time(14,55),
    703: time(15,0),
    801: time(15,40),
    802: time(15,45),
    803: time(15,50),
    804: time(15,55),
    805: time(16,0)
    }

cat_names = {
    101: 'Varsity Male',
    102: 'Varsity Female',
    103: 'Advanced Middle School Male',
    104: 'Advanced Middle School Female',
    201: 'Junior Varsity 9-10th Grade Male',
    202: 'Junior Varsity 11-12th Grade Male',
    203: 'Junior Varsity Female',
    301: 'Novice 10-12th Grade Male',
    302: 'Novice 9th Grade Male',
    401: 'Novice 9-12th Grade Female',
    402: 'Intermediate 6-8th Grade Female',
    403: 'Novice 6-8th Grade Female',
    501: 'Intermediate 7-8th Grade Male',
    502: 'Intermediate 6th Grade Male',
    503: 'Novice 7-8th Grade Male',
    504: 'Novice 6th Grade Male',
    601: 'Advanced Elementary Male',
    602: 'Elementary 5th Grade Male',
    603: 'Elementary 4th Grade Male',
    701: 'Advanced Elementary Female',
    702: 'Elementary 5th Grade Female',
    703: 'Elementary 4th Grade Female',
    801: 'Elementary 3rd Grade Male',
    802: 'Elementary 2nd Grade Male',
    803: 'Elementary 2nd-3rd Grade Female',
    804: 'Elementary PreK-1st Grade Male',
    805: 'Elementary PreK-1st Grade Female'

    }

min_sat = time(14,0)
min_sun = time(9,0)

max_sat = time(18,0)
max_sun = time(17,0)

sat_cats = [601, 602, 603, 701, 702, 703, 801, 802, 803, 804, 805]
sun_cats = [101, 102, 103, 104, 201, 202, 203, 301, 302, 401, 402, 403, 501, 502, 503, 504]

dflt_step = timedelta(minutes=5)

strt = pd.DataFrame(columns = ['CatID', 'StrtTm'])

tab1, tab2 = st.sidebar.tabs(["Saturday", "Sunday"])

p = 0
with tab1:
    for cats in sat_cats:
        strt.loc[p, 'CatID'] = cats
        strt.loc[p, 'StrtTm'] = st.slider(
            cat_names[cats] + " (" + str(dflt_strt[cats]) + ")",
            min_value = min_sat,
            max_value = max_sat,
            value = dflt_strt[cats],
            step = dflt_step
            )
        p += 1

with tab2:
    for cats in sun_cats:
        strt.loc[p, 'CatID'] = cats
        strt.loc[p, 'StrtTm'] = st.slider(
            cat_names[cats] + " (" + str(dflt_strt[cats]) + ")",
            min_value = min_sun,
            max_value = max_sun,
            value = dflt_strt[cats],
            step = dflt_step
            )
        p += 1

df = df_raw[['RegID','CatID','Cat','Venue']]
r = 0
while r < df_raw.shape[0]:
    catid = df_raw.loc[r,'CatID']
    if catid in [501, 502]:
        catid = 521
        df_raw.loc[r,'CatID'] = catid
    elif catid in [503]:
        catid = 523
        df_raw.loc[r,'CatID'] = catid
    elif catid in [402]:
        catid = 422
        df_raw.loc[r,'CatID'] = catid
    strt_row = strt.loc[strt['CatID']] == catid.index[0]
    n = 1
    while n <= 3:
        if not np.isnan(df_raw.loc[r, 'Lap' + str(n)]):
            if n in [1]:
                df_raw.loc[r, 'dLap' + str(n)] = timedelta(seconds=df_raw.loc[r, 'Lap' + str(n)]) + datetime.combine(datetime.now().date(), strt.loc[strt_row, 'StrtTm'])        
            elif n in [2, 3]:
                df_raw.loc[r, 'dLap' + str(n)] = timedelta(seconds=df_raw.loc[r, 'Lap' + str(n)]) + df_raw.loc[r, 'dLap' + str(n-1)]
        n += 1
    r += 1

df_sat = df_raw[df_raw['CatID'].isin(sat_cats)]
df_sun = df_raw[df_raw['CatID'].isin(sun_cats)]

fig = plt.figure()
sns.stripplot(data = df_sat, x = df_sat['dLap1'], y = df_sat['Cat'], size = 3, edgecolor = 'k', linewidth = 0.2)
sns.stripplot(data = df_sat, x = df_sat['dLap2'], y = df_sat['Cat'], size = 3, edgecolor = 'k', linewidth = 0.2)
sns.stripplot(data = df_sat, x = df_sat['dLap3'], y = df_sat['Cat'], size = 3, edgecolor = 'k', linewidth = 0.2)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xlim(datetime.combine(datetime.now().date(), min_sat), datetime.combine(datetime.now().date(), max_sat))
plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
plt.xlabel('Time')
plt.xticks(rotation=85)
plt.grid()
st.pyplot(fig, use_container_width=True)
plt.show()

fig = plt.figure()
sns.stripplot(data = df_sun, x = df_sun['dLap1'], y = df_sun['Cat'], size = 3, edgecolor = 'k', linewidth = 0.2)
sns.stripplot(data = df_sun, x = df_sun['dLap2'], y = df_sun['Cat'], size = 3, edgecolor = 'k', linewidth = 0.2)
sns.stripplot(data = df_sun, x = df_sun['dLap3'], y = df_sun['Cat'], size = 3, edgecolor = 'k', linewidth = 0.2)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xlim(datetime.combine(datetime.now().date(), min_sun), datetime.combine(datetime.now().date(), max_sun))
plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
plt.xlabel('Time')
plt.xticks(rotation=85)
plt.grid()
st.pyplot(fig, use_container_width=True)

plt.show()




