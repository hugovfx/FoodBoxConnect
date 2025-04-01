import pymongo
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la URL de MongoDB desde las variables de entorno
url = os.getenv('MONGODB_URI')

if not url:
    raise ValueError("La URL de MongoDB no está configurada correctamente en las variables de entorno")

# Conectar a la base de datos de MongoDB
client = pymongo.MongoClient(url)

# Especificar la base de datos que deseas usar
db = client['foodboxconnect']
