import pandas as pd
from urllib.request import urlopen
import json


df = pd.read_csv('datadata.csv')

columns = ['State', 'County', 'Urban', 'Pop2010', 'OHU2010', 'LILATracts_1And10', 'LILATracts_halfAnd10', 'HUNVFlag', 'LowIncomeTracts',
           'PovertyRate', 'MedianFamilyIncome', 'LA1and10', 'LAhalfand10', 'LA1and20', 'LATracts_half', 'LATracts1', 'LATracts10', 'LATracts20',
           'lawhitehalfshare', 'lablackhalfshare', 'laasianhalfshare', 'laaianhalfshare', 'lahisphalfshare', 'lawhite1share', 'lablack1share',
            'laasian1share', 'laaian1share', 'lahisp1share'
           ]
df = df.filter(items=columns)

ffr = pd.read_csv('FastFoodRestaurants.csv')
columns_ffr = ['latitude', 'longitude', 'name']
ffr = ffr[ffr['province'] == 'VT']
ffr = ffr.filter(items=columns_ffr)



# # important columns
# """
# By:
#     State
#     County

# Show:
#     Pop2010
#     PovertyRate
#     MedianFamilyIncome


# """

vermont = df[df['State'] == 'Vermont']

vt_counties = vermont['County'].unique()
condensed_vermont = vermont.groupby('County').sum()
mean_poverty = vermont.groupby('County').mean()['PovertyRate']

long = list(ffr['longitude'])
lat = list(ffr['latitude'])
name = list(ffr['name'])

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

vt_counties = [thing for thing in counties['features'] if thing['properties']['STATE'] == '50']
# county_data = vt_counties['properties']
fips = [f"50{thing['properties']['COUNTY']}" for thing in vt_counties]
fips.sort()

import plotly.express as px
import plotly.figure_factory as ff

colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
    "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
    "#08519c", "#0b4083", "#08306b"]

values = condensed_vermont['Pop2010'].values
values = mean_poverty.round(3).values
endpoints = sorted([int(val) for val in values])

fig = ff.create_choropleth(
    fips=fips, values=values, scope=['VT'],
    binning_endpoints=[], colorscale=colorscale,
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, round_legend_values=True,
    legend_title='Poverty Rate by County', title='Vermont'
)

fig.show()

fig1 = px.scatter_mapbox(ffr, hover_name=list(ffr['name']), lat=list(ffr["latitude"]), lon=list(ffr["longitude"]),
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=6)
                 
fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig1.show()
