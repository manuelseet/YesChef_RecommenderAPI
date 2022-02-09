import pandas as pd
import numpy as np
from sklearn.metrics import jaccard_score  # Cosine Similarity

recipe_collection_name = "RecipeNew"
f_vec_collection_name = "feature_vector"
u_act_collection_name = "UserActivity"

################# Landing Single Recipe Recommendations ##################


def obtain_single_recipe_reco(userEmail, max, dbname):

    # 1. GET USER BOOKMARKS
    user_act_collection = dbname[u_act_collection_name]
    this_user_act = user_act_collection.find({"userEmail": userEmail})[0]
    # print(this_user_act)
    # get List of bookmark objects
    this_user_bookmark_list = this_user_act["bookmarks"]

    # 2. GET FEATURE VECTOR
    feature_collection = dbname[f_vec_collection_name]
    cursor = feature_collection.find()
    list_vectors = list(cursor)[0]
    list_vectors.pop('_id')
    feature_vectors = pd.DataFrame.from_dict(list_vectors, orient="index")

    # 3. GET QUERY RECIPE ID
    # for now, get the latest
    query_recipeID = this_user_bookmark_list[-1]["recipeId"]

    # TEMPORARY OVERRIDE UNTIL BOOKMARK UPDATE TO NEW DB
    query_recipeID = feature_vectors.index[-1]

    # 4. PREPARE CORPUS
    query_vector = pd.DataFrame(feature_vectors.loc[query_recipeID])
    query_feature_vector = query_vector.T
    test_feature_vector = feature_vectors.drop([query_recipeID], axis=0)

    # 5. CALCULATE SIMILARITY SCORES (based on OHE feature vector)
    #similarity1 = cosine_similarity(query_feature_vector, test_feature_vector)

    jaccard_similarity = []
    for row in range(test_feature_vector.shape[0]):
        js = jaccard_score(
            query_feature_vector.iloc[0, :], test_feature_vector.iloc[row, :], average='binary')
        jaccard_similarity.append(js)

    jaccard_similarity = np.array([jaccard_similarity])

    cs = pd.DataFrame(data=jaccard_similarity,
                      index=['cosine'],
                      columns=[x for x in test_feature_vector.index]).T

    cs_sorted = cs.sort_values(by=['cosine'], ascending=False)
    recommendations = cs_sorted.index.tolist()[0:max]

    print(query_recipeID)
    return (query_recipeID, recommendations)


################# Landing You Might Like Recommendations ##################


def obtain_you_might_like_reco(userEmail, max, dbname):

    # 1. GET USER BOOKMARKS
    user_act_collection = dbname[u_act_collection_name]
    this_user_act = user_act_collection.find({"userEmail": userEmail})[0]
    # print(this_user_act)
    # get List of bookmark objects
    this_user_bookmark_list = this_user_act["bookmarks"]

    # 2. GET FEATURE VECTOR
    feature_collection = dbname[f_vec_collection_name]
    cursor = feature_collection.find()
    list_vectors = list(cursor)[0]
    list_vectors.pop('_id')
    feature_vectors = pd.DataFrame.from_dict(list_vectors, orient="index")

    # 3. GET QUERY RECIPE ID
    # for now, get the latest
    query_recipeID = this_user_bookmark_list[-1]["recipeId"]

    # TEMPORARY OVERRIDE UNTIL BOOKMARK UPDATE TO NEW DB
    query_recipeID = feature_vectors.index[-2]

    # 4. PREPARE CORPUS
    query_vector = pd.DataFrame(feature_vectors.loc[query_recipeID])
    query_feature_vector = query_vector.T
    test_feature_vector = feature_vectors.drop([query_recipeID], axis=0)

    # 5. CALCULATE SIMILARITY SCORES (based on OHE feature vector)
    #similarity1 = cosine_similarity(query_feature_vector, test_feature_vector)

    jaccard_similarity = []
    for row in range(test_feature_vector.shape[0]):
        js = jaccard_score(
            query_feature_vector.iloc[0, :], test_feature_vector.iloc[row, :], average='binary')
        jaccard_similarity.append(js)

    jaccard_similarity = np.array([jaccard_similarity])

    cs = pd.DataFrame(data=jaccard_similarity,
                      index=['cosine'],
                      columns=[x for x in test_feature_vector.index]).T

    cs_sorted = cs.sort_values(by=['cosine'], ascending=False)
    recommendations = cs_sorted.index.tolist()[0:max]

    return recommendations
