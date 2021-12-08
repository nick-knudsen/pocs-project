import pandas as pd
from urllib.request import urlopen
import json


def prep_vermont():
    columns = ['State', 'County', 'Urban', 'Pop2010', 'OHU2010', 'LILATracts_1And10', 'LILATracts_halfAnd10', 'HUNVFlag', 'LowIncomeTracts',
            'PovertyRate', 'MedianFamilyIncome', 'LA1and10', 'LAhalfand10', 'LA1and20', 'LATracts_half', 'LATracts1', 'LATracts10', 'LATracts20',
            'LAPOP1_10', 'lapophalf', 'lapophalfshare', 'lawhitehalfshare', 'lablackhalfshare', 'laasianhalfshare', 'laaianhalfshare', 'lahisphalfshare', 
            'lapop1', 'lapop1share', 'lawhite1share', 'lablack1share', 'laasian1share', 'laaian1share', 'lahisp1share', 'lapop10', 'lapop10share']

    df_path = r'datadata.csv'

    df = pd.read_csv(df_path, usecols=columns)

    df_vermont = df[df['State'] == 'Vermont']

    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)


    vt_counties = [thing for thing in counties['features'] if thing['properties']['STATE'] == '50']
    # county_data = vt_counties['properties']
    fips = [f"50{thing['properties']['COUNTY']}" for thing in vt_counties]
    fips.sort()
    return df_vermont, vt_counties, fips
