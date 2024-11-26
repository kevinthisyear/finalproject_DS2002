from logger_setup import setup_logger
import os
from retrieve_data import retreive_data
from clean_data import clean_data

URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
script_dir = os.path.dirname(os.path.abspath(__file__))
FILEPATH_TO_CLEAN_DATA = os.path.join(os.path.dirname(script_dir), "raw_data", "owid-co2-data.csv")
YEAR_START = 1950
YEAR_END = 2023

if __name__ == "__main__":
    retreive_data(URL)

    clean_data(FILEPATH_TO_CLEAN_DATA, YEAR_START, YEAR_END)
