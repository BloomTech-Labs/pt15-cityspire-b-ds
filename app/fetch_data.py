import os
import requests
import sqlalchemy
from dotenv import load_dotenv

def fetch_data(city, state, ZIPcode, latitude, longitude):

    # Verify ZIPcode, latitude and longitude have correct data types
    try:
        int(ZIPcode)
        float(latitude)
        float(longitude)
    except:
        print(f'Error: {ZIPcode} must be an integer. And {latitude} and {longitude} must be floats')
        return None


    # Fetch data from population_size table
    def fetch_population_size():

        # First attempt to fetch 1 record from population_size table with only ZIPcode values
        SQL = f'''SELECT "population", "density" FROM population_size WHERE "zips" LIKE '%%{ZIPcode}%%';'''
        results = list(conn.execute(SQL))
        if len(results) == 1:
            return results[0]

        # Next attempt to fetch 1 record from population_size table with only City and State values
        SQL = f'''SELECT "population", "density" FROM population_size WHERE "city_ascii" = '{city}' AND "state_id" = '{state}';'''
        results = list(conn.execute(SQL))
        if len(results) == 1:
            return results[0]

        # Finally attempt to fetch 1 record from population_size table with City and State and ZIPcode values
        SQL = f'''SELECT "population", "density" FROM population_size WHERE "city_ascii" = '{city}' AND "state_id" = '{state}' AND "zips" LIKE '%%{ZIPcode}%%';'''
        results = list(conn.execute(SQL))
        if len(results) == 1:
            return results[0]

        # If the above fails then return None
        return (None, None)

    # Fetch data from Walk Score API

    def fetch_walk_score():
        API_URL = WALKSCORE_API_ROUTE+city+"%20"+state+"%20"+ZIPcode + \
            "&lat="+latitude+"&lon="+longitude+"&wsapikey="+WALKSCORE_API_KEY
        response = requests.get(API_URL).json()

        # Check if API call is successful and if so then return values
        if len(response) > 1:
            return (response['walkscore'], response['description'])
        # If API call is successfull then return None
        else:
            return (None, None)

    # Fetch data from city_crime_rates and crime_rates tables
    def fetch_crime_rates():

        # First attempt to fetch 1 record from from city_crime_rates with City and State values
        SQL = f'''SELECT ("Violent Crime" / 100000), ("Property Crime" / 100000) FROM city_crime_rates WHERE "City" = '{city}' AND "State" = '{state}';'''
        results = list(conn.execute(SQL))
        if len(results) == 1:
            return results[0]

        # Next attempt to fetch 1 record from from crime_rates with ZIPcode and State values
        SQL = f'''SELECT ("Mean Violent Crime" / 100000), ("Mean Property Crime" / 100000) FROM crime_rates WHERE "ZIP" = '{ZIPcode}' AND "State" = '{state}';'''
        results = list(conn.execute(SQL))
        if len(results) == 1:
            return results[0]

        # If the above fails then return None
        return (None, None)

    # Fetch data from zip_rent table

    def fetch_zip_rent():

        # List of all months in 2020 and 2021
        rent_dates = ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01', '2020-06-01',
                      '2020-07-01', '2020-08-01', '2020-09-01', '2020-10-01', '2020-11-01', '2020-12-01',
                      '2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01', '2021-06-01',
                      '2021-07-01', '2021-08-01', '2021-09-01', '2021-10-01', '2021-11-01', '2021-12-01']

        # First attempt to fetch 1 record from fetch_zip_rent table with only ZIPcode values
        SQL = f'''SELECT "{'", "'.join(rent_dates)}" FROM zip_rent WHERE "RegionName" = '{ZIPcode}';'''
        results = list(conn.execute(SQL))
        if len(results) == 1:
            return {key: value for key, value in list(zip(rent_dates, results[0]))}

        # Next attempt to fetch 1 record from zip_rent table with only City and State values
        SQL = f'''SELECT "{'", "'.join(rent_dates)}" FROM zip_rent WHERE "MsaName" = '{city+", "+state}';'''
        results = list(conn.execute(SQL))
        if len(results) == 1:
            return {key: value for key, value in list(zip(rent_dates, results[0]))}

        # Finally attempt to fetch 1 record from zip_rent table with City and State and ZIPcode values
        SQL = f'''SELECT "{'", "'.join(rent_dates)}" FROM zip_rent WHERE "MsaName" = '{city+", "+state}' AND "RegionName" = '{ZIPcode}'';'''
        if len(results) == 1:
            return {key: value for key, value in list(zip(rent_dates, results[0]))}

        # If the above fails then return None
        return None

    # Fetch data from cost_of_living table

    def fetch_cost_of_living():

        # Attempt to fetch 1 record from from cost_of_living table with City and State values
        SQL = f'''SELECT "Cost of Living Index" FROM cost_of_living WHERE "City" = '{city}' AND "State" = '{state}';'''
        results = list(conn.execute(SQL))
        if len(results) == 1:
            return results[0][0]

        # If the above fails then return None
        return None

    load_dotenv()
    WALKSCORE_API_ROUTE = "https://api.walkscore.com/score?format=json&address="
    WALKSCORE_API_KEY = os.getenv("WALKSCORE_API_KEY")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    city_data = {}
    city_data['ZIPcode'] = ZIPcode
    city_data['City'], city_data['State'] = city, state
    city_data['Latitude'], city_data['Longitude'] = latitude, longitude

    engine = sqlalchemy.create_engine(DB_URL)
    conn = engine.connect()

    city_data['Population'], city_data['Density'] = fetch_population_size()
    city_data['WalkScore'], city_data['WalkScoreDescription'] = fetch_walk_score()
    city_data['ViolentCrimeRate'], city_data['PropertyCrimeRate'] = fetch_crime_rates()
    city_data['MonthlyRents'] = fetch_zip_rent()
    city_data['CostOfLivingIndex'] = fetch_cost_of_living()

    conn.close()

    return city_data
