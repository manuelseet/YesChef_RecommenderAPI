import pandas as pd
from flask import Flask, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity # Cosine Similarity
from datetime import datetime
from sklearn.metrics import jaccard_score # Cosine Similarity
import atexit

#from APScheduler.scheduler import Scheduler

###Import other py files
from dao import get_database
from service_ml_01 import *
#from service_mlops import *
#from service_db_seeding import *

################# MongoDB settings ##################

db_conn = "mongodb+srv://user:password2022@cluster0.qisep.mongodb.net/mongopractice?retryWrites=true&w=majority"
db_name = "YesChefDB" #"dummy_recipes"
recipe_collection = "RecipeNew"
f_vec_collection = "feature_vector"


################# Flask API ##################
app = Flask(__name__)
#cron = Scheduler(daemon=True) #opne a background thread
#cron.start()

@app.route('/landingSingleRecipeReco', methods=['GET'])
def recommend_single_recipe():
    print("----->", "Reached the API Endpoint")
    dbname = get_database(db_conn, db_name)
    thisUserId = request.args.get('userId', type= str)
    noOfRecommendations = request.args.get('n', type= int)
    (query_recipeID, recommend_list) = obtain_single_recipe_reco(thisUserId, noOfRecommendations, dbname) # must do dependency injection
    response_dict = {"userId": thisUserId, "query_recipeID": query_recipeID, "recommendations": recommend_list}
    return response_dict

@app.route('/landingYouMightLikeReco', methods=['GET'])
def recommend_you_might_like():
    print("----->", "Reached the API Endpoint")
    dbname = get_database(db_conn, db_name)
    thisUserId = request.args.get('userId', type= str)
    noOfRecommendations = request.args.get('n', type= int)
    recommend_list = obtain_you_might_like_reco(thisUserId, noOfRecommendations, dbname) # must do dependency injection
    response_dict = {"userId": thisUserId, "recommendations": recommend_list}
    return response_dict

"""
@cron.interval_schedule(seconds=5)
def schedule_featurization(): 
    #updateFeatureVector()
    print("This test runs every 5 seconds %s" % datetime.now())

# destroy the background thread if web is stopped
atexit.register(lambda: cron.shutdown(wait=False))
"""

# run the server
if __name__ == '__main__':
    app.run(port=5000, debug=True)  
    dbname = get_database(db_conn, db_name)


