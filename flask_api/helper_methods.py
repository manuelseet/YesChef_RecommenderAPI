import pandas as pd
import numpy as np
from sklearn.metrics import jaccard_score


def get_recipes_sortby_jaccard(test_feature_vector, query_feature_vector):
    jaccard_similarity = []
    for row in range(test_feature_vector.shape[0]):
        js = jaccard_score(
            query_feature_vector.iloc[0, :], test_feature_vector.iloc[row, :], average='binary')
        jaccard_similarity.append(js)

    jaccard_similarity = np.array([jaccard_similarity])

    js = pd.DataFrame(data=jaccard_similarity,
                      index=['jaccard'],
                      columns=[x for x in test_feature_vector.index]).T

    return js.sort_values(by=['jaccard'], ascending=False)
