import requests

from logger_setup import setup_logger
import pandas as pd

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


def generate_codebook_md(url, output_file):
    # Read the CSV file from the URL
    response = requests.get(url)
    if response.status_code == 200:
        with open("raw_data/owid-co2-codebook.csv", "wb") as file:
            file.write(response.content)
        logger.info("File downloaded successfully!")
    else:
        logger.error(f"Failed to download file. Status code: {response.status_code}")

    try:
        data = pd.read_csv(url)
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        return
    
    # Validate that required columns exist
    required_columns = ["column", "description", "unit", "source"]
    if not all(col in data.columns for col in required_columns):
        logger.warning(f"Missing required columns. Expected: {required_columns}")
        return

    # Create the Markdown content
    with open(output_file, "w") as md_file:
        md_file.write("# Codebook\n\n")
        md_file.write("This codebook describes the columns, their descriptions, units, and sources.\n\n")

        # Iterate over each row and write its content
        for _, row in data.iterrows():
            md_file.write(f"## {row['column']}\n")
            md_file.write(f"- **Description**: {row['description']}\n")
            md_file.write(f"- **Unit**: {row['unit']}\n")
            md_file.write(f"- **Source**: {row['source']}\n\n")

    logger.info(f"Codebook successfully generated and saved to {output_file}.")