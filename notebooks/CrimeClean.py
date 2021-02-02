import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
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


us_states = ['AL', 'AZ', 'AR', 'CA', 'CO', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',
             'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MI', 'MN', 'MS', 'MO',
             'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
             'OR', 'PA', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
             'WI', 'WY']


def scrape_data():
    '''
        Scrape government website for mapping of County names to FIPs
        Code source: https://stackoverflow.com/questions/52690994/web-scraping-python-writing-to-a-csv
    '''

    url = requests.get("https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697")
    soup = bs(url.content, 'html.parser')

    fips = pd.DataFrame(columns=['FIPS', 'County', 'State'])

    row_count = 0
    # Iterate through table
    for tr in soup.find_all("tr"):
        data = []

        # Iterate through table row (for each non-header row)
        for td in tr.find_all("td"):
            if td.a:
                data.append(td.a.text.strip())
            else:
                data.append(td.text.strip())

        # Append data row to fips data frame
        if data:
            if len(data) == 3 and data != ['Home', 'Home', 'Home'] and data != ['', '', '']:
                fips = fips.append({'FIPS':data[0], 'County':data[1], 'State':data[2]}, ignore_index=True)

    # Sanity check
    assert len(fips), 3232

    return fips


def clean_crime_data(df):
    # Select required data frame columns
    df.columns = ['State', 'County', 'Violent Crime', 'Property Crime']

    # Clean State names
    df['State'] = df['State'].astype(str)
    df['State'] = df['State'].str.replace('\d+', '')
    df['State'] = df['State'].str.replace(' - Metropolitan Counties', '')
    df['State'] = df['State'].str.replace(' - Nonmetropolitan Counties', '')

    # Remove State multi-indexing by iterating through State names
    currState = None
    for index, value in df['State'].items():
        if value != 'nan':
            currState = value
        else:
            df.loc[index, 'State'] = currState

    # Make State names uppercase to be consistent with state abbreviations dict
    df['State'] = df['State'].str.upper()

    # Replace State names with abbreviations
    global us_state_abbrev
    df['State'] = df['State'].replace(us_state_abbrev)

    # Sanity Check
    global us_states
    assert list(df['State'].unique()) == us_states

    # Clean County names in crime data to be consistent with County names in FIPS dataset
    df['County'] = df['County'].str.replace('\d+', '')
    df['County'] = df['County'].str.replace(' County Unified Police Department', '')
    df['County'] = df['County'].str.replace(' County Police Department', '')
    df['County'] = df['County'].str.replace(' Police Department', '')
    df['County'] = df['County'].str.replace('Westchester Public Safety', 'Westchester')
    df['County'] = df['County'].str.replace(' County', '')
    df['County'] = df['County'].str.replace('DeWitt', 'De Witt')
    df['County'] = df['County'].str.replace('DeKalb', 'De Kalb')
    df['County'] = df['County'].str.replace('DeSoto', 'De Soto')
    df['County'] = df['County'].str.replace('DuPage', 'Du Page')
    df['County'] = df['County'].str.replace('Lamoure', 'La Moure')
    df['County'] = df['County'].str.replace('Butte-Silver Bow', 'Silver Bow')
    df['County'] = df['County'].str.replace('Hartsville/Trousdale', 'Trousdale')
    df['County'] = df['County'].str.replace("O'Brien", 'O Brien')
    df['County'] = df['County'].str.replace("Prince George's", 'Prince George')
    df['County'] = df['County'].str.replace("Queen Anne's", 'Queen Annes')
    df['County'] = df['County'].str.replace('St. Charles', 'St Charles')
    df['County'] = df['County'].str.replace('St. Clair', 'St Clair')
    df['County'] = df['County'].str.replace('St. Francis', 'St Francis')
    df['County'] = df['County'].str.replace('St. Helena', 'St Helena')
    df['County'] = df['County'].str.replace('St. James', 'St James')
    df['County'] = df['County'].str.replace('St. John the Baptist', 'St John the Baptist')
    df['County'] = df['County'].str.replace('St. Johns', 'St Johns')
    df['County'] = df['County'].str.replace('St. Joseph', 'St Joseph')
    df['County'] = df['County'].str.replace('St. Lawrence', 'St Lawrence')
    df['County'] = df['County'].str.replace('St. Louis', 'St Louis')
    df['County'] = df['County'].str.replace('St. Lucie', 'St Lucie')
    df['County'] = df['County'].str.replace('St. Landry', 'St Landry')
    df['County'] = df['County'].str.replace('St. Martin', 'St Martin')
    df['County'] = df['County'].str.replace('St. Mary', 'St Mary')
    df['County'] = df['County'].str.replace("St. Mary's", 'St Mary')
    df['County'] = df['County'].str.replace("St Mary's", 'St Mary')
    df['County'] = df['County'].str.replace('St. Tammany', 'Trousdale')
    df['County'] = df['County'].str.replace('St. Bernard', 'St Bernard')
    df['County'] = df['County'].str.replace('St. Francois', 'St Francois')
    df['County'] = df['County'].str.replace('Crockett,', 'Crockett')
    df['County'] = df['County'].str.replace('King,', 'King')
    df['County'] = df['County'].str.replace('Lake,', 'Lake')
    df['County'] = df['County'].str.replace('Augusta-Richmond', 'Augusta')
    df['County'] = df['County'].str.replace('LaGrange', 'La Grange')

    # Sanity check
    # nan is included because Alabama has all empty values in 2019
    x = set(df['County'].values).difference(fips['County'].values)
    assert x == {np.nan} or x == set()

    # Merge/sum duplicate rows
    df = df.groupby(['State', 'County']).sum()
    df = df.reset_index()

    return df


if __name__ == "__main__":

    # Import county FIPS data
    fips = scrape_data()

    # Import FBI Crime data for 2017
    CSV_PATH = Path('CrimeClean.py').cwd().parent / 'data' / 'raw' / \
        'Table_10_Offenses_Known_to_Law_Enforcement_by_State_by_Metropolitan_and_Nonmetropolitan_Counties_2017.xls'
    crime_2017 = pd.read_excel(CSV_PATH, header=4, skipfooter=8,
                           usecols=['State', 'County', 'Violent\ncrime', 'Property\ncrime'])

    # # Import FBI Crime data for 2017
    CSV_PATH = Path('CrimeClean.py').cwd().parent / 'data' / 'raw' / \
        'Table_10_Offenses_Known_to_Law_Enforcement_by_State_by_Metropolitan_and_Nonmetropolitan_Counties_2018.xls'
    crime_2018 = pd.read_excel(CSV_PATH, header=4, skipfooter=8,
                           usecols=['State', 'County', 'Violent\ncrime', 'Property\ncrime'])

    # # Import FBI Crime data for 2019
    CSV_PATH = Path('CrimeClean.py').cwd().parent / 'data' / 'raw' / \
        'Table_10_Offenses_Known_to_Law_Enforcement_by_State_by_Metropolitan_and_Nonmetropolitan_Counties_2019.xls'
    crime_2019 = pd.read_excel(CSV_PATH, header=4, skipfooter=8,
                           usecols=['State', 'County', 'Violent\ncrime', 'Property\ncrime'])

    # Clean each crime dataset
    crime_2017_clean = clean_crime_data(crime_2017)
    crime_2018_clean = clean_crime_data(crime_2018)
    crime_2019_clean = clean_crime_data(crime_2019)

    # Join three crime datasets
    df1 = pd.merge(crime_2017_clean, crime_2018_clean,
                on=['State', 'County'], how='outer')
    df2 = pd.merge(df1, crime_2019_clean, on=['State', 'County'], how='outer')

    # Join FIPS dataset
    df3 = pd.merge(df2, fips, on=['State', 'County'], how='left')

    # Calculate mean across three crime datasets
    df3['Mean Violent Crime'] = df3[['Violent Crime_x',
                                                'Violent Crime_y', 'Violent Crime']].mean(axis=1)
    df3['Mean Property Crime'] = df3[['Property Crime_x',
                                                'Property Crime_y', 'Property Crime']].mean(axis=1)

    # Select the two new columns with mean data
    df3 = df3[['County', 'FIPS', 'State',
            'Mean Violent Crime', 'Mean Property Crime']]

    # Drop rows with no FIPS data
    df4 = df3.dropna(subset=['FIPS'])

    # Convert FIPS data from object type to in64 type
    df4['FIPS'] = df4['FIPS'].astype('int64')

    # Import zips <-> fips mapping dataset
    CSV_PATH = Path('CrimeClean.py').cwd().parent / 'data' / 'raw' / \
        'ZIP-COUNTY-FIPS_2017-06.csv'
    zips = pd.read_csv(CSV_PATH, usecols=['ZIP', 'STATE', 'STCOUNTYFP'])
    zips.columns = ['ZIP', 'State', 'FIPS']

    # Merge crime dataset with zips dataset
    df5 = pd.merge(df4, zips, on=['FIPS'], how='left')

    # Clean final dataset
    df5 = df5.drop('State_y', axis=1)
    df5 = df5[['ZIP', 'County', 'FIPS', 'State_x', 'Mean Violent Crime', 'Mean Property Crime']]
    df5.columns = ['ZIP', 'County', 'FIPS', 'State', 'Mean Violent Crime', 'Mean Property Crime']

    # Store cleaned data in directory
    CSV_PATH = Path('CrimeClean.py').cwd().parent / 'data' / 'clean' / 'crime_clean.csv'
    print('CSV_PATH', CSV_PATH)
    df5.to_csv(CSV_PATH)

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
    df5.to_sql("crime_rates", connection, if_exists='fail', method='multi')
