import numpy as np
from dao import *

################# Landing Single Recipe Recommendations ##################


def obtain_single_recipe_reco(userEmail, max, dbname):
    this_user_act = get_this_user_activity(dbname, userEmail)
    this_user_bookmark_list = this_user_act["bookmarks"]
    #this_user_review_list = this_user_act["reviews"]

    query_recipeID = this_user_bookmark_list[-1]["recipeId"]

    this_recipe_sm = get_similarity_matrix(dbname)[query_recipeID]
    this_recipe_sm_np = np.array(list(this_recipe_sm.items()), dtype=[
                                 ('recipeId', np.unicode_, 24), ('jaccard', float)])
    this_recipe_sm_np = np.sort(this_recipe_sm_np, order='jaccard')
    recommendations = [
        x[0] for x in this_recipe_sm_np[this_recipe_sm_np['jaccard'] < 1][-max:]]

    print(query_recipeID)
    return (query_recipeID, recommendations)


################# Landing You Might Like Recommendations ##################


def obtain_you_might_like_reco(userEmail, max, dbname):
    this_user_act = get_this_user_activity(dbname, userEmail)
    this_user_bookmark_list = this_user_act["bookmarks"]
    #this_user_review_list = this_user_act["reviews"]

    query_recipeID = this_user_bookmark_list[-2]["recipeId"]

    this_recipe_sm = get_similarity_matrix(dbname)[query_recipeID]
    dtype = [('recipeId', np.unicode_, 24), ('jaccard', float)]
    this_recipe_sm_np = np.array(list(this_recipe_sm.items()), dtype=dtype)
    this_recipe_sm_np = np.sort(this_recipe_sm_np, order='jaccard')
    recommendations = [
        x[0] for x in this_recipe_sm_np[this_recipe_sm_np['jaccard'] < 1][-max:]]

    return recommendations


"""


def obtain_single_recipe_reco(userEmail, max, dbname):

    # 1. GET USER BOOKMARKS
    this_user_act = get_this_user_activity(dbname, userEmail)
    this_user_bookmark_list = this_user_act["bookmarks"]
    #this_user_review_list = this_user_act["reviews"]

    # 2. GET FEATURE VECTOR
    feature_vectors = get_feature_vector(dbname)

    # 3. GET QUERY RECIPE ID
    query_recipeID = this_user_bookmark_list[-1]["recipeId"]
    # TEMPORARY OVERRIDE UNTIL BOOKMARK UPDATE TO NEW DB
    query_recipeID = feature_vectors.index[-1]

    # 4. PREPARE CORPUS
    query_feature_vector = pd.DataFrame(feature_vectors.loc[query_recipeID]).T
    test_feature_vector = feature_vectors.drop([query_recipeID], axis=0)

    # 5. CALCULATE SIMILARITY SCORES (based on OHE feature vector)
    js_sorted = get_recipes_sortby_jaccard(
        test_feature_vector, query_feature_vector)
    recommendations = js_sorted.index.tolist()[0:max]

    print(query_recipeID)
    return (query_recipeID, recommendations)


def obtain_you_might_like_reco(userEmail, max, dbname):

    # 1. GET USER BOOKMARKS
    this_user_act = get_this_user_activity(dbname, userEmail)
    this_user_bookmark_list = this_user_act["bookmarks"]
    #this_user_review_list = this_user_act["reviews"]

    # 2. GET FEATURE VECTOR
    feature_vectors = get_feature_vector(dbname)

    # 3. GET QUERY RECIPE ID
    # for now, get the latest
    query_recipeID = this_user_bookmark_list[-1]["recipeId"]
    # TEMPORARY OVERRIDE UNTIL BOOKMARK UPDATE TO NEW DB
    query_recipeID = feature_vectors.index[-2]

    # 4. PREPARE CORPUS
    query_feature_vector = pd.DataFrame(feature_vectors.loc[query_recipeID]).T
    test_feature_vector = feature_vectors.drop([query_recipeID], axis=0)

    # 5. CALCULATE SIMILARITY SCORES (based on OHE feature vector)
    js_sorted = get_recipes_sortby_jaccard(
        test_feature_vector, query_feature_vector)
    recommendations = js_sorted.index.tolist()[0:max]

    return recommendations
"""
