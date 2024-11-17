import customtkinter
from tkinter import filedialog, messagebox
import pandas as pd
import os

def get_relacionar_frame(parent):
    relacionar_frame = customtkinter.CTkFrame(master=parent, corner_radius=0)
    label = customtkinter.CTkLabel(relacionar_frame, text="Configuración de Fusión de Archivos")
    label.pack(pady=20)

    # Crear un contenedor de dos columnas para los botones de carga de archivos
    file_buttons_frame = customtkinter.CTkFrame(master=relacionar_frame)
    file_buttons_frame.pack(pady=10, padx=20, fill="x")

    # Campo de entrada para las columnas comunes
    merge_column_entry = customtkinter.CTkEntry(file_buttons_frame, placeholder_text="Columna común para fusionar...")
    merge_column_entry.grid(row=0, column=0, padx=5, pady=5, sticky="w")  # Posicionar a la izquierda

    # Etiquetas para mostrar los archivos cargados
    primary_file_label = customtkinter.CTkLabel(file_buttons_frame, text="")
    secondary_file_label = customtkinter.CTkLabel(file_buttons_frame, text="")

    # Variables para almacenar las rutas de los archivos
    primary_file_path = customtkinter.StringVar()
    secondary_file_path = customtkinter.StringVar()

    # Función para cargar archivos
    def load_file(path_variable, title, label):
        filename = filedialog.askopenfilename(title=title, filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
        if filename:
            path_variable.set(filename)
            label.configure(text=os.path.basename(filename))

    # Botón para cargar archivo principal
    load_primary_button = customtkinter.CTkButton(file_buttons_frame, text="Cargar Archivo Principal",
                                                  command=lambda: load_file(primary_file_path, "Seleccione el archivo principal", primary_file_label))
    load_primary_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    primary_file_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    # Botón para cargar archivo secundario
    load_secondary_button = customtkinter.CTkButton(file_buttons_frame, text="Cargar Archivo Secundario",
                                                    command=lambda: load_file(secondary_file_path, "Seleccione el archivo secundario", secondary_file_label))
    load_secondary_button.grid(row=1, column=1, padx=5, pady=5, sticky="e")
    secondary_file_label.grid(row=2, column=1, padx=5, pady=5, sticky="e")

    # Función para fusionar los archivos directamente
    def merge_into_primary():
        primary_path = primary_file_path.get()
        secondary_path = secondary_file_path.get()
        merge_column = merge_column_entry.get()

        if not primary_path or not secondary_path:
            messagebox.showerror("Error", "Debe cargar ambos archivos antes de fusionar.")
            return
        if not merge_column:
            messagebox.showerror("Error", "Debe especificar la columna común para fusionar.")
            return

        try:
            # Leer los datos de ambos archivos
            primary_df = pd.read_excel(primary_path)
            secondary_df = pd.read_excel(secondary_path)

            # Verificar que la columna existe en ambos archivos
            if merge_column not in primary_df.columns or merge_column not in secondary_df.columns:
                messagebox.showerror("Error", f"La columna '{merge_column}' no existe en uno o ambos archivos.")
                return

            # Fusionar los datos
            merged_df = pd.merge(primary_df, secondary_df, on=merge_column, how='inner')

            # Definir la ruta del archivo fusionado en Documentos
            documents_path = os.path.expanduser("~/Documents")
            fusion_file_path = os.path.join(documents_path, "Fusión.xlsx")

            # Guardar el archivo fusionado en la carpeta Documentos
            merged_df.to_excel(fusion_file_path, index=False)
            messagebox.showinfo("Éxito", f"Archivos fusionados correctamente y guardados en: {fusion_file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al fusionar: {str(e)}")

    # Botón para fusionar archivos
    merge_button = customtkinter.CTkButton(relacionar_frame, text="Fusionar Archivos", command=merge_into_primary)
    merge_button.pack(pady=20)

    return relacionar_frame


