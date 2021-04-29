'''

Steps 1 and 2 of automation.md
Download of shapefiles?

See Python – Project 0 written JN Matthews?


'''



#GEO_ID and NAME is same

# Delete Margin columns, i.e. check for an M
delete_columns = \
    'B03002_009E', 'B03002_010E', 'B03002_019E', 'B03002_020E', 'B03002_021E',

rename_columns = {\
    'B03002_001E': 'TOTPOP',
    'B03002_002E': 'NH_WHITE',
    'B03002_003E': 'NH_BLACK',
    'B03002_004E': 'NH_AMIN',
    'B03002_005E': 'NH_ASIAN',
    'B03002_006E': 'NH_NHPI',
    'B03002_007E': 'NH_OTHER',
    'B03002_008E': 'NH_2MORE',
    'B03002_011E': 'HISP',
    'B03002_012E': 'H_WHITE',
    'B03002_013E': 'H_BLACK',
    'B03002_014E': 'H_AMIN',
    'B03002_015E': 'H_ASIAN',
    'B03002_016E': 'H_NHPI',
    'B03002_017E': 'H_OTHER',
    'B03002_018E': 'H_2MORE'}

# Download B03002, ACS20195Y 
# Remove margin of error columns
# Truncate GEO_ID to right 12 characters
# After creating csv, make csvt to help QGIS with datatypes

import os 

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import requests
from tqdm import tqdm

"""
    ###### Format for 2010 Decennial Summary File 1 ########################

    resp = requests.get(
        "https://api.census.gov/data/2010/dec/sf1"
        "?get=NAME&for=county:*&in=state:{}".format(state_fips))


variables = [
    # pop
    "P005001", "P005003", "P005004", "P005005", "P005006", "P005007", "P005008", "P005009", "P005010",
    "P005011", "P005012", "P005013", "P005014", "P005015", "P005016", "P005017",
    # vap
    "P011001", "P011002", "P011005", "P011006",  "P011007", "P011008", "P011009", "P011010", "P011011",
]

keys = [
    # pop
    "TOTPOP", "NH_WHITE", "NH_BLACK", "NH_AMIN ", "NH_ASIAN", "NH_NHPI", "NH_OTHER", "NH_2MORE",
    "HISP", "H_WHITE", "H_BLACK", "H_AMIN", "H_ASIAN", "H_NHPI", "H_OTHER", "H_2MORE",
    # vap
    "VAP", "HVAP", "WVAP", "BVAP", "AMINVAP", "ASIANVAP", "NHPIVAP", "OTHERVAP", "2MOREVAP",
]

    ###### Format for 2019 Decennial ######################################

https://api.census.gov/data/2019/acs/acs5?get=GEO_ID,B03002_001E,B03002_003E,B03002_004E&for=block%20group:*&in=state:22&in=county:071

[["NAME","B03002_001E","B03002_003E","B03002_004E","state","county","tract","block group"],
["Block Group 2, Census Tract 108, Orleans Parish, Louisiana","970","855","32","22","071","010800","2"],

GEOID: 220710108002
GEOID = state + county + tract + blockgroup

"""

state_fips = "22"
county_fips = "071"
variables = list(rename_columns.keys())

def blockgroup_data_for_county(state_fips, county_fips, variables=variables):
    """ Collects blockgroup data for given county

    Parameters
    ----------
    state_fips : str
        Two digit code for given state
    county_fips : str
        Three digit code for given county
    variables : list, optional
        List of alphanumeric codes for requested Census columns

    Returns
    -------
    pandas.DataFrame
        Census result processed into DataFrame table. 

    Raises
    ------
    """

    num_col_chunks = int(np.ceil(len(variables) / 50))
    chunks = [variables[i::num_col_chunks] for i in range(num_col_chunks)]
    variable_lookup = rename_columns ### rewrite, redundant ###
    data = pd.DataFrame()
    for chunk in chunks:
        url = (
            "https://api.census.gov/data/2019/acs/acs5"
            + "?get=GEO_ID,{}&for=block group:*".format(",".join(chunk))
            + "&in=state:{}&in=county:{}".format(state_fips, county_fips)
        )
        resp = requests.get(url)
        header, *rows = resp.json()
        columns = [variable_lookup.get(column_name, column_name) for column_name in header]

        dtypes = {key: int for key in columns}
        dtypes.update({key: str for key in ["GEO_ID","state", "county", "tract", "block group"]})
        df = pd.DataFrame.from_records(rows, columns=columns).astype(dtypes)
        if data.empty: 
            data = df
        else:
            data = pd.merge(data, df, on=["state", "county", "block group"])

    data["geoid"] = data["state"] + data["county"] + data["tract"] + data["block group"]
    return data

def block_data_for_counties(state_fips, county_fips, variables=variables):
    """ Collects blockgroup data for list of counties, all in one state.

    Parameters
    ----------
    state_fips : str
        Two digit code for given state
    county_fips : list
        List of three digit code of requested county
    variables : list, optional
        List of alphanumeric codes for requested Census columns

    Returns
    -------
    pandas.DataFrame
        Concatenated pandas DataFrame of data from all counties. 

    Raises
    ------
    """
    county_fips_codes = counties(state_fips)
    return pd.concat(
        [
            blockgroup_data_for_county(state_fips, county_fips, variables)
            for county_fips in tqdm(county_fips_codes)
        ]
    )

"""

import os; os.getcwd(); os.chdir('automation-temp'); from process_census import *
data = blockgroup_data_for_county(state_fips, county_fips, variables)
data.to_csv('filename')



"""
"""
def block_data_for_state(state_fips, variables=variables, keys=keys):
    county_fips_codes = counties(state_fips)
    return pd.concat(
        [
            block_data_for_county(state_fips, county_fips, variables, keys)
            for county_fips in tqdm(county_fips_codes)
        ]
    )
"""