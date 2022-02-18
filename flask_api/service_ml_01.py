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
