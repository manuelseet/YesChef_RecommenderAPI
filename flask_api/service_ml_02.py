import pandas as pd
import numpy as np
from dao import *

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
