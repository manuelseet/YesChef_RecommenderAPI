def get_database(db_conn, db_name):
    import pymongo
    CONNECTION_STRING = db_conn
    client = pymongo.MongoClient(CONNECTION_STRING)
    return client[db_name]