import logging 
import pymongo
import json
import datetime



import datetime 
from flask import Flask, render_template, request, jsonify,redirect 
import json
import requests 
from google.auth.transport import requests as grequests 
from google.cloud import datastore 
import google.oauth2.id_token 
import pymongo 

firebase_request_adapter = grequests.Request()



datastore_client = datastore.Client() 

app = Flask(__name__)




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


mongoClient = pymongo.MongoClient("mongodb+srv://sachin2517:2517.Ylo@cluster0.mvn0mxf.mongodb.net/?retryWrites=true&w=majority") 
mongoDB = mongoClient['Request']


# def get_mongodb_items(): 
    # Search data from Mongodb

    # myCursor = None
    # create queries
    # title_query = {"Unit title": {"$eq": "IoT Unit"}} 
    # author_query = {"Unit leader": {"$eq": "Xin"}} 
    # dateCreated_query = {"dateCreated": {"$eq": 2021}}
    # demo_thing = {"thumbnail": {"$eq": "some url"}}  

    # myCursor = collection.find() 
    # {"$and": [demo_thing]}
    # list_cur = list(myCursor) 
    # print(list_cur) 
    # json_data = dumps(list_cur) 
    # return json_data 

def store_post_mongodb(name, email, gamename): 
    collection = mongoDB['requests'] 
    json_data = {"name": name, "email": email, "gamename": gamename} 

    collection.insert_one(json_data) 


def store_update_mongodb(email, gamename): 
    collection = mongoDB['requests'] 
    # email will not be added, as author parameter will be used to identify individual users posts
    # json_data = 

    collection.update_one({"email": email},{"$set":{"gamename": gamename}})

def store_delete_mongodb(name, email, gamename): 
    collection = mongoDB['requests'] 
    # email will not be added, as author parameter will be used to identify individual users posts
    json_data = {"name": name, "email": email, "gamename": gamename} 

    collection.delete_one(json_data)


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
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load. For improved performance,
            # some applications may wish to cache results in an encrypted
            # session store (see for instance
            # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token( 
            id_token, firebase_request_adapter) 


        except ValueError as exc: 
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)

    return render_template( 
        'about.html', 
        user_data=claims, error_message=error_message) 

@app.route('/games') 
def about(): 
    url = "https://europe-west2-sachin-online-game-store.cloudfunctions.net/GoogleStorage_Display"

    uResponse = requests.get(url)

    jResponse = uResponse.text 
    data = json.loads(jResponse)
    return render_template('Games.html', data=data)

@app.route('/register') 
def form():
    id_token = request.cookies.get("token") 
    error_message = None
    claims = None
    data = None
    
    url = "https://europe-west2-sachin-online-game-store.cloudfunctions.net/DisplayGames"

    uResponse = requests.get(url)

    jResponse = uResponse.text 
    data = json.loads(jResponse)

    if id_token: 
        try: 
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load. For improved performance,
            # some applications may wish to cache results in an encrypted
            # session store (see for instance
            # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token( 
                id_token, firebase_request_adapter) 

            store_time(claims['email'], datetime.datetime.now()) 
            # times = fetch_times(claims['email'], 3) 

            
            

        except ValueError as exc: 
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc) 

 # Record and fetch the recent times a logged-in user has accessed
 # the site. This is currently shared amongst all users, but will be
 # individualized in a following step. 
            

    return render_template(
        'register.html',
        user_data=claims, error_message=error_message, data=data) 
# [END form] 


@app.route('/createpost', methods=['POST']) 
def createpost(): 
    name = request.form['name'] 
    email = request.form['email'] 
    gamename = request.form['gamename']

    if email and gamename: 
        store_post_mongodb(name, email, gamename) 
    return jsonify({'message': "Post submitted!"})

@app.route('/updatepost', methods=['PUT']) 
def updatePost(): 
    email = request.form['email']  
    gamename = request.form['gamename']

    if email and gamename: 
        store_update_mongodb(email, gamename) 
    return jsonify({'message': "Post Updated!"})

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