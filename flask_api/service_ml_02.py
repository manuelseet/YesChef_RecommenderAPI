import pandas as pd
import numpy as np
from dao import *
from helper_methods import get_recipes_sortby_jaccard

################# More Like This Recipe Recommendations ##################


def obtain_more_like_this_reco(recipeId, max, dbname):

    # get similarity matrix from Mongo
    sim_mat = get_similarity_matrix(dbname)
    this_recipe_sm = sim_mat[recipeId]
    dtype = [('recipeId', np.unicode_, 24), ('jaccard', float)]
    this_recipe_sm_np = np.array(list(this_recipe_sm.items()), dtype=dtype)
    this_recipe_sm_np = np.sort(this_recipe_sm_np, order='jaccard')
    recommendations = [
        x[0] for x in this_recipe_sm_np[this_recipe_sm_np['jaccard'] < 1][-max:]]
    return recommendations


"""
def obtain_more_like_this_reco(recipeId, max, dbname):

    # 1. GET FEATURE VECTOR
    feature_vectors = get_feature_vector(dbname)

    # 2. GET QUERY RECIPE ID
    query_recipeID = recipeId

    # 3. PREPARE SEARCH CORPUS & QUERY DOC
    query_feature_vector = pd.DataFrame(feature_vectors.loc[query_recipeID]).T
    test_feature_vector = feature_vectors.drop([query_recipeID], axis=0)

    # 4. CALCULATE SIMILARITY SCORES (based on OHE feature vector)
    js_sorted = get_recipes_sortby_jaccard(
        test_feature_vector, query_feature_vector)
    recommendations = js_sorted.index.tolist()[0:max]

    return recommendations
"""
