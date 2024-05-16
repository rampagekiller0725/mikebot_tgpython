import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client['mikeplaybot']
col = db['users']

def insert_one(data):
    col.insert_one(data)

def users():
    return [x['name'] for x in col.find({}, {"name": 1})]

def find_one(username):
    return col.find_one({"name": username})