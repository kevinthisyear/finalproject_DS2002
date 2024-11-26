from logger_setup import setup_logger
import os
from retrieve_data import retreive_data
from clean_data import clean_data
from access_cloud import store_data_to_cloud
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

# Get environment variables
MONGO_URI = os.getenv('MONGO_URI')
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
script_dir = os.path.dirname(os.path.abspath(__file__))
FILEPATH_TO_RAW_DATA = os.path.join(os.path.dirname(script_dir), "raw_data", "owid-co2-data.csv")
FILEPATH_TO_CLEAN_DATA = os.path.join(os.path.dirname(script_dir), "data", "cleaned_emissions_data.csv")
YEAR_START = 1950
YEAR_END = 2023

if __name__ == "__main__":
    # EXTRACT
    retreive_data(URL)

    # TRANSFORM
    clean_data(FILEPATH_TO_RAW_DATA, YEAR_START, YEAR_END)

    # LOAD
    # Create a new client and connect to the server
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    store_data_to_cloud(client=client, filepath=FILEPATH_TO_CLEAN_DATA, db_name="data", collection_name="emissions")
    store_data_to_cloud(client=client, filepath=os.path.join(os.path.dirname(script_dir), "data", "country_data.csv"), db_name="data", collection_name="country_data")
    store_data_to_cloud(client=client, filepath=os.path.join(os.path.dirname(script_dir), "data", "continent_data.csv"), db_name="data", collection_name="continent_data")
    store_data_to_cloud(client=client, filepath=os.path.join(os.path.dirname(script_dir), "data", "nations_data.csv"), db_name="data", collection_name="nations_data")
    store_data_to_cloud(client=client, filepath=os.path.join(os.path.dirname(script_dir), "data", "socioeconomic_data.csv"), db_name="data", collection_name="socioeconomic_data")
    


