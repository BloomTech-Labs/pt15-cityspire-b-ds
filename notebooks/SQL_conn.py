import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv

data = pd.read_csv('Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_mon.csv')
main = data.iloc[:, 0:9] #this is main part of the table, contains all the identifying information about the place
prices = data.iloc[:, -48:] #this part of the table is the information about prices
house_price = pd.concat([main, prices], axis=1) #merging two pieces of the dataframe together

#performing the same operation for the second table
rental = pd.read_csv('Metro_ZORI_AllHomesPlusMultifamily_SSA.csv')
rental_data = rental.iloc[:, -48:]
rental_main = rental.iloc[:,:3]
rental_rate = pd.concat([rental_main, rental_data], axis = 1)

def cleaning(df_prices):
    """
    'Metro' column contains some NaN values, which is possibly because some locations do
    not have any Metro assigned to it. This function replaces these NaNs to 'None'.
    """
    house_price['Metro'] = house_price['Metro'].replace(np.nan, 'None')


#uploading data to PG SQL server
load_dotenv()
DB_USER=os.getenv("DB_USER")
DB_PASS=os.getenv("DB_PASS")
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")
database_url = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = sqlalchemy.create_engine(database_url)
house_price.to_sql('house_prices', engine)
rental_rate.to_sql('rental_rates', engine)




