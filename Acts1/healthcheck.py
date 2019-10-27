from apscheduler.schedulers.background import BackgroundScheduler
from scale import *
import logging
import requests
logging.basicConfig()
import time
import requests

sched = BackgroundScheduler()
sched1 = BackgroundScheduler()

def health():
    global ki
    for i in ki.keys():
    	try: 
    		req = requests.head("http://localhost:"+str(i)+"/api/v1/_health")
    		print(str(i) + " contaner returned " + str(req.status_code))
    		if(not (req.status_code == 200) ):
    			down(ki[i],i)
    			up(i)
    			ki = OrderedDict(sorted(ki.items())) 
    	except:
    		print("waiting")


def sca():
    global ki
    r = requests.get(url="http://localhost:5000/api/count")
    k = r.json()["val"]
    ki = scale(k)




# seconds can be replaced with minutes, hours, or days
sched.add_job(health, 'interval', seconds = 1)
sched1.add_job(sca, 'interval', seconds=20)
sched.start()
sched1.start()


a = 1
while 1 :
	a = 2
