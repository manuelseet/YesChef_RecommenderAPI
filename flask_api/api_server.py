import pandas as pd
from flask import Flask, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity  # Cosine Similarity
from datetime import datetime
from sklearn.metrics import jaccard_score  # Cosine Similarity
import atexit


import custom_word_lists as cwl
import pandas as pd
import spacy
from spacy import displacy
from pattern.text.en import singularize
import string


from apscheduler.schedulers.background import BackgroundScheduler

# Import other py files
from dao import get_database
from service_ml_01 import *
from service_ml_02 import *
from service_mlops import *
#from service_db_seeding import *

################# MongoDB settings ##################

db_conn = "mongodb+srv://user:password2022@cluster0.qisep.mongodb.net/mongopractice?retryWrites=true&w=majority"
db_name = "YesChefDB"  # "dummy_recipes"
recipe_collection = "RecipeNew"
f_vec_collection = "feature_vector"


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
                     "query_recipeID": query_recipeID, "recommendations": recommend_list}
    return response_dict


@app.route('/landingYouMightLikeReco', methods=['GET'])
def recommend_you_might_like():
    thisUserId = request.args.get('userId', type=str)
    noOfRecommendations = request.args.get('n', type=int)
    recommend_list = obtain_you_might_like_reco(
        thisUserId, noOfRecommendations, mongoDB)  # must do dependency injection
    response_dict = {"userId": thisUserId, "recommendations": recommend_list}
    return response_dict


@app.route('/moreLikeThisReco', methods=['GET'])
def recommend_more_like_this():
    recipeId = request.args.get('recipeId', type=str)
    noOfRecommendations = request.args.get('n', type=int)
    recommend_list = obtain_more_like_this_reco(
        recipeId, noOfRecommendations, mongoDB)  # must do dependency injection
    response_dict = {"recommendations": recommend_list}
    return response_dict

##~~~~~~ ML Ops Scheduler ~~~~~~##


def schedule_MLOps():
    print("MLOps is starting %s" % datetime.now())
    updateFeatureVector(mongoDB)
    print("MLOps has ended %s" % datetime.now())


def background_housekeeping():
    scheduler.shutdown(wait=True)
    print("housekeeping at shutdown")


scheduler = BackgroundScheduler()

# destroy background thread when api is stopped
atexit.register(lambda: background_housekeeping())


##============= run the server ==============##
if __name__ == '__main__':
    scheduler.add_job(func=schedule_MLOps, trigger="interval", minutes=60)
    # scheduler.add_job(myjob, 'cron', hour=0) #this is to run at every clock hour
    scheduler.start()
    app.run(port=5000, debug=True, use_reloader=False)
