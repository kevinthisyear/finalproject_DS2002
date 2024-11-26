from logger_setup import setup_logger
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd

logger = setup_logger()

def store_data_to_cloud(client, filepath, db_name, collection_name):
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        logger.info("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        logger.error(e)
    
    df = pd.read_csv(filepath)

    data = df.to_dict(orient="records")
    db = client[db_name]
    collection = db[collection_name]

    # Insert data into MongoDB collection
    result = collection.insert_many(data)    
    
    logger.info(f"Inserted {len(result.inserted_ids)} documents into {collection_name} collection!")

def get_dataframe_from_cloud(uri, db_name, collection_name):
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        logger.info("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        logger.error(e)
    
    db = client[db_name]
    collection = db[collection_name]

    # Retrieve data from MongoDB collection
    cursor = collection.find()
    # Convert the cursor to a list of dictionaries (MongoDB documents)
    data = list(cursor)
    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(data)

    df.drop(columns=['_id'], inplace=True)

    return df
