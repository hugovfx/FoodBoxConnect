import pymongo

url = 'mongodb+srv://hugobaeza:ykh55NBxdaFzFhgc@cluster0.mp0jt.mongodb.net/'

client = pymongo.MongoClient(url)
db = client['foodboxconnect']