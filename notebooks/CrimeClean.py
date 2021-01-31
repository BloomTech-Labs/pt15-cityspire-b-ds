import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
from pathlib import Path


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

    crime_2017 = clean_crime_data(crime_2017)
    crime_2018 = clean_crime_data(crime_2018)
    crime_2019 = clean_crime_data(crime_2019)

    print(crime_2019)
