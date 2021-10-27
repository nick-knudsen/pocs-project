import pandas as pd
from urllib.request import urlopen
import json


df = pd.read_csv('datadata.csv')


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
condensed_vermont = vermont.groupby('County').mean()


with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

vt_counties = [thing for thing in counties['features'] if thing['properties']['STATE'] == '50']
# county_data = vt_counties['properties']
fips = [f"50{thing['properties']['COUNTY']}" for thing in vt_counties]


import plotly.express as px
import plotly.figure_factory as ff

colorscale = [
    'rgb(193, 193, 193)',
    'rgb(239,239,239)',
    'rgb(195, 196, 222)',
    'rgb(144,148,194)',
    'rgb(101,104,168)',
    'rgb(65, 53, 132)'
]


values = condensed_vermont['Pop2010']
values = [i + 1 for i in range(14)]
fig = ff.create_choropleth(
    fips=fips, values=values, scope=['VT'],
    binning_endpoints=[2, 4, 6, 8, 10], colorscale=colorscale,
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, round_legend_values=True,
    legend_title='Population by County', title='Vermont'
)
fig.layout.template = None
fig.show()