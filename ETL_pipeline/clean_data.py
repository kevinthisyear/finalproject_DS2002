import pandas as pd
import numpy as np
import sys
from logger_setup import setup_logger

logger = setup_logger()

def clean_data(file_path, year_start, year_end):
    # Load the data
    data = pd.read_csv(file_path)

    # Inspect the Data
    logger.info("Initial Data Overview:")
    logger.info(data.info())

    # Standardize Column Names
    # Convert column names to lowercase and replace spaces with underscores
    data.columns = data.columns.str.lower().str.replace(' ', '_')

    # Handle Missing Values
    # Identify missing values
    missing_summary = data.isnull().sum()
    logger.info("\nMissing Values Summary:")
    logger.info(missing_summary)

    # Handle missing numerical values (exclude `gdp` and `consumption_co2`)
    numerical_cols = data.select_dtypes(include=[np.number]).columns
    excluded_cols = ['gdp', 'consumption_co2']
    numerical_cols_to_fill = [col for col in numerical_cols if col not in excluded_cols]
    for col in numerical_cols_to_fill:
        data[col] = data[col].fillna(data[col].median())

    # Handle missing categorical values
    categorical_cols = data.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        data[col] = data[col].fillna("Unknown")

    # Remove Duplicates
    initial_rows = data.shape[0]
    data.drop_duplicates(inplace=True)
    logger.info(f"\nDuplicates Removed: {initial_rows - data.shape[0]} rows")

    # Standardize Units (Example for emissions)
    # Skip transformations for `gdp` and `consumption_co2`
    if 'emissions' in data.columns:
        data['emissions'] = data['emissions'] / 1000  # Assuming input is in kg

    # Validate Data Ranges
    # Example: Check year range and replace out-of-range values
    if 'year' in data.columns:
        data = data[(data['year'] >= year_start) & (data['year'] <= year_end)]

    if 'emissions' in data.columns:
        data = data[data['emissions'] >= 0]

    # Ensure `gdp` and `consumption_co2` are untouched
    if 'gdp' in data.columns and 'consumption_co2' in data.columns:
        data = data.dropna(subset=['gdp', 'consumption_co2'])

    # Enrich Data (Optional)
    if 'population' in data.columns and 'emissions' in data.columns:
        data['emissions_per_capita'] = data['emissions'] / data['population']

    # Save Cleaned Data
    output_file = "data/cleaned_emissions_data.csv"
    data.to_csv(output_file, index=False)
    logger.info(f"\nCleaned data saved to {output_file}")

    logger.info("\nCleaned Data Overview:")
    logger.info(data.info())

    total_null_values = data.isnull().sum().sum()
    print(f"Total null values in the DataFrame: {total_null_values}")
    total_empty_values = (data == "").sum().sum()
    print(f"Total empty strings in the DataFrame: {total_empty_values}")

    # Ensure the 'country' column exists
    if 'country' not in data.columns:
        logger.error("The dataset does not contain a 'country' column. Quitting program...")
        sys.exit()

    # Inspect unique values in the 'country' column
    unique_countries = data['country'].unique()
    logger.info("\nUnique values in the 'country' column:")
    logger.info(unique_countries)

    # 2. Define functions for category identification (unchanged)
    # Normalize names for comparison (lowercase, stripped spaces)
    ISO_COUNTRIES = [c.lower().strip() for c in ISO_COUNTRIES]
    CONTINENTS = [c.lower().strip() for c in CONTINENTS]
    NATIONS = [c.lower().strip() for c in NATIONS]
    SOCIOECONOMIC = [c.lower().strip() for c in SOCIOECONOMIC]

    def is_valid_country(name):
        return name.lower().strip() in ISO_COUNTRIES

    def is_continent(name):
        return name.lower().strip() in CONTINENTS

    def is_nations(name):
        return name.lower().strip() in NATIONS

    def is_socioeconomic(name):
        return name.lower().strip() in SOCIOECONOMIC

    def not_in_category(name):
        if pd.isna(name):
            return True
        return (
            name.lower().strip() not in ISO_COUNTRIES
            and name.lower().strip() not in CONTINENTS
            and name.lower().strip() not in NATIONS
            and name.lower().strip() not in SOCIOECONOMIC
        )

    # Separate rows based on whether they are valid countries
    country_rows = data[data['country'].apply(is_valid_country)]
    continent_rows = data[data['country'].apply(is_continent)]
    nations_rows = data[data['country'].apply(is_nations)]
    socioeconomic_rows = data[data['country'].apply(is_socioeconomic)]
    remaining_rows = data[data['country'].apply(not_in_category)]

    # Save the separated datasets
    country_file = "data/country_data.csv"
    continent_file = "data/continent_data.csv"
    nations_file = "data/nations_data.csv"
    socioeconomic_file = "data/socioeconomic_data.csv"
    non_country_file = "data/non_country_data.csv"

    country_rows.to_csv(country_file, index=False)
    continent_rows.to_csv(continent_file, index=False)
    nations_rows.to_csv(nations_file, index=False)
    socioeconomic_rows.to_csv(socioeconomic_file, index=False)

    logger.info("\nSummary:")
    logger.info(f"Valid country rows: {country_rows.shape[0]}")