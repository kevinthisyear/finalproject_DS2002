import os
from retrieve_data import retreive_data, generate_codebook_md
from clean_data import clean_data
from access_cloud import store_data_to_cloud
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
CODEBOOK_URL = "https://raw.githubusercontent.com/owid/co2-data/refs/heads/master/owid-co2-codebook.csv"
script_dir = os.path.dirname(os.path.abspath(__file__))
FILEPATH_TO_RAW_DATA = os.path.join(os.path.dirname(script_dir), "raw_data", "owid-co2-data.csv")
FILEPATH_TO_CLEAN_DATA = os.path.join(os.path.dirname(script_dir), "data", "cleaned_emissions_data.csv")
YEAR_START = 1950
YEAR_END = 2023

if __name__ == "__main__":
    # EXTRACT
    retreive_data(URL)
    output_markdown_file = "raw_data/codebook.md"
    generate_codebook_md(CODEBOOK_URL, output_markdown_file)

    # TRANSFORM
    clean_data(FILEPATH_TO_RAW_DATA, YEAR_START, YEAR_END)

    # LOAD
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    store_data_to_cloud(client=client, filepath=FILEPATH_TO_CLEAN_DATA, db_name="data", collection_name="emissions")
    store_data_to_cloud(client=client, filepath=os.path.join(os.path.dirname(script_dir), "data", "country_data.csv"), db_name="data", collection_name="country_data")
    store_data_to_cloud(client=client, filepath=os.path.join(os.path.dirname(script_dir), "data", "continent_data.csv"), db_name="data", collection_name="continent_data")
    store_data_to_cloud(client=client, filepath=os.path.join(os.path.dirname(script_dir), "data", "socioeconomic_data.csv"), db_name="data", collection_name="socioeconomic_data")
    store_data_to_cloud(client=client, filepath=os.path.join(os.path.dirname(script_dir), "raw_data", "owid-co2-codebook.csv"), db_name="data", collection_name="codebook")
    
