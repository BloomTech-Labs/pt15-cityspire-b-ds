import pandas as pd
import numpy as np
from pathlib import Path
import sqlalchemy
import os
from dotenv import load_dotenv

us_state_abbrev = {
    'ALABAMA': 'AL',
    'ALASKA': 'AK',
    'ARIZONA': 'AZ',
    'ARKANSAS': 'AR',
    'CALIFORNIA': 'CA',
    'COLORADO': 'CO',
    'CONNECTICUT': 'CT',
    'DELAWARE': 'DE',
    'DISTRICT OF COLUMBIA': 'DC',
    'FLORIDA': 'FL',
    'GEORGIA': 'GA',
    'GUAM': 'GU',
    'HAWAII': 'HI',
    'IDAHO': 'ID',
    'ILLINOIS': 'IL',
    'INDIANA': 'IN',
    'IOWA': 'IA',
    'KANSAS': 'KS',
    'KENTUCKY': 'KY',
    'LOUISIANA': 'LA',
    'MAINE': 'ME',
    'MARYLAND': 'MD',
    'MASSACHUSETTS': 'MA',
    'MICHIGAN': 'MI',
    'MINNESOTA': 'MN',
    'MISSISSIPPI': 'MS',
    'MISSOURI': 'MO',
    'MONTANA': 'MT',
    'NEBRASKA': 'NE',
    'NEVADA': 'NV',
    'NEW HAMPSHIRE': 'NH',
    'NEW JERSEY': 'NJ',
    'NEW MEXICO': 'NM',
    'NEW YORK': 'NY',
    'NORTH CAROLINA': 'NC',
    'NORTH DAKOTA': 'ND',
    'OHIO': 'OH',
    'OKLAHOMA': 'OK',
    'OREGON': 'OR',
    'PENNSYLVANIA': 'PA',
    'PUERTO RICO': 'PR',
    'RHODE ISLAND': 'RI',
    'SOUTH CAROLINA': 'SC',
    'SOUTH DAKOTA': 'SD',
    'TENNESSEE': 'TN',
    'TEXAS': 'TX',
    'UTAH': 'UT',
    'VERMONT': 'VT',
    'VIRGINIA': 'VA',
    'WASHINGTON': 'WA',
    'WEST VIRGINIA': 'WV',
    'WISCONSIN': 'WI',
    'WYOMING': 'WY'
}

us_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
             'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
             'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
             'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
             'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI',
             'WY']

# Import FBI city crime data for 2019
CSV_PATH = Path('CityCrimeClean.py').cwd().parent / 'data' / 'raw' / 'Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2019.xls'
print('CSV_PATH:', CSV_PATH)
city_crime_2019 = pd.read_excel(CSV_PATH, header=3, skipfooter=8,
                                usecols=['State', 'City', 'Violent\ncrime', 'Property\ncrime'])

# Select required data frame columns
city_crime_2019.columns = ['State', 'City', 'Violent Crime', 'Property Crime']

# Clean State names
city_crime_2019['State'] = city_crime_2019['State'].astype(str)
city_crime_2019['State'] = city_crime_2019['State'].str.replace('\d+', '')
city_crime_2019['State'] = city_crime_2019['State'].str.replace(
    ' - Metropolitan Counties', '')
city_crime_2019['State'] = city_crime_2019['State'].str.replace(
    ' - Nonmetropolitan Counties', '')

# Remove State multi-indexing by iterating through State names
currState = None
for index, value in city_crime_2019['State'].items():
    if value != 'nan':
        currState = value
    else:
        city_crime_2019.loc[index, 'State'] = currState

# Make State names uppercase to be consistent with state abbreviations dict
city_crime_2019['State'] = city_crime_2019['State'].str.upper()

# Replace State names with abbreviations
city_crime_2019['State'] = city_crime_2019['State'].replace(us_state_abbrev)

# Sanity Check
assert list(city_crime_2019['State'].unique()) == us_states

# Clean city names
city_crime_2019['City'] = city_crime_2019['City'].str.replace('\d+', '')
city_crime_2019['City'] = city_crime_2019['City'].replace('Boston,', 'Boston')

# Store cleaned data in directory
CSV_PATH = Path('CityCrimeClean.py').cwd().parent / 'data' / 'clean' / 'CityCrimeClean.csv'
print('CSV_PATH:', CSV_PATH)
city_crime_2019.to_csv(CSV_PATH)

# Insert cleaned crime dataset into database
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = sqlalchemy.create_engine(DB_URL)
connection = engine.connect()
city_crime_2019.to_sql("city_crime_rates", connection, if_exists='fail', method='multi')
