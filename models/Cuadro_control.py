import firebase_admin
from firebase_admin import credentials, db
import sys
import os
import json

sys.path.insert(0, os.path.abspath('..'))  # Ajuste para importar otros módulos si necesario

class DatabaseManager:
    def __init__(self):
        self.database_url = 'https://dane-758ea-default-rtdb.firebaseio.com/'
        self.credentials_path = 'Firebase.json'
        self.initialize_connection()

    def get_resource_path(self, relative_path):
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def initialize_connection(self):
        cred_path = self.get_resource_path(self.credentials_path)
        cred = credentials.Certificate(cred_path)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {'databaseURL': self.database_url})
        else:
            self.app = firebase_admin.get_app()
        self.ref = db.reference('cuadro_de_control_de_operaciones_estadisticas')

    def fetch_data_grouped_by_email(self, child_key, threshold):
        try:
            query_ref = self.ref.order_by_child(child_key).start_at(threshold)
            results = query_ref.get()
            email_group = {}
            
            print("Results fetched:", results)  # Depuración: Imprime los resultados obtenidos
            
            if results:
                for key, value in results.items():
                    print("Processing:", key, value)  # Muestra toda la información de cada entrada
                    if value.get(child_key, 0) > threshold:
                        email = value.get('Email', 'default_email@example.com')  # Usa un correo predeterminado si falta
                        project_details = {
                            'project_name': value.get('PROYECTO', 'No Project Name'),
                            'days_late': value.get('Atrasado', 'N/A'),
                            'other_info': value.get('other_info', 'No Additional Info')
                        }
                        print(f"Adding to {email}: {project_details}")  # Detalles del proyecto a agregar
                        if email not in email_group:
                            email_group[email] = []
                        email_group[email].append(project_details)


            print("Email group:", email_group)  # Depuración: Imprime el grupo de email formado
            return email_group
        except Exception as e:
            print(f"Error fetching and grouping data by email: {e}")
            return {}



if __name__ == "__main__":
    db_manager = DatabaseManager()
    grouped_data = db_manager.fetch_data_grouped_by_email('Atrasado', 2)
    print(json.dumps(grouped_data, indent=4))
