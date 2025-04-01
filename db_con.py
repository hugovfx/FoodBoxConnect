import pymongo
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la URL de MongoDB desde las variables de entorno
url = os.getenv('MONGODB_URI')

# Manejo de errores mejorado
if not url:
    # Valor de desarrollo por defecto (solo para desarrollo local)
    if os.getenv('DEBUG', 'False') == 'True':
        url = "mongodb://localhost:27017/"
        print("ADVERTENCIA: Usando conexión MongoDB local para desarrollo")
    else:
        raise ValueError("La URL de MongoDB no está configurada correctamente en las variables de entorno")

try:
    # Conectar a la base de datos de MongoDB con manejo de errores y timeout
    client = pymongo.MongoClient(url, serverSelectionTimeoutMS=5000)
    
    # Verificar conexión
    client.server_info()
    
    # Especificar la base de datos
    db = client['foodboxconnect']
    
    print("Conexión a MongoDB establecida correctamente")
    
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(f"Error al conectar a MongoDB: {err}")
    raise