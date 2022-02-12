import pandas as pd
from bson.objectid import ObjectId

recipe_collection_name = "RecipeNew"
f_vec_collection_name = "feature_vector"
u_act_collection_name = "UserActivity"
sim_mat_collection_name = "similarity_matrix"


def get_database(db_conn, db_name):
    import pymongo
    CONNECTION_STRING = db_conn
    client = pymongo.MongoClient(CONNECTION_STRING)
    return client[db_name]


def get_feature_vector(dbname):
    feature_collection = dbname[f_vec_collection_name]
    cursor = feature_collection.find()
    list_vectors = list(cursor)[0]
    list_vectors.pop('_id')
    return pd.DataFrame.from_dict(list_vectors, orient="index")


def get_this_user_activity(dbname, userEmail):
    user_act_collection = dbname[u_act_collection_name]
    return user_act_collection.find({"userEmail": userEmail})[0]


def get_all_recipes(dbname):
    recipe_collection = dbname[recipe_collection_name]
    return recipe_collection.find()


def get_this_recipe(dbname, recipeId):
    recipe_collection = dbname[recipe_collection_name]
    return recipe_collection.find_one({"_id": ObjectId(recipeId)})


def get_similarity_matrix(dbname):
    sim_mat_collection = dbname[sim_mat_collection_name]
    cursor = sim_mat_collection.find()
    sim_mat = list(cursor)[0]
    sim_mat.pop('_id')
    return sim_mat
