from logger_setup import setup_logger
import pandas as pd

logger = setup_logger()

def store_data_to_cloud(client, filepath, db_name, collection_name):
    # confirm a successful connection
    try:
        client.admin.command('ping')
        logger.info("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        logger.error(e)
    
    df = pd.read_csv(filepath)
    data = df.to_dict(orient="records")
    db = client[db_name]
    collection = db[collection_name]

    # insert data into MongoDB collection
    result = collection.insert_many(data)
    logger.info(f"Inserted {len(result.inserted_ids)} documents into {collection_name} collection!")
    