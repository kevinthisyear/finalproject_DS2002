import pandas as pd

def get_dataframe_from_cloud(client, db_name, collection_name):
    # confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print.error(e)
    
    db = client[db_name]
    collection = db[collection_name]

    # retrieve data from MongoDB collection and convert to pandas df
    df = pd.DataFrame(list(collection.find()))
    df.drop(columns=['_id'], inplace=True)

    return df