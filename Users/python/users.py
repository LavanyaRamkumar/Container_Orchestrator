import random, os, json, datetime, time ,string
from flask import *
import hashlib
from pymongo import *
import string 
import datetime
import re
from flask_cors import CORS

usercounter = 0

app = Flask(__name__)
CORS(app)


@app.errorhandler(404)
def page_not_found(e):
    return "bla",404

@app.route('/')

def index():
    return render_template('form.html')

client = MongoClient('mongo',27017)
#client = MongoClient(port=27017)
db=client.cc_assignment.users
cat = client.cc_assignment.categories
act = client.cc_assignment.act

def getNextSequence(collection,name):
    collection.update_one( { '_id': name },{ '$inc': {'seq': 1}})
    return int(collection.find_one({'_id':name})["seq"])

#api 1
@app.route('/api/v1/users', methods=['POST'])
def process():
    global usercounter 
    usercounter = usercounter + 1
    j = request.get_json()
    name = j['name']
    password = j['password']
    if( len(password) != 40 or not all(c in string.hexdigits for c in password) ):
        return jsonify({'code' : 600})

    if name and password and password != "da39a3ee5e6b4b0d3255bfef95601890afd80709":
        if(db.count_documents({"name":name})>0):
            return jsonify({'code' : 405})

        result=db.insert_one({'userId': getNextSequence(client.cc_assignment.orgid_counter,"userId"), 'name': name, 'password' : password })
        return jsonify({'code' : 201})
    return jsonify({'code' : 400})

#api 2
@app.route('/api/v1/users/<username>', methods=['DELETE'])
def userdelete(username):
    global usercounter 
    usercounter = usercounter + 1
    if(db.count_documents({"name":username})>0):
        db.delete_one({"name":username})
        return jsonify({'code':200})
    else:
        abort(404)
        return jsonify({'code':404})

#get list of users
@app.route('/api/v1/users', methods=['GET'])
def users():
    global usercounter 
    usercounter = usercounter + 1
    j = db.find()
    l = list()
    for x in j:
        l.append(x['name'])
    return jsonify(l)

#get list of users
@app.route('/api/v1/userlist', methods=['GET'])
def listuser():
    global usercounter 
    usercounter = usercounter + 1
    j = db.find()
    d = dict()
    for x in j:
        d[x['name']]=x['userId']
    return jsonify(d)

@app.route('/api/v1/_count', methods=['GET'])
def countusers():
    global usercounter
    l = list()
    l.append(usercounter)
    if(usercounter <= 0):
        return "empty",204
    return(jsonify(l))

@app.route('/api/v1/_count', methods=['DELETE'])
def deletecount():
    global usercounter
    usercounter = 0
    return(jsonify({}))

#login
@app.route('/api/v1/users/login', methods=['POST'])
def processes():
    global usercounter 
    usercounter = usercounter + 1
    j = request.get_json()
    name = j['name']
    password = j['password']
    if( len(password) != 40 or not all(c in string.hexdigits for c in password) ):
        return jsonify({'code' : 600 ,"text" :"Sha1 error"}),200

    if name and password and password != "da39a3ee5e6b4b0d3255bfef95601890afd80709":
        if(db.count_documents({"name":name})<=0):
            return jsonify({'code' : 405 ,"text" :"login fail"}),400

        v = db.find_one({'name': name},{"_id":0})
        return jsonify({'code' : 201,"text" :"Successfull login","userId":v["userId"]}),201
    return jsonify({'code' : 400,"text" :"data missing"}),400


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)