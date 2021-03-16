import os
import re

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import plotly.express as px 
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.subplots import make_subplots

# CONCATENATING FILES
df_lst = []
for f in os.listdir('../data'):
    temp = pd.read_csv('../data/' + f)
    df_lst.append(temp)
df = pd.concat(df_lst, ignore_index=True)

# FUNCTIONS
def clean_data(df):

    # Converting 'Week Ending' to datetime values
    df['Week Ending'] = pd.to_datetime(df['Week Ending'])

    # Dropping rows that did not meet quality assurance check
    df = df.loc[df['Passed Quality Assurance Check'] == 'Y']

    # Dropping rows where 'Geolocation' value is not provided
    df = df.dropna(subset=['Geolocation'])

    # Resetting index
    df = df.reset_index(drop=True)

    # List of all the binary columns
    binary_columns = [
        'Resident Access to Testing in Facility',
        'Laboratory Type Is State Health Dept',
        'Laboratory Type Is Private Lab',
        'Laboratory Type Is Other',
        'Able to Test or Obtain Resources to Test All Current Residents Within Next 7 Days',
        'Reason for Not Testing Residents - Lack of PPE for Personnel ', 
        'Reason for Not Testing Residents - Lack of Supplies',
        'Reason for Not Testing Residents  - Lack of Access to Laboratory',
        'Reason for Not Testing Residents - Lack of Access to Trained Personnel ', 
        'Reason for Not Testing Residents  - Uncertainty About Reimbursement',
        'Reason for Not Testing Residents  - Other',
        'During Past Two Weeks Average Time to Receive Resident Test Results',
        'Has Facility Performed Resident Tests Since Last Report',
        'Tested Residents with New Signs or Symptoms',
        'Tested Asymptomatic Residents in a Unit or Section After a New Case',
        'Tested Asymptomatic Residents Facility-Wide After a New Case',
        'Tested Asymptomatic Residents Without Known Exposure as Surveillance',
        'Tested Another Subgroup of Residents',
        'Able to Test or Obtain Resources to Test All Staff and/or Personnel Within Next 7 Days',
        'Reason for Not Testing Staff and/or Personnel - Lack of PPE for Personnel ',
        'Reason for Not Testing Staff and/or Personnel - Lack of Supplies',
        'Reason for Not Testing Staff and/or Personnel - Lack of Access to Laboratory',
        'Reason for Not Testing Staff and/or Personnel  - Lack of Access to Trained Personnel ', 
        'Reason for Not Testing Staff and/or Personnel - Uncertainty About Reimbursement',
        'Reason for Not Testing Staff and/or Personnel - Other',
        'During Past Two Weeks Average Time to Receive Staff and/or Personnel Test Results',
        'Has Facility Performed Staff and/or Personnel Tests Since Last Report',
        'Tested Staff and/or Personnel with New Signs or Symptoms',
        'Tested Asymptomatic Staff and/or Personnel in a Unit or Section After a New Case',
        'Tested Asymptomatic Staff and/or Personnel Facility-Wide After a New Case',
        'Tested Asymptomatic Staff and/or Personnel Without Known Exposure as Surveillance',
        'Tested Another Subgroup of Staff and/or Personnel',
        'In-House Point-of-Care Test Machine',
        'Shortage of Clinical Staff',
        'Shortage of Aides',
        'Shortage of Other Staff',
        'Any Current Supply of N95 Masks',
        'One-Week Supply of N95 Masks',
        'Any Current Supply of Surgical Masks',
        'One-Week Supply of Surgical Masks',
        'Any Current Supply of Eye Protection',
        'One-Week Supply of Eye Protection',
        'Any Current Supply of Gowns',
        'One-Week Supply of Gowns',
        'Any Current Supply of Gloves',
        'One-Week Supply of Gloves',
        'Any Current Supply of Hand Sanitizer',
        'One-Week Supply of Hand Sanitizer',
        'Ventilator Dependent Unit',
        'Any Current Supply of Ventilator Supplies',
        'One-Week Supply of Ventilator Supplies',
        'Three or More Confirmed COVID-19 Cases This Week',
        'Initial Confirmed COVID-19 Case This Week',
        'Has Facility Performed Tests Since Last Report',
        'In-House Point-of-Care Test Machine',
        'Enough Supplies to Test All Staff and/or Personnel Using Point-of-Care Test Machine',
        'Shortage of Nursing Staff'
    ]

    for col in binary_columns:
        df[col] = df[col].map({'N':0, 'Y':1})

    df['Percent Beds Occupied'] = df['Total Number of Occupied Beds']/df['Number of All Beds']
    df['Percent Beds Occupied'] = df['Percent Beds Occupied'].replace(np.inf, 1)

    df['Percent of COVID Deaths over Total COVID Cases']= df['Residents Total COVID-19 Deaths']/(df['Residents Total COVID-19 Deaths']+df['Residents Total Confirmed COVID-19'])

    return df

def get_df_by_state(df):

    # Grouping by state, week ending
    df_by_state = df.groupby(by=['Provider State', 'Week Ending']).sum()

    # Resetting index
    df_by_state = df_by_state.reset_index()

    # Setting 'Week Ending' back to str (for plotly graphs)
    df_by_state['Week Ending'] = df_by_state['Week Ending'].astype(str)

    return df_by_state

def get_df_by_provider(df):
    # Grouping by geolocation, week ending, and provider number
    df_by_provider = df.groupby(by=['Geolocation', 'Week Ending', 'Federal Provider Number']).sum()
    df_by_provider = df_by_provider.reset_index()

    # Setting 'Week Ending' back to str (for plotly graphs)
    df_by_provider['Week Ending'] = df_by_provider['Week Ending'].astype(str)

    # Sorting values by 'Week Ending' (for plotly graphs)
    df_by_provider = df_by_provider.sort_values(by='Week Ending', ascending=True)
    
    return df_by_provider

def get_df_timeseries(df):
    
    # Grouping by week
    df_timeseries = df.groupby(by='Week Ending').sum()
    
    # Percent Beds Occupied
    df_timeseries['Percent Beds Occupied'] = df_timeseries['Total Number of Occupied Beds']/df_timeseries['Number of All Beds']

    # Percent of COVID Deaths over Total COVID Cases
    df_timeseries['Percent of COVID Deaths over Total COVID Cases']= df_timeseries['Residents Total COVID-19 Deaths']/(df_timeseries['Residents Total COVID-19 Deaths']+df_timeseries['Residents Total Confirmed COVID-19'])

    return df_timeseries

def get_df_timeseries_by_state(df):
    df_timeseries_by_state = df.groupby(by=['Provider State', 'Week Ending']).sum()
    df_timeseries_by_state = df_timeseries_by_state.reset_index()

    df_timeseries_by_state['Percent Beds Occupied'] = df_timeseries_by_state['Total Number of Occupied Beds']/df_timeseries_by_state['Number of All Beds']

    df_timeseries_by_state['Percent of COVID Deaths over Total COVID Cases'] = df_timeseries_by_state['Residents Total COVID-19 Deaths']/(df_timeseries_by_state['Residents Total COVID-19 Deaths']+df_timeseries_by_state['Residents Total Confirmed COVID-19'])
    
    # df_timeseries_by_state.set_index('Week Ending', inplace=True)
    # df_timeseries_by_state = df_timeseries_by_state.reset_index()
    
    return df_timeseries_by_state

def plot_choropleth_binary_data(col):
    temp = df.groupby(by=['Provider State', 'Week Ending']).agg(['sum', 'count'])
    temp = temp[col]
    temp = temp.reset_index()
    temp['Percentage'] = temp['sum']/temp['count']
    temp['Week Ending'] = temp['Week Ending'].astype(str)
    
    fig = px.choropleth(
    temp,
    locations='Provider State',
    locationmode='USA-states',
    color='Percentage',
    color_continuous_scale='Portland',
    animation_frame='Week Ending',
    range_color=(0, 0.5)
    )

    fig.update_layout(
        title=col,
        margin={"r":0,"t":25,"l":0,"b":0},
        coloraxis_colorbar=dict(title="")
    )

    fig.update_geos(scope="usa", visible=True)

    # Getting lattittudes and longitudes from 'Geolocation' column
    def get_lattitude(geolocation):
        pointRegex = re.compile(r'-?[0-9]+.[0-9]+')
        return float(pointRegex.findall(geolocation)[0])

    def get_longitude(geolocation):
        pointRegex = re.compile(r'-?[0-9]+.[0-9]+')
        return float(pointRegex.findall(geolocation)[1])

    df_by_provider['lat'] = df_by_provider['Geolocation'].apply(get_lattitude)
    df_by_provider['long'] = df_by_provider['Geolocation'].apply(get_longitude)
    
    return fig


# EXECUTIONS

df = clean_data(df)
df_by_state = get_df_by_state(df)
df_by_provider = get_df_by_provider(df)
df_timeseries = get_df_timeseries(df)
df_timeseries_by_state = get_df_timeseries_by_state(df)

# HISTOGRAM 1
histogram_1 = px.histogram(
    df,
    x='Percent of COVID Deaths over Total COVID Cases',
    nbins=50,
    range_x=[0.0, 1],
    range_y=[0, 60000],
    title='Distribution of Percent of COVID Deaths over Total COVID Cases',
    opacity=0.7
)

histogram_1.write_html('./datasets/histogram_1.html')

# HISTOGRAM 2
histogram_2 = px.histogram(
    df.loc[df['Percent Beds Occupied'] <= 1],
    x='Percent Beds Occupied',
    nbins=50,
    range_x=[0, 1],
    range_y=[0, 70000],
    title='Distribution of Percent Beds Occupied',
    opacity=0.7
)

histogram_2.write_html('./datasets/histogram_2.html')

# CHOROPLETH 1
fig = px.choropleth(
    df_by_state,
    locations='Provider State',
    locationmode='USA-states',
    color='Residents Weekly Confirmed COVID-19',
    color_continuous_scale='Portland',
    animation_frame='Week Ending',
    range_color=(0, 500)
)

fig.update_layout(
    title='Residents Weekly Confirmed COVID-19',
    margin={"r":0,"t":25,"l":0,"b":0},
    coloraxis_colorbar=dict(title="")
)

fig.update_geos(scope="usa", visible=True)
fig.write_html('./datasets/choropleth_1.html')

# CHOROPLETH 2
fig = px.choropleth(
    df_by_state,
    locations='Provider State',
    locationmode='USA-states',
    color='Residents Weekly COVID-19 Deaths',
    color_continuous_scale='Portland',
    animation_frame='Week Ending',
    range_color=(0, 500)
)

fig.update_layout(
    title='Residents Weekly COVID-19 Deaths',
    margin={"r":0,"t":25,"l":0,"b":0},
    coloraxis_colorbar=dict(title="")
)

fig.update_geos(scope="usa", visible=True)
fig.write_html('./datasets/choropleth_2.html')

# CHOROPLETH 3
fig = plot_choropleth_binary_data('Shortage of Nursing Staff')
fig.write_html('./datasets/choropleth_3.html')

# CHOROPLETH 4
fig = plot_choropleth_binary_data('Shortage of Aides')
fig.write_html('./datasets/choropleth_4.html')

# BUBBLE MAP 1
fig = px.scatter_geo(
    # Filtering by Admissions > 10 for performance purposes
    df_by_provider.loc[df_by_provider['Residents Weekly Confirmed COVID-19'] >= 5],
    lat = 'long',
    lon = 'lat',
    locationmode='USA-states',
    hover_name='Federal Provider Number',
    size = 'Residents Weekly Confirmed COVID-19',
    animation_frame='Week Ending'
)

fig.update_layout(
    title='Residents Weekly Confirmed COVID-19',
    margin={"r":0,"t":25,"l":0,"b":0}
)

fig.update_geos(scope="usa", visible=True)
fig.write_html('./datasets/bubblemap_1.html')

# BUBBLE MAP 2
fig = px.scatter_geo(
    # Filtering by Admissions > 10 for performance purposes
    df_by_provider.loc[df_by_provider['Residents Weekly COVID-19 Deaths'] >= 3],
    lat = 'long',
    lon = 'lat',
    locationmode='USA-states',
    hover_name='Federal Provider Number',
    size = 'Residents Weekly COVID-19 Deaths',
    animation_frame='Week Ending'
)

fig.update_layout(
    title='Residents Weekly COVID-19 Deaths',
    margin={"r":0,"t":25,"l":0,"b":0}
)

fig.update_geos(scope="usa", visible=True)
fig.write_html('./datasets/bubblemap_2.html')

# TIME SERIES 1
fig = px.line(
    df_timeseries,
    y=['Residents Weekly Confirmed COVID-19',
       'Residents Weekly COVID-19 Deaths',
      ],
    title='Weekly COVID-19 Cases and Deaths'
)

fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=0.99))

fig.write_html('./datasets/line_graph_1.html')

# TIME SERIES 2
fig = px.line(
    df_timeseries,
    y='Percent Beds Occupied',
    title='Percent Beds Occupied'
)

fig.write_html('./datasets/line_graph_2.html')

# TIME SERIES 3
fig = px.line(
    df_timeseries,
    y='Percent of COVID Deaths over Total COVID Cases',
    title='Percent of COVID Deaths over Total COVID Cases'
)
fig.write_html('./datasets/line_graph_3.html')


# TIME SERIES STATE 1
fig = px.line(df_timeseries_by_state, x="Week Ending", y="Residents Weekly COVID-19 Deaths", color="Provider State",
              line_group="Provider State", hover_name="Provider State", title='Residents Weekly COVID-19 Deaths')
fig.write_html('./datasets/line_graph_state_1.html')

# TIME SERIES STATE 2
fig = px.line(df_timeseries_by_state, x="Week Ending", y="Residents Weekly Confirmed COVID-19", color="Provider State",
              line_group="Provider State", hover_name="Provider State", title='Residents Weekly Confirmed COVID-19')
fig.write_html('./datasets/line_graph_state_2.html')

# TIME SERIES STATE 3
fig = px.line(df_timeseries_by_state, x="Week Ending", y="Percent Beds Occupied", color="Provider State",
              line_group="Provider State", hover_name="Provider State", title='Percent Beds Occupied')
fig.write_html('./datasets/line_graph_state_3.html')

# TIME SERIES STATE 4
fig = px.line(df_timeseries_by_state, x="Week Ending", y="Percent of COVID Deaths over Total COVID Cases", color="Provider State",
              line_group="Provider State", hover_name="Provider State", title='Percent of COVID Deaths over Total COVID Cases')
fig.write_html('./datasets/line_graph_state_4.html')