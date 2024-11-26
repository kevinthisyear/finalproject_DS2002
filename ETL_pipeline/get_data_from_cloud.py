from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd

def get_dataframe_from_cloud(client, db_name, collection_name):
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print.error(e)
    
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