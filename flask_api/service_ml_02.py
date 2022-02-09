import pandas as pd
import numpy as np
from sklearn.metrics import jaccard_score  # Cosine Similarity

recipe_collection_name = "RecipeNew"
f_vec_collection_name = "feature_vector"
u_act_collection_name = "UserActivity"

################# More Like This Recipe Recommendations ##################


def obtain_more_like_this_reco(recipeId, max, dbname):

    # 1. GET FEATURE VECTOR
    feature_collection = dbname[f_vec_collection_name]
    cursor = feature_collection.find()
    list_vectors = list(cursor)[0]
    list_vectors.pop('_id')
    feature_vectors = pd.DataFrame.from_dict(list_vectors, orient="index")

    # 2. GET QUERY RECIPE ID
    query_recipeID = recipeId

    # 3. PREPARE CORPUS
    query_vector = pd.DataFrame(feature_vectors.loc[query_recipeID])
    query_feature_vector = query_vector.T
    test_feature_vector = feature_vectors.drop([query_recipeID], axis=0)

    # 4. CALCULATE SIMILARITY SCORES (based on OHE feature vector)

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
