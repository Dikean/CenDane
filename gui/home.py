import customtkinter
from tkinter import ttk, Toplevel, Scrollbar, HORIZONTAL, VERTICAL, messagebox
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
import os
import requests
import re
import threading
from PIL import Image, ImageTk
import sys


# Función para limpiar nombres de archivos y carpetas
def limpiar_nombre(nombre):
    return re.sub(r"[^\w\s-]", "", nombre).replace(" ", "_")

# Función para obtener la ruta de los recursos, para poder acceder a ellos en el ejecutable
def get_resource_path(relative_path):
    """Obtiene la ruta al recurso empaquetado (o la ruta relativa si no está empaquetado)."""
    try:
        # PyInstaller coloca archivos en una carpeta temporal.
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def get_home_frame(parent):

    home_frame = customtkinter.CTkFrame(master=parent, corner_radius=0)
    label = customtkinter.CTkLabel(home_frame, text="Descarga de Documentos", font=("Arial", 24))
    label.pack(pady=20)

    # Contenedor para los botones
    button_frame = customtkinter.CTkFrame(master=home_frame)
    button_frame.pack(fill='x', pady=10)

    # Botón para abrir la ventana de búsqueda
    search_button = customtkinter.CTkButton(button_frame, text="Buscar por Cédula",
                                            command=lambda: open_search_dialog(home_frame, table))
    search_button.pack(side="left", padx=10)

    # Botones Update y Download
    download_button = customtkinter.CTkButton(button_frame, text="Descargar",
                                              command=lambda: handle_selected_downloads(table, df))
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
    
    name_entry = customtkinter.CTkEntry(dialog, placeholder_text="Ingrese Nombre o Cédula...")
    name_entry.pack(pady=20, padx=20)
    
    search_btn = customtkinter.CTkButton(dialog, text="Buscar",
                                         command=lambda: filter_table(name_entry.get(), table))
    search_btn.pack(pady=10)

def get_data_from_google_sheets():
    # Usar el archivo credentials.json para autenticarte
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    credentials_path = get_resource_path('./Credentials.json')
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    
    # Abrir la hoja de cálculo por ID
    sheet_id = "16pCE_88pfw1ASf8oB_epNgQrlwbU04ZYwcBQiFd49Hw"
    sheet = client.open_by_key(sheet_id).sheet1
    
    # Obtener todos los valores de la hoja
    data = sheet.get_all_values()
    
    # Mostrar los datos en la consola
    # print("Datos obtenidos desde Google Sheets:")
    # for row in data:
    #  print(row)
    
    # Devuelve los datos en formato adecuado para el Treeview
    return data

def filter_table(input_value, table):
    # Limpiar la tabla antes de insertar nuevos datos
    for i in table.get_children():
        table.delete(i)
    
    # Limpiar espacios en blanco en los encabezados y valores del DataFrame
    global df
    df.columns = df.columns.str.strip()  # Eliminar espacios en los encabezados de las columnas
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)  # Eliminar espacios de los valores de tipo string

    # Imprimir los nombres de las columnas para depuración
    print("Columnas disponibles en el DataFrame:")
    for col in df.columns:
        print(f"'{col}'")
    
    # Determinar si el input es un número o un texto (cédula o nombre)
    if input_value.isdigit():
        # Buscar por cédula (en la columna correspondiente)
        column_name = '4. Ingrese su número de documento de identidad'
        if column_name in df.columns:
            filtered_data = df[df[column_name].astype(str).str.contains(input_value, case=False, na=False)]
        else:
            messagebox.showerror("Error", f"La columna '{column_name}' no existe en los datos.")
            return
    else:
        # Buscar por nombre (en la columna correspondiente)
        column_name = '1. Ingrese su nombre completo (Sin apellidos)'
        if column_name in df.columns:
            filtered_data = df[df[column_name].str.contains(input_value, case=False, na=False)]
        else:
            messagebox.showerror("Error", f"La columna '{column_name}' no existe en los datos.")
            return

    # Si no hay resultados después del filtro, mostrar un mensaje
    if filtered_data.empty:
        messagebox.showinfo("Sin resultados", "No se encontraron resultados para la búsqueda.")
    else:
        # Cargar los datos filtrados en la tabla
        load_data_to_table(table, filtered_data)


def load_data_to_table(table, df):
    # Limpiar el Treeview antes de insertar nuevos datos
    for item in table.get_children():
        table.delete(item)

    # Cargar los datos en el Treeview
    for index, row in df.iterrows():
        table.insert('', 'end', values=row.tolist())

def handle_selected_downloads(table, df):
    selected_item = table.selection()
    
    if selected_item:
        # Obtener los valores de la fila seleccionada
        row_values = table.item(selected_item, 'values')

        # Crear una ventana emergente de carga
        loading_window = Toplevel()
        loading_window.title("Descargando...")
        loading_label = customtkinter.CTkLabel(loading_window, text="Descargando documentos, por favor espere...")
        loading_label.pack(padx=20, pady=20)
        loading_window.geometry("300x100")
        loading_window.resizable(False, False)

        # Centrar la ventana de carga
        loading_window.update_idletasks()
        width = loading_window.winfo_width()
        height = loading_window.winfo_height()
        x = (loading_window.winfo_screenwidth() // 2) - (width // 2)
        y = (loading_window.winfo_screenheight() // 2) - (height // 2)
        loading_window.geometry(f"{width}x{height}+{x}+{y}")

        # Hacer que la descarga se realice en un hilo separado
        threading.Thread(target=download_documents_for_selected_row, args=(row_values, df, loading_window)).start()
    else:
        messagebox.showwarning("Selección Inválida", "Por favor, seleccione una fila.")


def download_documents_for_selected_row(row_values, df, loading_window):
    try:
        # Crear la carpeta principal en la carpeta de Documentos con cédula y nombre
        cedula = row_values[9]
        nombre = row_values[6]  # Supongamos que el nombre está en la columna 1

        for index, row_values in df.iterrows():
            cedula = row_values[9]  # Suponiendo que la cédula está en la columna 10 (índice 10)
            nombre = row_values[6]   # Suponiendo que el nombre está en la columna 7 (índice 7)
            
            # Mostrar los valores de la fila
            print(f"Fila {index}: Cédula: {cedula}, Nombre: {nombre}")

        # Intentar guardar en la carpeta "Documentos"
        try:
            documents_path = os.path.join(os.path.expanduser("~"), "Documents")
            carpeta_principal = os.path.join(documents_path, limpiar_nombre(f"{cedula} - {nombre}"))
            if not os.path.exists(carpeta_principal):
                os.makedirs(carpeta_principal)
        except PermissionError:
            # Si no se puede acceder a "Documentos", usar "Escritorio"
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            carpeta_principal = os.path.join(desktop_path, limpiar_nombre(f"{cedula} - {nombre}"))
            if not os.path.exists(carpeta_principal):
                os.makedirs(carpeta_principal)

        # Definir las categorías y sus respectivas columnas
        categorias = {
            "DOCUMENTOS PERSONALES": [
                'RESGISTO DE DEUDORES ALIMENTARIOS MOROSOS (REDAM)',
                'CERTIFICADO DE AFILIACIÓN A PENSIÓN Y/O RESOLUCIÓN DE PENSIONADO',
                'CERTIFICADO ANTECEDENTES DISCIPLINARIOS PROCURADURÍA',
                'CERTIFICADO ANTECEDENTES DISCIPLINARIOS DE SU PROFESIÓN VIGENTE',
                'CERTIFICADO ANTECEDENTES FISCALES CONTRALORÍA',
                'CERTIFICADO ANTECEDENTES POLICÍA NACIONAL',
                'SISTEMA REGISTRO NACIONAL DE MEDIDAS CORRECTIVAS (RNMC)',
                'ESTADO SITUACIÓN MILITAR',
                'COPIA DE TARJETA PROFESIONAL, MATRICULA PROFESIONAL Y/O REGISTRO EN LAS CARRERAS AUXILIARES',
                'CERTIFICADO DE AFILIACIÓN A SALUD COMO INDEPENDIENTE CON CONTRATO PRESTACIÓN DE SERVICIOS MAYOR A UN (1) MES.'
            ],
            "OTROS DOCUMENTOS": [
                'CERTIFICADO DE AFILIACIÓN A ARL',
                'COPIA DEL RUT',
                'CERTIFICACIÓN BANCARIA CUENTA PERSONAL.',
                'EXAMEN MÉDICO OCUPACIONAL.',
                'COPIA DE LA CÉDULA DE CIUDADANÍA POR AMBAS CARAS'
            ],
            "HOJA DE VIDA Y SOPORTES": [
                'CERTIFICACIONES LABORALES',
                'En un solo archivo en PDF, nombrado SOPORTES (peso entre 3Mb a 5Mb, sin fotos ni documentos borrosos), se debe incluir lo siguiente:'
            ]
        }

        # Crear subcarpetas y descargar archivos
        for categoria, columnas in categorias.items():
            carpeta_categoria = os.path.join(carpeta_principal, limpiar_nombre(categoria))
            if not os.path.exists(carpeta_categoria):
                os.makedirs(carpeta_categoria)

            for col_name in columnas:
                if col_name in df.columns:
                    enlace = row_values[df.columns.get_loc(col_name)]
                    if pd.notna(enlace) and isinstance(enlace, str):
                        print(f"Descargando archivo desde: {enlace}")

                        if "drive.google.com" in enlace:
                            file_id = enlace.split("id=")[-1]
                            download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                        else:
                            download_url = enlace

                        respuesta = requests.get(download_url)
                        if respuesta.status_code == 200 and "html" not in respuesta.headers.get('Content-Type', ''):
                            nombre_archivo = limpiar_nombre(col_name) + ".pdf"
                            ruta_archivo = os.path.join(carpeta_categoria, nombre_archivo)

                            with open(ruta_archivo, "wb") as archivo:
                                archivo.write(respuesta.content)
                            print(f"Archivo descargado correctamente en {ruta_archivo}.")
                        else:
                            print(f"No se pudo descargar el archivo en la columna '{col_name}'. Enlace no válido o acceso restringido.")
    finally:
        # Cerrar la ventana de carga y mostrar mensaje de descarga completa con la ruta principal
        loading_window.destroy()
        messagebox.showinfo("Descarga Completa", f"Todos los documentos se han descargado correctamente en la carpeta:\n\n{carpeta_principal}")
