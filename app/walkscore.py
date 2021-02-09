import os
import requests
import sqlalchemy
from dotenv import load_dotenv


def get_walkscore(WALKSCORE_ZIP: str) -> (76, 'Very Walkable'):

    # Access population_size table in db and return city, state, lat and lon for record with specified zip
    load_dotenv()
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    engine = sqlalchemy.create_engine(DB_URL)
    conn = engine.connect()
    sql = "SELECT city_ascii, state_id, lat, lng FROM population_size WHERE zips LIKE '%%"+WALKSCORE_ZIP+"%%'"
    res = conn.execute(sql)
    zip_data = res.fetchone() # tuple with four values, ie. ('Boston', 'MA', 42.3188, -71.0846)
    conn.close()

    # Access official WalkScore API and return walkscore and description
    WALKSCORE_ROUTE = "https://api.walkscore.com/score?format=json&address="
    WALKSCORE_API_KEY = os.getenv("WALKSCORE_API_KEY")
    WALKSCORE_CITY = zip_data[0]
    WALKSCORE_STATE = zip_data[1]
    WALKSCORE_LAT = str(zip_data[2])
    WALKSCORE_LON = str(zip_data[3])

    API_URL = WALKSCORE_ROUTE+WALKSCORE_CITY+"%20"+WALKSCORE_STATE+"%20"+WALKSCORE_ZIP + \
        "&lat="+WALKSCORE_LAT+"&lon="+WALKSCORE_LON+"&wsapikey="+WALKSCORE_API_KEY
    response = requests.get(API_URL)

    return (response.json()['walkscore'], response.json()['description'])
