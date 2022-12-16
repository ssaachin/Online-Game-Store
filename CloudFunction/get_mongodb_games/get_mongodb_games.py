from pymongo import MongoClient 
from bson.json_util import dumps 
from flask import Blueprint, request, jsonify 
import os 
import requests 
import json 
# end imports

# Cloud function to get a forum posts from mongo
def get_mongodb_games(request): 

 client = MongoClient("mongodb+srv://sachin2517:2517.Ylo@cluster0.mvn0mxf.mongodb.net/?retryWrites=true&w=majority") 
 
 # connect to the db
 db = client.Request 
 myCursor = None



 myCursor = db.requests.find() 
 list_cur = list(myCursor)

 json_data = dumps(list_cur) 


 return json_data
