import docker
import random
from collections import OrderedDict
client = docker.from_env()
portVal = 8000
p = 8000
m = ""

ki = dict() #{8000:docker_id}
for i in client.containers.list():
	l = client.containers.get(i.id).name
	if(not(l == "acts_mongo_1")):
		ki[p] = client.containers.get(i.id).short_id
		p = p + 1
ki = OrderedDict(ki)
print(ki)

def runs(num):
	global portVal
	global ki
	c = len(ki)
	if(c < num):
		while(c < num):
			portVal = portVal + 1
			up(portVal)
			c = c + 1
	if(c > num):
		ki = OrderedDict(sorted(ki.items()))
		while(c > num):
			down(ki[ki.keys()[-1]], (ki.keys()[-1]))
			portVal = portVal - 1
			c = c -1 

def up(portVals):
	global ki
	s1=client.containers.run('acts_acts', ports = {'5000/tcp':portVals}, privileged=False, detach=True, network="acts_default")
	ki[portVals] = s1.short_id
	print(str(portVals) + " added")

def down(ids,p):
	global ki
	k = client.containers.get(ids)
	k.kill()
	del ki[p]
	print(str(p) + " killed")


def killAll():
	for i in client.containers.list() :
		k = client.containers.get(i.id)
		if(not (k.name == "acts_acts_1") and not (k.name == "acts_mongo_1")):
			k.kill()

			
def scale(val):
	global ki
	global portVal
	print("\n"+ "scaling " + str(val))
	c=len(ki)
	if(val < 20):
		if(c > 1):
			ki = OrderedDict(sorted(ki.items()))
			while(c > 1):
				down(ki[ki.keys()[-1]], (ki.keys()[-1]))
				portVal = portVal - 1
				c = c -1
	
	if(val >= 20 and val < 40 ):
		runs(2)

	if(val >= 40 and val < 60 ):
		runs(3)

	if(val >= 60 and val < 80 ):
		runs(4)

	if(val >= 80 and val < 100 ):
		runs(5)

	if(val >= 100 and val < 120 ):
		runs(6)

	if(val >= 120 and val < 140 ):
		runs(7)

	if(val >= 140 and val < 160 ):
		runs(8)

	if(val >= 160 and val < 180 ):
		runs(9)

	if(val >= 180 and val < 200 ):
		runs(10)
	if(val >= 200):
		run(int(math.floor(val/20))+1)
	print("# of containers " + str(len(ki)) + "\n")
	print(ki)
	return(ki) 


killAll()


#for i in range(10):
#	k = random.randint(0,199)
 #	scale(k)
	#print(ki)

