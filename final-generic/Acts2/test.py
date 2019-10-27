import requests
import random


	#k=random.randint(0,199)
	#print(k)
for i in range(50):
	resp = requests.request(method="GET",url= "http://127.0.0.1:5000/api/v1/categories")
	print(resp.status_code)


