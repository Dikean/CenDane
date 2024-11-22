import firebase_admin
from firebase_admin import credentials, db
import sys
import os

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Lugar donde necesitas cargar Firebase.json
firebase_config_path = get_resource_path("Firebase.json")
cred = credentials.Certificate(firebase_config_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dane-758ea-default-rtdb.firebaseio.com/'  # Asegúrate de que esta URL sea correcta
})

# Referencia a la base de datos
ref = db.reference('cuadro_de_control_de_operaciones_estadisticas')  # Cambia 'usuarios' por el nombre del nodo que quieras usar
