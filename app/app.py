import os

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import re

import plotly.express as px 
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.subplots import make_subplots

st.title("COVID-19 Nursing Home Dashboard")

@st.cache
def get_plots():
    plotly_lst = {}
    for f in os.listdir('./datasets'):
        temp = open('./datasets/' + f, 'r', encoding='utf-8')
        temp_code = temp.read()
        plotly_lst[f] = temp_code
    return plotly_lst

plotly_lst = get_plots()



# SIDEBARS
select = st.sidebar.selectbox('Navigation',
[
    'Home',
    'Distribution Plots',
    'Choropleths',
    'Bubble Maps',
    'Line Graphs (National)',
    'Line Graphs (State)'
], key='1')

if select == 'Home':
    st.markdown("""
    This dashboard will visualize [COVID-19 Nursing Home Dataset](https://data.cms.gov/Special-Programs-Initiatives-COVID-19-Nursing-Home/COVID-19-Nursing-Home-Dataset/s2uc-8wxp) from the Centers for Medicare & Medicaid Services.
    
    COVID-19 has disproportionately affected residents of long-term care facilities, [with these facilities](https://www.aarp.org/caregiving/health/info-2020/covid-19-nursing-homes-an-american-tragedy.html) constituting less than 1 percent of the U.S. population yet 43 percent of all COVID-19 deaths.

    This app was created to help assess the COVID-19 response performance in nursing homes on a national and state level and potentially help determine whether government resources need to be redirected.   

    Learn more about [CDC's guidance for nursing home and long-term care facilities](https://www.cdc.gov/coronavirus/2019-ncov/hcp/long-term-care.html). 
    """)

if select == 'Distribution Plots':
    distribution_plots = {
        'Percent of Covid Deaths over Total COVID Cases':plotly_lst['histogram_1.html'],
        'Percent Beds Occupied':plotly_lst['histogram_2.html']
    }
    distribution = st.selectbox("Select Distribution Plot", list(distribution_plots.keys()), 0)
    st.components.v1.html(distribution_plots[distribution], height=600)

if select == 'Choropleths':
    choropleths = {
        'Residents Weekly Confirmed COVID-19':plotly_lst['choropleth_1.html'],
        'Residents Weekly COVID-19 Deaths':plotly_lst['choropleth_2.html'],
        'Shortage of Nursing Staff':plotly_lst['choropleth_3.html'],
        'Shortage of Aides':plotly_lst['choropleth_4.html']
    }
    choropleth = st.selectbox("Select Choropleth", list(choropleths.keys()), 0)
    st.components.v1.html(choropleths[choropleth], height=600)

if select == 'Bubble Maps':
    st.markdown("""
    ### **Note**

    - 'Residents Weekly Confirmed COVID-19' shows nursing homes reporting over 5 or more confirmed COVID-19 cases. 
    - 'Residents Weekly COVID-19' shows nursing homes reporting 3 or more COVID-19 deaths. 
    
    """)
    bubble_maps = {
        'Residents Weekly Confirmed COVID-19':plotly_lst['bubblemap_1.html'],
        'Residents Weekly COVID-19 Deaths':plotly_lst['bubblemap_2.html']
    }
    bubble_map = st.selectbox("Select Bubble Map", list(bubble_maps.keys()), 0)
    st.components.v1.html(bubble_maps[bubble_map], height=600)

if select == 'Line Graphs (National)':
    line_graphs = {
        'Residents Weekly COVID-19 Cases and Deaths': plotly_lst['line_graph_1.html'],
        'Percent Beds Occupied':plotly_lst['line_graph_2.html'],
        'Percent of COVID Deaths over Total COVID Cases':plotly_lst['line_graph_3.html']
    }
    line_graph = st.selectbox("Select Line Graph", list(line_graphs.keys()), 0)
    st.components.v1.html(line_graphs[line_graph], height=600)

if select == 'Line Graphs (State)':
    line_graphs_state = {
        'Residents Weekly COVID-19 Deaths': plotly_lst['line_graph_state_1.html'],
        'Residents Weekly Confirmed COVID-19': plotly_lst['line_graph_state_2.html'],
        'Percent Beds Occupied':plotly_lst['line_graph_state_3.html'],
        'Percent of COVID Deaths over Total COVID Cases':plotly_lst['line_graph_state_4.html']
    }
    line_graph_state = st.selectbox("Select Line Graph", list(line_graphs_state.keys()), 0)
    st.components.v1.html(line_graphs_state[line_graph_state], height=600)