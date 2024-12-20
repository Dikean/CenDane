# -*- coding: utf-8 -*-
"""NEW MACRO.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bGmICoPHJacSWb-9_5UBScXraLsXaOVd
"""

import gspread
from google.auth import default
from google.colab import auth

# Autenticación de usuario
auth.authenticate_user()

# Autoriza el uso de las credenciales
creds, _ = default()
gc = gspread.authorize(creds)

# ID de la hoja de cálculo
spreadsheet_id = '159CgHiDNcUK-bTSRLFWhCXhYzpF0zk4Y9yR9U2GxiG0'
spreadsheet = gc.open_by_key(spreadsheet_id)

# Seleccionar la hoja por su nombre
worksheet = spreadsheet.worksheet('Respuestas de formulario 1')

# Importar pandas
import pandas as pd

# Obtener todos los datos de la hoja en forma de DataFrame
data = worksheet.get_all_values()
headers = data.pop(0)  # Extrae la primera fila para usarla como encabezado
df = pd.DataFrame(data, columns=headers)

# Mostrar el DataFrame
print(df)

# Contar las respuestas por 'Marca temporal'
conteo_respuestas = df['4. Ingrese su número de documento de identidad '].value_counts()
print(conteo_respuestas)

# Solicitar el número de documento de identidad desde la consola
cedula = input("Por favor, ingresa el número de documento de identidad que deseas buscar: ")

# Filtrar los datos por el número de documento de identidad
resultado = df[df['4. Ingrese su número de documento de identidad '] == cedula]

# Mostrar los resultados
if not resultado.empty:
    print("Datos encontrados para el documento de identidad ingresado:")
    print(resultado)
else:
    print("No se encontraron datos para el documento de identidad ingresado.")

import os
import requests
import re  # Importamos re para limpiar nombres de archivos y carpetas

# Función para limpiar nombres de archivos y carpetas
def limpiar_nombre(nombre):
    # Reemplazamos caracteres especiales y espacios por guiones bajos
    return re.sub(r"[^\w\s-]", "", nombre).replace(" ", "_")

# Solicitar el número de documento de identidad desde la consola
cedula = input("Por favor, ingresa el número de documento de identidad que deseas buscar: ")

# Filtrar los datos por el número de documento de identidad
resultado = df[df['4. Ingrese su número de documento de identidad '] == cedula]

# Verificar si se encontraron datos para la cédula ingresada
if not resultado.empty:
    print("Datos encontrados para el documento de identidad ingresado:")
    print(resultado)

    # Nombre de ejemplo
    nombre = 'Test'

    # Crear la carpeta principal
    carpeta_principal = limpiar_nombre(f"{cedula} - {nombre}")
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

    # Parte 1: Crear todas las carpetas necesarias
    for categoria in categorias:
        carpeta_categoria = os.path.join(carpeta_principal, limpiar_nombre(categoria))
        if not os.path.exists(carpeta_categoria):
            os.makedirs(carpeta_categoria)  # Crear subcarpeta para cada categoría

    # Parte 2: Descargar y guardar los archivos en las carpetas correspondientes
    for categoria, columnas in categorias.items():
        carpeta_categoria = os.path.join(carpeta_principal, limpiar_nombre(categoria))

        # Descargar archivos de las columnas de esta categoría
        for col in columnas:
            if col in resultado.columns:
                enlace = resultado.iloc[0][col]
                if pd.notna(enlace) and isinstance(enlace, str):
                    print(f"Descargando archivo desde: {enlace}")

                    # Extraer el FILE_ID y convertirlo a un enlace directo
                    if "drive.google.com" in enlace:
                        file_id = enlace.split("id=")[-1]  # Extraer solo el ID del archivo
                        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                    else:
                        download_url = enlace  # Usa el enlace tal cual si no es de Google Drive

                    # Realizar la solicitud y guardar el archivo
                    respuesta = requests.get(download_url)
                    if respuesta.status_code == 200 and "html" not in respuesta.headers.get('Content-Type', ''):
                        nombre_archivo = limpiar_nombre(col) + ".pdf"
                        ruta_archivo = os.path.join(carpeta_categoria, nombre_archivo)

                        # Guardar el archivo en la ruta especificada
                        with open(ruta_archivo, "wb") as archivo:
                            archivo.write(respuesta.content)
                        print(f"Archivo descargado correctamente en {nombre_archivo}.")
                    else:
                        print(f"No se pudo descargar el archivo en la columna '{col}'. Enlace no válido o acceso restringido.")
            else:
                print(f"Advertencia: La columna '{col}' no se encontró en el DataFrame. Verifica el nombre exacto.")

    print(f"Todos los archivos asociados a la cédula {cedula} han sido descargados en la carpeta '{carpeta_principal}'.")

else:
    print("No se encontraron datos para el documento de identidad ingresado.")

from google.colab import drive
drive.mount('/content/drive')