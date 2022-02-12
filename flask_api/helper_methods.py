import pandas as pd
import numpy as np
from sklearn.metrics import jaccard_score

import custom_word_lists as cwl
import pandas as pd
from pattern.text.en import singularize
import string


def my_ingredient_parser(ingredient_name, NER, isDebugging):

    ing_brand_removed = ingredient_name[ingredient_name.find(
        '®')+1:]  # remove brand names

    # singularize words and split them
    ing_subwords = singularize(ing_brand_removed).split()

    prepped_ing = " ".join(str(item) for item in ing_subwords)
    prepped_ing = prepped_ing.translate(str.maketrans(
        '', '', string.punctuation))  # remove punctuation

    if isDebugging == True:
        print(prepped_ing)

    ing_essence = []
    NERdoc = NER(prepped_ing)
    for token in NERdoc:
        if isDebugging == True:
            print(token.text, token.pos_)

        if token.pos_ == "NOUN" or token.pos_ == "PROPN" or token.text in cwl.include_word_list:
            if token.text not in cwl.barred_noun_list and token.text not in cwl.color_list:
                ing_essence.append(token.text)

    parsed_ing = " ".join(str(item) for item in ing_essence)
    for ing_cat in cwl.ing_categories:
        if ing_cat in parsed_ing:
            parsed_ing = ing_cat
            break

    return parsed_ing


def calculateBOW(wordset, l_doc):
    tf_diz = dict.fromkeys(wordset, 0)
    for word in l_doc:
        tf_diz[word] = 1  # l_doc.count(word)
    return tf_diz


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


def get_recipe_jaccard_scores(test_feature_vector, query_feature_vector, query_recipeID):
    jaccard_similarity = []
    for row in range(test_feature_vector.shape[0]):
        js = jaccard_score(
            query_feature_vector.iloc[0, :], test_feature_vector.iloc[row, :], average='binary')
        jaccard_similarity.append(js)

    jaccard_similarity = np.array([jaccard_similarity])

    js0 = pd.DataFrame(data=jaccard_similarity, index=[query_recipeID],
                       columns=[x for x in test_feature_vector.index])

    return js0
