import pandas as pd
from urllib.request import urlopen
import json
import os


def prep_state(state: str, state_code: int):
    columns = ['State', 'County', 'Urban', 'Pop2010', 'OHU2010', 'LILATracts_1And10', 'LILATracts_halfAnd10', 'HUNVFlag', 'LowIncomeTracts',
            'PovertyRate', 'MedianFamilyIncome', 'LA1and10', 'LAhalfand10', 'LA1and20', 'LATracts_half', 'LATracts1', 'LATracts10', 'LATracts20',
            'LAPOP1_10', 'lapophalf', 'lapophalfshare', 'lawhitehalfshare', 'lablackhalfshare', 'laasianhalfshare', 'laaianhalfshare', 'lahisphalfshare',
            'lapop1', 'lapop1share', 'lawhite1share', 'lablack1share', 'laasian1share', 'laaian1share', 'lahisp1share', 'lapop10', 'lapop10share']

    df_path = os.path.join('data', 'datadata.csv')

    df = pd.read_csv(df_path, usecols=columns)

    df_state = df[df['State'] == state]

    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)


    state_counties = [thing for thing in counties['features'] if thing['properties']['STATE'] == str(state_code)]
    # county_data = vt_counties['properties']
    fips = [f"{state_code}{thing['properties']['COUNTY']}" for thing in state_counties]
    fips.sort()
    return df_state, state_counties, fips
