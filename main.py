import logging 
import pymongo
import json


from flask import Flask, render_template,request 
from pymongo import MongoClient
from bson.json_util import dumps 

app = Flask(__name__)

cluster=MongoClient( "mongodb+srv://sachin2517:2517.Ylo@cluster0.mvn0mxf.mongodb.net/?retryWrites=true&w=majority") 
db=cluster["test"] 
collection=db["test"] 


def get_mongodb_items(): 
    # Search data from Mongodb

    myCursor = None
    # create queries
    # title_query = {"Unit title": {"$eq": "IoT Unit"}} 
    # author_query = {"Unit leader": {"$eq": "Xin"}} 
    # dateCreated_query = {"dateCreated": {"$eq": 2021}}
    # demo_thing = {"thumbnail": {"$eq": "some url"}}  

    myCursor = collection.find() 
    # {"$and": [demo_thing]}
    list_cur = list(myCursor) 
    print(list_cur) 
    json_data = dumps(list_cur) 
    return json_data 




@app.route('/') 
@app.route('/home') 
def home(): 
    jResponse=get_mongodb_items() 

    data=json.loads(jResponse) 
    return render_template('home.html', data=data) 



@app.route('/games') 
def about(): 
    return render_template('about.html')

@app.route('/register') 
def form(): 
    return render_template('register.html') 
# [END form] 

# [START submitted]
@app.route('/submitted', methods=['POST']) 
def submitted_form(): 
    name = request.form['name'] 
    email = request.form['email'] 
    site = request.form['site_url'] 
    comments = request.form['comments'] 

    # [END submitted]
    # [START render_template]
    return render_template( 
        'submitted_form.html', 
        name=name, 
        email=email, 
        site=site, 
        comments=comments) 
    # [END render_template]

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