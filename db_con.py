import pymongo
import os

url = os.getenv('API_KEY_MONGODB')

if not url:
    raise ValueError("La URL de MongoDB no está configurada correctamente en las variables de entorno")

client = pymongo.MongoClient(url)
db = client['foodboxconnect']
