import customtkinter
from tkinter import ttk, Toplevel, Scrollbar, HORIZONTAL, VERTICAL, messagebox
from PIL import Image, ImageTk
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
import os
import sys

# Función para obtener la ruta de los recursos, para poder acceder a ellos en el ejecutable
def get_resource_path(relative_path):
    """Obtiene la ruta al recurso empaquetado (o la ruta relativa si no está empaquetado)."""
    try:
        # PyInstaller coloca archivos en una carpeta temporal.
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Función para obtener la página principal del frame
def get_home_frame(parent):
    home_frame = customtkinter.CTkFrame(master=parent, corner_radius=0)
    label = customtkinter.CTkLabel(home_frame, text="Bienvenido a la página home")
    label.pack(pady=20)

    # Contenedor para los botones
    button_frame = customtkinter.CTkFrame(master=home_frame)
    button_frame.pack(fill='x', pady=10)

    # Botón para abrir la ventana de búsqueda
    search_button = customtkinter.CTkButton(button_frame, text="Buscar por Nombre",
                                            command=lambda: open_search_dialog(home_frame, table))
    search_button.pack(side="left", padx=10)

    # Botones Update y Download
    download_button = customtkinter.CTkButton(button_frame, text="Download",
                                              command=lambda: print("Download"))
    download_button.pack(side="right", padx=10)

    # Obtener los datos de Google Sheets
    data = get_data_from_google_sheets()

    # Convertir los datos a un DataFrame de pandas
    global df
    df = pd.DataFrame(data[1:], columns=data[0])

    # Crear el Treeview para la tabla
    table_frame = customtkinter.CTkFrame(master=home_frame)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Crear barras de desplazamiento horizontal y vertical
    scrollbar_x = Scrollbar(table_frame, orient=HORIZONTAL)
    scrollbar_y = Scrollbar(table_frame, orient=VERTICAL)

    # Configurar el Treeview con los encabezados
    headers = df.columns.tolist()
    table = ttk.Treeview(table_frame, columns=headers, show="headings", height=10,
                         xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    # Definir los encabezados dinámicamente desde los datos de Google Sheets
    for col in headers:
        table.heading(col, text=col)
        table.column(col, anchor="center", width=120)

    # Configurar las barras de desplazamiento
    scrollbar_x.config(command=table.xview)
    scrollbar_y.config(command=table.yview)

    # Colocar las barras de desplazamiento en la ventana
    scrollbar_x.pack(side="bottom", fill="x")
    scrollbar_y.pack(side="right", fill="y")

    # Empaquetar el Treeview
    table.pack(expand=True, fill='both')

    # Llenar la tabla con los datos excluyendo la primera fila (encabezados)
    load_data_to_table(table, df)

    return home_frame

def open_search_dialog(parent, table):
    dialog = Toplevel(parent)
    dialog.title("Buscar Persona")
    dialog.geometry("300x200")
    
    name_entry = customtkinter.CTkEntry(dialog, placeholder_text="Ingrese Nombre...")
    name_entry.pack(pady=20, padx=20)
    
    search_btn = customtkinter.CTkButton(dialog, text="Buscar",
                                         command=lambda: filter_table(name_entry.get(), table))
    search_btn.pack(pady=10)

def filter_table(name, table):
    # Eliminar las filas actuales de la tabla antes de filtrar
    for i in table.get_children():
        table.delete(i)

    # Filtrar los datos según la columna de nombre (columna 8, índice 7)
    filtered_data = df[df.iloc[:, 7].str.contains(name, case=False, na=False)]

    # Llenar la tabla con los datos filtrados
    load_data_to_table(table, filtered_data)

def get_data_from_google_sheets():
    # Usar el archivo credentials.json para autenticarte
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Usar get_resource_path para obtener la ruta al archivo Credentials.json
    credentials_path = get_resource_path('./Credentials.json')
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)

    # Abrir la hoja de cálculo por ID
    sheet_id = "159CgHiDNcUK-bTSRLFWhCXhYzpF0zk4Y9yR9U2GxiG0"
    sheet = client.open_by_key(sheet_id).sheet1
    
    # Obtener todos los valores de la hoja
    data = sheet.get_all_values()
    
    # Mostrar los datos en la consola
    print("Datos obtenidos desde Google Sheets:")
    for row in data:
        print(row)
    
    # Devuelve los datos en formato adecuado para el Treeview
    return data

def load_data_to_table(table, df):
    # Limpiar el Treeview antes de insertar nuevos datos
    for item in table.get_children():
        table.delete(item)

    # Cargar los datos en el Treeview
    for index, row in df.iterrows():
        table.insert('', 'end', values=row.tolist())

