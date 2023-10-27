import logging
import datetime
import json
import requests
import google.oauth2.id_token
from google.auth.transport import requests as grequests
from google.cloud import datastore
from flask import Flask, render_template, request, jsonify, redirect
import pymongo


app = Flask(__name__)

datastore_client = datastore.Client()
firebase_request_adapter = grequests.Request()

# setting up mongoDB to connect to my personal mongoDB compass
mongoClient = pymongo.MongoClient("mongodb+srv://sachin2517:2517.Ylo@cluster0.mvn0mxf.mongodb.net/?retryWrites=true&w=majority") 
mongoDB = mongoClient['Request']


# allocates a time when the data was inserted into the db
# all the functions above routes are being called by create, update and delete post at line 119
def store_time(email, dt): 
    entity = datastore.Entity(key=datastore_client.key('User', email, 'visit')) 
    entity.update({ 
        'timestamp': dt 
    }) 
    datastore_client.put(entity)

def fetch_times(email, limit): 
    ancestor = datastore_client.key('User', email) 
    query = datastore_client.query(kind='visit', ancestor=ancestor) 
    query.order = ['-timestamp'] 
    times = query.fetch(limit=limit) 
    return times 

# allows user to post data into the db
def store_post_mongodb(name, email, gamename): 
    collection = mongoDB['requests'] 
    json_data = {"name": name, "email": email, "gamename": gamename} 
    collection.insert_one(json_data) 

# allows user to update game requests
def store_update_mongodb(email, gamename): 
    collection = mongoDB['requests']
    collection.update_one({"email": email},{"$set":{"gamename": gamename}})

# allows deletation of a game request
def store_delete_mongodb(name, email, gamename): 
    collection = mongoDB['requests'] 
    json_data = {"name": name, "email": email, "gamename": gamename} 
    collection.delete_one(json_data)

# Routes
@app.route('/') 
@app.route('/home') 
def home(): 
    return render_template('home.html')

@app.route('/update') 
def update(): 
    return render_template('update.html')

@app.route('/delete') 
def delete(): 
    return render_template('delete.html')
      

@app.route('/add') 
def myreq(): 
    id_token = request.cookies.get("token") 
    error_message = None
    claims = None

    if id_token: 
        try: 
            # Verify the token against the Firebase Auth API
            claims = google.oauth2.id_token.verify_firebase_token( 
            id_token, firebase_request_adapter) 
        except ValueError as exc: 
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)

    return render_template('about.html', user_data=claims, error_message=error_message) 

# this displays the games available in the game store
@app.route('/games') 
def about(): 
    url = "https://europe-west2-sachin-online-game-store.cloudfunctions.net/GoogleStorage_Display"
    uResponse = requests.get(url)
    jResponse = uResponse.text 
    data = json.loads(jResponse)
    return render_template('Games.html', data=data)

# This handles the registration with firebase, which allows access to the games data from the google data store
# if the token stored in the cookie isn't successful then this feature won't work for the unauthorised user
@app.route('/register') 
def form():
    firebase_id_token = request.cookies.get("token") 
    
    error_message = None
    claims = None
    data = None
    
    url = "https://europe-west2-sachin-online-game-store.cloudfunctions.net/DisplayGames"
    uResponse = requests.get(url)
    jResponse = uResponse.text 
    data = json.loads(jResponse)
    
    if firebase_id_token: 
        try: 
            claims = google.oauth2.id_token.verify_firebase_token(firebase_id_token, firebase_request_adapter) 
            store_time(claims['email'], datetime.datetime.now()) 
        except ValueError as exc: 
            error_message = str(exc)  
            
    return render_template('register.html', user_data=claims, error_message=error_message, data=data) 

# These functions are used to manipulate the data in mongodb
# This is to add a game request
@app.route('/createpost', methods=['POST']) 
def createpost(): 
    name = request.form['name'] 
    email = request.form['email'] 
    gamename = request.form['gamename']

    if email and gamename: 
        store_post_mongodb(name, email, gamename) 
    return jsonify({'message': "Post submitted!"})

# This is to update the game request
@app.route('/updatepost', methods=['PUT']) 
def updatePost(): 
    email = request.form['email']  
    gamename = request.form['gamename']

    if email and gamename: 
        store_update_mongodb(email, gamename) 
    return jsonify({'message': "Post Updated!"})

# This is to delete the game request
@app.route('/deletepost', methods=['DELETE']) 
def deletePost(): 
    name = request.form['name'] 
    email = request.form['email'] 
    gamename = request.form['gamename'] 

    if name and email and gamename: 
        store_delete_mongodb(name, email, gamename) 
    return jsonify({'message': "Post Deleted!"})



@app.errorhandler(500) 
def server_error(e): 
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.') 
    return 'An internal error occurred.', 500

@app.errorhandler(404) 
def page_not_found(error): 
    return render_template('404.html'), 404


if __name__ == '__main__': 
    # Only run for local development.
    app.run(host='127.0.0.1', port=8080, debug=True)