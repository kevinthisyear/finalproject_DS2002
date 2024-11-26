import requests

from logger_setup import setup_logger

# Get the shared logger
logger = setup_logger()

def retreive_data(url):
    # Send a GET request to the URL
    logger.info("Retreiving data from github URL...")
    response = requests.get(url)

    if response.status_code == 200:
        with open("raw_data/owid-co2-data.csv", "wb") as file:
            file.write(response.content)
        logger.info("File downloaded successfully!")
    else:
        logger.error(f"Failed to download file. Status code: {response.status_code}")
