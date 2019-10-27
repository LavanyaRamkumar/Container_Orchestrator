import random, os, json, datetime, time ,string
import docker
import random
from flask import *
client = docker.from_env()
import requests
app = Flask(__name__)
c=0
gc = 0

@app.route("/")
def index():
	return ("wrong path")

@app.route("/api/v1/<path:subreddits>", methods=['GET', 'POST', 'DELETE'])
def recv_req(subreddits):
	a = len(client.containers.list()) - 1
	global c
	global gc
	i=c%(a)
	new_url = "http://localhost:"+str(int(8000+i))+"/api/v1/"+subreddits
	print(new_url)
	resp = requests.request(method=request.method,url= new_url,headers={key: value for (key, value) in request.headers if key != 'Host'}, data=request.get_data())
	headers = [(name, value) for (name, value) in resp.raw.headers.items()]
	response = Response(resp.content, resp.status_code, headers)
	c+=1
	gc = gc + 1 
	return (response)

@app.route("/api/count",methods=['GET'])
def count():
	global c
	k = c
	c = 0 	
	return k

@app.route("/api/global",methods=['GET'])
def count1():
	global gc 	
	return gc

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
