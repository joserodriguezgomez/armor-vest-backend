from pymongo import MongoClient
import os

def obtener_uri_mongo():
    """
    Obtiene la URI de MongoDB desde una variable de entorno y valida su existencia.
    """
    mongo_uri = os.environ.get("MONGO_URI")
    if not mongo_uri:
        raise EnvironmentError("La variable de entorno 'MONGO_URI' no está definida.")
    return mongo_uri

def conectar_a_mongodb(uri):
    """
    Establece la conexión con la base de datos MongoDB usando la URI proporcionada.
    """
    try:
        client = MongoClient(uri)
        db = client["armor_vest"]
        print("Conexión a la base de datos configurada correctamente.")
        return db
    except Exception as e:
        print(f"Error al conectar con MongoDB: {e}")
        raise

# Uso de las funciones
try:
    uri = obtener_uri_mongo()
    db = conectar_a_mongodb(uri)
    # Aquí puedes seguir con la lógica de manipulación de la base de datos
except EnvironmentError as e:
    print(e)
except Exception as e:
    print(f"Error no manejado: {e}")
