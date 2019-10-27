import json
from pymongo import MongoClient


client = MongoClient('mongo', 27017)
db = client['cc_assignment']
act = db['act']
cat = client.cc_assignment.categories
act = client.cc_assignment.act
ords = client.cc_assignment.orgid_counter
with open('orgid_counter.json') as f:
    file_data = json.load(f)

ords.insert(file_data)




client.close()