import pymongo

url = 'API_KEY_MONGODB'

client = pymongo.MongoClient(url)
db = client['foodboxconnect']