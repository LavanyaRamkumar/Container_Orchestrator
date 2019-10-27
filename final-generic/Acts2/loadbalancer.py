import random, os, json, datetime, time ,string
import docker
import random
import json
from flask import *
client = docker.from_env()
import requests
app = Flask(__name__)
c=0
gc = 0



@app.route("/<path:subreddits>", methods=['GET', 'POST', 'DELETE'])
def recv_req(subreddits):
	a = len(client.containers.list()) - 1
	global c
	global gc
	c+=1
	gc = gc + 1 
	j=gc%(a)
	print("Request",gc)
	print(a,"containers running")
	pos = -1
	new_url = request.url
	#print(new_url)
	col = new_url.rfind(':')
	#print(col)
	for i in range(col,len(new_url)-1):
		if(new_url[i].isdigit() and new_url[i+1]=="/"):
			pos = i+1
			break
	#print(pos)
	ur = new_url[:col+1]+str(int(8000+j))+new_url[pos:]
	print("Request sent to:",ur)
	print("\n")
	print("\n")
	new_url = ur
	resp = requests.request(method=request.method,url= new_url,headers={key: value for (key, value) in request.headers if key != 'Host'}, data=request.get_data())
	headers = [(name, value) for (name, value) in resp.raw.headers.items()]
	response = Response(resp.content, resp.status_code, headers)
		
	return (response)

@app.route("/api/count",methods=['GET'])
def count():
	global c
	k = c
	c = 0 	
	return jsonify({"val":k})

@app.route("/api/global",methods=['GET'])
def count1():
	global gc 	
	return gc

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(debug=True, host='0.0.0.0', port=port)
