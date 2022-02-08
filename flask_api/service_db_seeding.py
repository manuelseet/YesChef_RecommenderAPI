import requests
import json

querystring_list = [
    {"from":"0","size":"20", "tags": "american"},
    {"from":"0","size":"20", "tags": "korean"},
    {"from":"0","size":"20", "tags": "british"},
    {"from":"0","size":"20", "tags": "thai"},
    {"from":"0","size":"20", "tags": "indian"},
    {"from":"0","size":"20", "tags": "taiwanese"},
    {"from":"0","size":"20","tags":"japanese"},
    {"from":"0","size":"20","tags":"vietnamese"},
    {"from":"0","size":"20","tags":"chinese"}
]

querystring = querystring_list[0]

url = "https://tasty.p.rapidapi.com/recipes/list"
headers = {
    'x-rapidapi-host': "tasty.p.rapidapi.com",
    'x-rapidapi-key': "91082ada61msh47b4a99007a25f8p17b117jsnc919172a977e"
    }
response = requests.request("GET", url, headers=headers, params=querystring)

y = json.loads(response.text)

recipe_list = []

#get all recipes, whether embedded or not
for recipe in y["results"]:
    if "recipes" in recipe:
        #print(recipe["name"])
        for subrecipe in recipe["recipes"]:
            #print("---", subrecipe["name"])
            recipe_list.append(subrecipe)
    else:
        recipe_list.append(recipe)

ALL_RECIPE_DOCS = []
prelim_ALL_RECIPES = []

recipe_counter = 0
for recipe in recipe_list:
    recipe_counter += 1
    print(recipe_counter, ". ", recipe["name"])

    ##########Name, Description, ImageURL#############
    name = recipe["name"]

    imageURL = [recipe["thumbnail_url"]]
    if "beauty_url" in recipe:
        if recipe["beauty_url"] != None:
            imageURL.append(recipe["beauty_url"])

    description = ''
    if "description" in recipe:
        if recipe["description"] != None:
            description = recipe["description"]

    time = 0
    if recipe["total_time_minutes"] != None:
        time = recipe["total_time_minutes"]


    noOfServings = recipe["num_servings"]


    ###########Prep Steps##############################
    instructions = recipe["instructions"]
    prepSteps = []
    for step in instructions:
        prepSteps.append(step["display_text"])

    #########Ingredients####################
    raw_ing_comp = []
    ing_comp_sec = []
    if len(recipe["sections"]) > 1:
        ing_count = 0
        for sec in recipe["sections"]: 
            ing_count = ing_count + len(sec["components"])
            for comp in sec["components"]:
                raw_ing_comp.append(comp)
    elif len(recipe["sections"]) == 1:
        ing_count = len(recipe["sections"][0]["components"])
        sec = recipe["sections"][0]
        for comp in sec["components"]:
                raw_ing_comp.append(comp)

    prelim_ingredient_list = []
    #print("---------->", len(raw_ing_comp))
    for ing_comp in raw_ing_comp:
        ing_dict = {"ingredient": None, "amount": None, "unit": None, "comment": None }
        ing_obj = ing_comp["ingredient"]

        ##Get the measurements
        measurement_obj = ing_comp["measurements"]
        if len(measurement_obj) == 1:
            ing_dict["amount"] = measurement_obj[0]["quantity"]
            ing_dict["unit"] = measurement_obj[0]["unit"]["abbreviation"]
        else:
            for i in range(len(measurement_obj)):
                if measurement_obj[i]["unit"]["system"] == "metric":
                    ing_dict["amount"] = measurement_obj[i]["quantity"]
                    ing_dict["unit"] = measurement_obj[i]["unit"]["abbreviation"]
        
        #get the 

        if ing_dict["unit"] == "":
            if ing_dict["amount"] != "1" or ing_dict["amount"] != "½": 
                ing_dict["ingredient"] = ing_obj["display_plural"]
            else: 
                ing_dict["ingredient"] = ing_obj["display_singular"]
        else: 
            ing_dict["ingredient"] = ing_obj["display_singular"]

        ing_dict["comment"] = ing_comp["extra_comment"]

        prelim_ingredient_list.append(ing_dict)


    ing_name_set = []
    final_ingredient_list = []
    for ing in prelim_ingredient_list:
        if ing["ingredient"] not in ing_name_set:
            final_ingredient_list.append(ing)
            ing_name_set.append(ing["ingredient"])


    #########Nutrition####################
    nutrition_list = []
    if recipe["nutrition"]:
        d = recipe["nutrition"]
        fiber_count = 1
        for key, value in d.items():
            if key != "updated_at":
                nut_dict = {}
                nut_dict["content"] = key
                nut_dict["quantity"] = value
                nut_dict["unit"] = "g"
                if key == "calories":
                    nut_dict["unit"] = "kcal"
                    calories = value
                if key == "fiber":
                    fiber_count += 1
            if key != "fiber" or (key == "fiber" and fiber_count != 2):
                nutrition_list.append(nut_dict)
        

    #########Tags####################
    cuisineType = []
    techniques = []
    tags = []
    difficulty = []

    tags_list = recipe["tags"]
    for tag in tags_list:
        if tag["type"] == "cuisine":
            cuisineType.append(tag["display_name"])
            continue

        if tag["type"] == "difficulty":
            difficulty.append(tag["display_name"])
            continue
        
        if tag["type"] == "meal":
            courseType = tag["display_name"]
            continue

        if tag["type"] == "method":
            techniques.append(tag["display_name"])

        if tag["type"] == "dietary":
            tags.append(tag["display_name"])

            
    ########### CREATE RECIPE DOC ##############################
    recipe_doc = {
        "name": name,
        "description": description,
        "imageURL": imageURL,

        "cuisineType": cuisineType,
        "courseType": courseType,
        "difficulty": difficulty,
        "tags": tags,
        "technique": techniques,

        "prepTime": time,
        "noOfServings": noOfServings,
        "calories": calories,

        "ingredients": final_ingredient_list,
        "prepSteps": prepSteps,

        "nutrition": nutrition_list,

        "source": "Tasty.co",

    }
    prelim_ALL_RECIPES.append(recipe_doc)

all_recipe_set = []
ALL_RECIPE_DOCS = []
for recipe in prelim_ALL_RECIPES:
    if recipe["name"] not in all_recipe_set:
        ALL_RECIPE_DOCS.append(recipe)
        all_recipe_set.append(recipe["name"])

print(len(ALL_RECIPE_DOCS))


#########################################
####### GET DATABASE ##############
#########################################

def get_database():
    from pymongo import MongoClient
    import pymongo
    CONNECTION_STRING = "mongodb+srv://user:password2022@cluster0.qisep.mongodb.net/mongopractice?retryWrites=true&w=majority"
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)
    return client["YesChefDB"]
    
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    # Get the database
    dbname = get_database()

#Insert into Database
collection_name = dbname["RecipeNew"]
collection_name.insert_many(ALL_RECIPE_DOCS)


#########################################
#######IN CASE OF RESEEDING ##############
#########################################
#collection_name.delete_many({})