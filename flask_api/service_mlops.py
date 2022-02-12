from dao import *

import pandas as pd
import spacy

from helper_methods import *


############### FEATURE ENGINEERING #######################
def updateFeatureVector(dbname):
    print("#################> entering feature vector method##############")

    #=========== PREPARE DATA ===========
    feature_vectors = get_feature_vector(dbname)
    all_recipeIDs = [str(x["_id"]) for x in get_all_recipes(dbname)]

    if all_recipeIDs == list(feature_vectors.index):
        print("MongoDB Feature Vector is Updated. No Need for MLOps now")
        print("#################> exiting feature vector method##############")
    else:
        #=========== GET INGREDIENT VOCAB ===========
        recipe_list = get_all_recipes(dbname)
        ingredient_vocab = []
        for recipe in recipe_list:
            if "ingredients" in recipe:
                ingredient_list = recipe["ingredients"]
                for ing in ingredient_list:
                    if "ingredient" in ing:
                        ing_name = ing["ingredient"]
                        if ing_name != None:
                            ingredient_vocab.append(ing_name.lower())
        ingredient_vocab = list(set(ingredient_vocab))
        
        #===========. ENGINEERING FEATURE VOCAB ===========
        NER_engine = spacy.load("en_core_web_sm")
        
        parsed_ingredient_vocab = []
        for ing in ingredient_vocab: 
            ing_parsed = my_ingredient_parser(ing, NER_engine, False)
            parsed_ingredient_vocab.append(ing_parsed)

        parsed_ingredient_vocab = list(set(parsed_ingredient_vocab))
        print(len(parsed_ingredient_vocab))
        parsed_ingredient_vocab.insert(0, "recipeID")
        print("-------->finished parsing method ", parsed_ingredient_vocab[:10])

        

        #=========== FEATURE VECTORIZATION ===========
        allBOWs = []
        recipe_list = get_all_recipes(dbname)
        for recipe in recipe_list:
            recipe_ing = []
            if "ingredients" in recipe:
                ingredient_list = recipe["ingredients"]
                for ing in ingredient_list:
                    if "ingredient" in ing:
                        ing_name = ing["ingredient"]
                        if ing_name != None:
                            ing_name = ing_name.lower()
                            ing_parsed = my_ingredient_parser(ing_name, NER_engine, False)
                            if ing_parsed in parsed_ingredient_vocab:
                                recipe_ing.append(ing_parsed)
            bow0 = calculateBOW(parsed_ingredient_vocab,recipe_ing)
            recipeID = str(recipe["_id"])
            bow0["recipeID"] = recipeID
            allBOWs.append(bow0)

        #=========== PERSIST FEATURE VECTORS to MongoDB (as backup)===========
        df_bow = pd.DataFrame(allBOWs)
        df_bow.set_index("recipeID", inplace = True)
        df_bow_new = df_bow.drop([""], axis = 1)

        df_bow_dict = df_bow_new.to_dict('index')
        f_vec_collection = "feature_vector"
        feature_collection_mongo = dbname[f_vec_collection]
        feature_collection_mongo.delete_many({})
        feature_collection_mongo.insert_one(df_bow_dict)

        #=========== Calculate SIMILARITY MATRIX ===========
        feature_vectors = df_bow_new
        query_recipeID = feature_vectors.index[0]
        query_feature_vector = pd.DataFrame(feature_vectors.loc[query_recipeID]).T
        test_feature_vector = feature_vectors

        sim_matrix = get_recipe_jaccard_scores(test_feature_vector, query_feature_vector, query_recipeID)

        for i in range(1,test_feature_vector.shape[0]):
            query_recipeID = feature_vectors.index[i]
            query_feature_vector = pd.DataFrame(feature_vectors.loc[query_recipeID]).T
            js1 = get_recipe_jaccard_scores(test_feature_vector, query_feature_vector, query_recipeID)
            sim_matrix = pd.concat([sim_matrix, js1])


        #=========== persist SIMILARITY MATRIX to MongoDB ===========
        sim_matrix_dict = sim_matrix.to_dict('index')
        sim_mat_collection_name = "similarity_matrix"
        sim_mat_collection = dbname[sim_mat_collection_name]
        sim_mat_collection.delete_many({})
        sim_mat_collection.insert_one(sim_matrix_dict)


        #=========== PRINT TO EXCEL ===========  
        sim_matrix.to_excel("similarity_matrix.xlsx")
    