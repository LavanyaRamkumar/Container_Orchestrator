import os,json
import docker
import subprocess
client = docker.from_env()
with open('data.json') as json_file:  
	d = json.load(json_file)
print(client.images.remove("run:latest"))	
print(client.images.list())
print(client.images.pull(d["image"]))
bashCommand = "sudo docker tag "+d["image"]+" run:latest"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
print(client.images.list())
