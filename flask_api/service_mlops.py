from dao import get_database
import custom_word_lists as cwl

import pandas as pd
import spacy
from spacy import displacy
from pattern.text.en import singularize
import string
import custom_word_lists as cwl

db_conn = "mongodb+srv://user:password2022@cluster0.qisep.mongodb.net/mongopractice?retryWrites=true&w=majority"
db_name = "YesChefDB" #"dummy_recipes"
recipe_collection_name = "RecipeNew"
f_vec_collection_name = "feature_vector"

if __name__ == "__main__":    
    dbname = get_database(db_conn, db_name)
    recipe_collection = dbname[recipe_collection_name]
    feature_collection = dbname[f_vec_collection_name]


cursor = recipe_collection.find()
list_cur = list(cursor)
df = pd.DataFrame(list_cur)


def my_ingredient_parser(ingredient_name, NER, isDebugging):

    ing_brand_removed = ingredient_name[ingredient_name.find('®')+1:] #remove brand names

    ing_subwords = singularize(ing_brand_removed).split() #singularize words and split them
    
    prepped_ing = " ".join(str(item) for item in ing_subwords)
    prepped_ing = prepped_ing.translate(str.maketrans('', '', string.punctuation)) #remove punctuation

    if isDebugging == True:
        print(prepped_ing)

    ing_essence = []
    NERdoc = NER(prepped_ing)
    for token in NERdoc:
        if isDebugging == True:
            print(token.text,token.pos_)

        if token.pos_ == "NOUN" or token.pos_ == "PROPN" or token.text in cwl.include_word_list:
            if token.text not in cwl.barred_noun_list and token.text not in cwl.color_list:
                ing_essence.append(token.text)

    parsed_ing = " ".join(str(item) for item in ing_essence)
    for ing_cat in cwl.ing_categories:
        if ing_cat in parsed_ing:
            parsed_ing = ing_cat
            break
    
    return parsed_ing

ingredient_vocab = []
recipe_list = recipe_collection.find()
for recipe in recipe_list:
    if "ingredients" in recipe:
        ingredient_list = recipe["ingredients"]
        for ing in ingredient_list:
            if "ingredient" in ing:
                ing_name = ing["ingredient"]
                if ing_name != None:
                    ingredient_vocab.append(ing_name.lower())
ingredient_vocab = list(set(ingredient_vocab))

NER_engine = spacy.load("en_core_web_sm")

parsed_ingredient_vocab = []
for ing in ingredient_vocab: 
    ing_parsed = my_ingredient_parser(ing, NER_engine, False)
    parsed_ingredient_vocab.append(ing_parsed)

parsed_ingredient_vocab = list(set(parsed_ingredient_vocab))
print(len(parsed_ingredient_vocab))
parsed_ingredient_vocab.insert(0, "recipeID")


def calculateBOW(wordset,l_doc):
  tf_diz = dict.fromkeys(wordset,0)
  for word in l_doc:
      tf_diz[word]=1 #l_doc.count(word)
  return tf_diz

allBOWs = []
recipe_list = recipe_collection.find()
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


df_bow = pd.DataFrame(allBOWs)
df_bow.set_index("recipeID", inplace = True)
df_bow_new = df_bow.drop([""], axis = 1)

df_bow_dict = df_bow.to_dict('index')
f_vec_collection = "feature_vector"
feature_collection = dbname[f_vec_collection]
feature_collection.delete_many({})
feature_collection.insert_one(df_bow_dict)


countRecipes = df_bow_new.sum()
countRecipes.to_excel("feature_count.xlsx")