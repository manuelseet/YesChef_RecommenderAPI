import joblib
import pandas as pd
from flask import Flask, request
from datetime import datetime
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

# Import other py files
from dao import get_database
from service_ml_01 import *
from service_ml_02 import *
from service_ml_tag import *
from service_mlops import *
from service_ml_03 import *
#from service_db_seeding import *

################# MongoDB settings ##################

db_conn = "mongodb+srv://user:password2022@cluster0.qisep.mongodb.net/mongopractice?retryWrites=true&w=majority"
db_name = "YesChefDB"  # "dummy_recipes"

################# Flask API ##################
app = Flask(__name__)

mongoDB = get_database(db_conn, db_name)


@app.route('/landingSingleRecipeReco', methods=['GET'])
def recommend_single_recipe():
    thisUserId = request.args.get('userId', type=str)
    noOfRecommendations = request.args.get('n', type=int)
    (query_recipeID, recommend_list) = obtain_single_recipe_reco(
        thisUserId, noOfRecommendations, mongoDB)  # must do dependency injection
    response_dict = {"userId": thisUserId,
                     "query_recipeID": query_recipeID,
                     "recommendations": recommend_list}
    return response_dict


@app.route('/landingYouMightLikeReco', methods=['GET'])
def recommend_you_might_like():
    thisUserId = request.args.get('userId', type=str)
    noOfRecommendations = request.args.get('n', type=int)
    recommend_list = obtain_you_might_like_reco(
        thisUserId, noOfRecommendations, mongoDB)  # must do dependency injection
    response_dict = {"userId": thisUserId,
                     "recommendations": recommend_list}
    return response_dict


@app.route('/moreLikeThisReco', methods=['GET'])
def recommend_more_like_this():
    recipeId = request.args.get('recipeId', type=str)
    noOfRecommendations = request.args.get('n', type=int)
    recommend_list = obtain_more_like_this_reco(
        recipeId, noOfRecommendations, mongoDB)  # must do dependency injection
    response_dict = {"recommendations": recommend_list}
    return response_dict


@app.route('/predictDifficulty', methods=['GET'])
def predict_recipe_difficulty():
    recipeId = request.args.get('recipeId', type=str)
    prediction = obtain_difficulty_prediction(
        recipeId, mongoDB)
    response_dict = {"prediction": prediction}
    return response_dict

#model 3
model_03 = joblib.load('tfidf_model3')

@app.route("/searchByIngredient", methods = ["GET"])
def recommendation_searchByRecipe():
    req = request.args
    req = req.to_dict()
    ingredients = req['ingredients']
    ingredients_query = [ingredients]

    recipes_corpus_docs = Recipes_Corpus.split("', '")
    recipes_corpus_docs = preprocess_data(recipes_corpus_docs)

    model_03.fit(recipes_corpus_docs)
    tfidf_recipes_docs = model_03.transform(recipes_corpus_docs).toarray()

    features = model_03.get_feature_names_out()
    indexes = [recipes_ingredients.iloc[i, 1] for i in range(len(recipes_ingredients))]
    tfidf_df_recipes = pd.DataFrame(data=tfidf_recipes_docs, index=indexes, columns=features)

    tfidf_query = model_03.transform(ingredients_query).toarray()

    docs_similarity = cosine_similarity(tfidf_query, tfidf_df_recipes)
    query_similarity = docs_similarity[0]

    series = pd.Series(query_similarity, index=tfidf_df_recipes.index)
    sorted_series = series.sort_values(ascending=False)
    sorted_series = sorted_series[sorted_series != 0]
    sorted_id = sorted_series.index

    id = []
    for e in sorted_id:
        id.append(e)
    print(id)
    recommendation_list_json = json.dumps(id)
    print(recommendation_list_json)
    response_dict = {"prediction": recommendation_list_json}

    return response_dict


##~~~~~~ ML Ops Scheduler ~~~~~~##


def schedule_MLOps():
    print("MLOps is starting %s" % datetime.now())
    updateFeatureVector(mongoDB)
    print("MLOps has ended %s" % datetime.now())


def background_housekeeping():
    scheduler.shutdown(wait=True)
    print("Perform housekeeping at shutdown")


scheduler = BackgroundScheduler()

# destroy background thread when api is stopped
atexit.register(lambda: background_housekeeping())


##============= run the server ==============##
if __name__ == '__main__':
    scheduler.add_job(func=schedule_MLOps, trigger="interval", minutes=60)
    # scheduler.add_job(myjob, 'cron', hour=0) #this is to run at every clock hour
    scheduler.start()
    app.run(port=5000, debug=False, use_reloader=False, threaded=True)
