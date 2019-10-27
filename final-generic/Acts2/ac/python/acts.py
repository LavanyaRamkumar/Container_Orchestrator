import random, os, json, datetime, time ,string
from flask import *
import hashlib
from pymongo import *
import string 
import datetime
import re
import requests
from flask_cors import CORS

healthFlag = 1
actscounter = 0
app = Flask(__name__)
CORS(app)

@app.errorhandler(404)
def page_not_found(e):
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    return "bla",404

@app.route('/')

def index():
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    return ""

@app.route('/upload')
def upload():
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    return render_template('upload.html')

@app.route('/cat')
def cat():
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    return render_template('cat.html')

client = MongoClient('mongo',27017)
# client = MongoClient(port=27017)
db=client.cc_assignment.users
cat = client.cc_assignment.categories
act = client.cc_assignment.act

def getNextSequence(collection,name):
    collection.update_one( { '_id': name },{ '$inc': {'seq': 1}})
    return int(collection.find_one({'_id':name})["seq"])

#api 1
@app.route('/api/v1/users', methods=['POST'])
def process():
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    return("please use port 8080")

#api 2
@app.route('/api/v1/users/<username>', methods=['DELETE'])
def userdelete(username):
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    return ("please use port 8080")

#api 3
@app.route('/api/v1/categories', methods=['GET'])
def categorieAdd():
    print("heyyy\n")
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    global actscounter
    actscounter = actscounter + 1
    j = cat.find()
    print(j)
    d = dict()
    for x in j:
        d[x['catName']]=x['size']
    return jsonify(d)

#api 4
@app.route('/api/v1/categories', methods=['POST'])
def categorieList():
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    global actscounter
    actscounter = actscounter + 1
    j = re.search("[A-Za-z0-9 _]+",(request.get_data().decode('utf-8')))
    if(j is None):
        return jsonify({'code':400})
    j = j.group(0)
    if(cat.count_documents({"catName":j})>0):
        return jsonify({'code':404})
    result=cat.insert_one({'catId': getNextSequence(client.cc_assignment.orgid_counter,"catId"), 'catName':j , 'size' : 0 })
    return jsonify({'code':200})

#api 5
@app.route('/api/v1/categories/<categories>', methods=['DELETE'])
def catdelete(categories):
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    global actscounter
    actscounter = actscounter + 1
    if(cat.count_documents({"catName":categories})>0):
        cat.delete_one({"catName":categories})
        return jsonify({'code':200})
    else:
        return jsonify({'code':404})

#api 6 and 8
@app.route('/api/v1/categories/<categoryName>/acts', methods=['GET'])
def catactsizeprint(categoryName):
    print("hello")
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    global actscounter
    actscounter = actscounter + 1
    start = request.args.get("start")
    end = request.args.get("end")
    if(start is None and end is None):
        if(not cat.count_documents({"catName":categoryName})>0):
            return jsonify({"code": 400})
        d = dict()
        j = cat.find_one({"catName" : categoryName})
        if(j['size'] < 100):
            l = list()
            if(act.count_documents({"catName":categoryName}) == 0):
                return jsonify({'code':404}),204
            v = act.find({"catName" : categoryName},{"_id":0})
            for x in v:
                l.append(x)
            return jsonify(l),200
        else:
            return jsonify({"code":413})
    if(start is None or end is None):
        return jsonify({"code":1400})
    else :
        start = int(start)
        end = int(end)
        if(start > end or (start<0 or end <0)):
            return jsonify({"code":1600})
        else :
            diff = end-start
            k = 1
            ll = list()
            val = act.count_documents({"catName":categoryName})
            if(val < diff or diff >100):
                return jsonify({"code" : 1400})
            if(val == 0):
                return jsonify({'code':1404})
            v = act.find({"catName" : categoryName},{"_id":0}).sort([("actId",-1)])
            for x in v:
                if(k <= diff):
                    ll.append(x)
                k = k + 1
            return jsonify(ll),200      

#api 7
@app.route('/api/v1/categories/<categories>/acts/size', methods=['GET'])
def catactsize(categories):
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    global actscounter
    actscounter = actscounter + 1
    if(not cat.count_documents({"catName":categories})>0):
        return jsonify({"code": 400})
    else:
        j = cat.find({"catName" : categories})
        for x in j:
            if(x['size'] == 0):
                return "empty" , 204
            return jsonify(x['size'])

#api 9
@app.route('/api/v1/acts/upvote', methods=['POST'])
def upvote():
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    global actscounter
    actscounter = actscounter + 1
    j = request.get_json()
    if(not act.count_documents({"actId":j['actId']})>0):
        return jsonify({"code": 400})
    else:
        act.update_one( { 'actId': j['actId'] },{ '$inc': {'upvote': 1}})
        return jsonify({"code": 200})

#api 10
@app.route('/api/v1/acts/<actId>', methods=['DELETE'])
def actDelete(actId):
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    global actscounter
    actscounter = actscounter + 1
    if(not act.count_documents({"actId":int(actId)})>0):
        return jsonify({"code": 400})
    else:
        j = act.find({"actId":int(actId)},{"_id":0})
        for i in j:
            l=(i["catName"])
        print(l)
        cat.update_one({ 'catName':l },{ '$inc': {'size': -1}})
        act.delete_one({"actId":int(actId)})
        return jsonify({'code':200})
        

def validateDateTime(date_text):
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    global actscounter
    actscounter = actscounter + 1
    try:
        datetime.datetime.strptime(date_text, '%d-%m-%Y:%S-%M-%H')
        return True
    except ValueError:
        return False
def validateBase64(data_text):
    data_text = data_text.split(",")[1]
    if(re.search("[A-Za-z0-9+/=]", data_text) and len(data_text)%4==0):
        return True
    else:
        return False
#api 11
@app.route('/api/v1/acts', methods=['POST'])
def actUpload():
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    global actscounter
    actscounter = actscounter + 1
    userdata = requests.get("http://34.201.221.121/api/v1/users")
    user=userdata.json()
    j = request.get_json()
    #to validate unique ID
    if(act.count_documents({"actId":j['actId']})>0):
        return jsonify({"code":405})
    #to validate timestamp
    if not validateDateTime(j['timestamp']):
        return jsonify({"code":406})
    #to validate user exists
    if(not j['username'] in user):
    # if(not db.count_documents({"name":j['username']})>0):
        return jsonify({"code":407})
    #to validate Base64 code 
    if(not validateBase64(j['imgB64'])):
        return jsonify({"code":408})
    #to validate upvote
    if("upvote" in j):
        return jsonify({"code":409})
    #to validate that cat exists
    if(not cat.count_documents({"catName":j['categoryName']})>0):
        return jsonify({"code":410})

    result=act.insert_one({'actId':j['actId'] , 'username': j['username'], 'timestamp' : j['timestamp'], 'caption':j['caption'], 'catName':j['categoryName'], 'img':j['imgB64'], 'upvote':0 })
    cat.update_one({ 'catName':j['categoryName'] },{ '$inc': {'size': 1}})
    client.cc_assignment.orgid_counter.update_one( {'_id':"actId"},{'$inc': {'seq': 1}})
    return jsonify({'code':200})

@app.route('/api/v1/_count', methods=['GET'])
def countusers():
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    global actscounter
    k = list()
    k.append(actscounter)
    if(actscounter <= 0):
        return "empty",204
    return(jsonify(k))


@app.route('/api/v1/_count', methods=['DELETE'])
def deletecount():
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    global actscounter
    actscounter = 0
    return(jsonify({}))

@app.route('/api/v1/acts/count', methods=['GET'])
def countacts():
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    global actscounter
    actscounter = actscounter + 1
    val = 0
    j = cat.find()
    for x in j:
        val = val + x['size']
    if(val == 0):
        return "empty",204
    return jsonify(val)



@app.route('/api/v1/_health', methods=['GET'])
def health():
    print("health")
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    j = cat.find()
    d = dict()
    for x in j:
        d[x['catName']]=x['size']
    return "",200   

@app.route('/api/v1/_crash', methods=['POST'])
def crash():
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    healthFlag = 0
    return "" ,200

# helper api's
# get act id
@app.route('/actId')
def actid():
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    f = client.cc_assignment.orgid_counter.find_one({"_id":"actId"})
    return jsonify(f['seq'])
#down vote
@app.route('/api/v1/acts/downvote', methods=['POST'])
def downvote():
    global healthFlag
    if healthFlag == 0 :
        return "" ,500
    j = request.get_json()
    if(not act.count_documents({"actId":j['actId']})>0):
        return jsonify({"code": 400})
    else:
        act.update_one( { 'actId': j['actId'] },{ '$inc': {'upvote': -1}})
        return jsonify({"code": 200})


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
