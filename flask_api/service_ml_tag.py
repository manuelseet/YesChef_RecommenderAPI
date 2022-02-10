import pandas as pd
from dao import *
import math
import joblib


############### CALCULATING FUNCTIONS #######################
def count_words_in_steps(prepSteps):
    all_step_words = []
    for step in prepSteps:
        word_list = step.split()
        for word in word_list:
            all_step_words.append(word)
    return len(all_step_words)

############### Predict difficulty #######################


def obtain_difficulty_prediction(recipeId, dbname):
    this_recipe_obj = get_this_recipe(dbname, recipeId)

    print("this recipe--------->", this_recipe_obj["name"])

    ##prepare independent variables  ######
    ing_count = len(this_recipe_obj["ingredients"])

    prep_time = this_recipe_obj["prepTime"]
    log_prep_time = math.log10(prep_time)

    prep_steps = this_recipe_obj["prepSteps"]
    prep_word_count = count_words_in_steps(prep_steps)

    print("Ingredient Count:", ing_count, prep_word_count, log_prep_time)

    ##get our model and predict  ######
    gboost_model = joblib.load("difficulty_gboost_model")
    y_pred = gboost_model.predict(
        [[ing_count, log_prep_time, prep_word_count]])

    difficulty_list = ["Easy", "Medium", "Advanced"]
    difficulty_word = difficulty_list[y_pred[0]]
    print("Model prediction is: ", difficulty_word)

    ##return predictions in array  ######
    prediction = [difficulty_word]
    return prediction
