from logger_setup import setup_logger
import os
from retrieve_data import retreive_data
from clean_data import clean_data
from access_cloud import store_data_to_cloud
from dotenv import load_dotenv

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
    store_data_to_cloud(uri=MONGO_URI, filepath=FILEPATH_TO_CLEAN_DATA, db_name="data", collection_name="emissions")

