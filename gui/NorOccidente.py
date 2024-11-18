import customtkinter
from tkinter import filedialog, messagebox
import pandas as pd
import os

def get_noroccidente_frame(parent):
    noroccidente_frame = customtkinter.CTkFrame(master=parent, corner_radius=0)
    label = customtkinter.CTkLabel(noroccidente_frame, text="Procesamiento de Archivos NorOccidente", font=("Arial", 24))
    label.pack(pady=20)

    # Texto de guía para el usuario encargado
    guide_label = customtkinter.CTkLabel(
        noroccidente_frame,
        text="Instrucciones:\n1. Primero, cargue el archivo Excel con la información de los contratos.\n"
             "2. Asegúrese de que las columnas tengan los nombres correctos: 'NO. DE CONTRATO' y 'NO. DE CEDULA'.\n"
             "3. Luego, haga clic en 'Procesar Archivo' para eliminar duplicados y guardar los resultados.",
        wraplength=400,
        justify="left"
    )
    guide_label.pack(pady=10)

    # Etiqueta para mostrar el archivo cargado
    file_label = customtkinter.CTkLabel(noroccidente_frame, text="")
    file_label.pack(pady=5)

    # Variable para almacenar la ruta del archivo
    file_path = customtkinter.StringVar()

    # Función para cargar archivo
    def load_file():
        filename = filedialog.askopenfilename(title="Seleccione un archivo Excel",
                                              filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
        if filename:
            file_path.set(filename)
            file_label.configure(text=os.path.basename(filename))

    # Botón para cargar archivo
    load_file_button = customtkinter.CTkButton(noroccidente_frame, text="Cargar Archivo",
                                               command=load_file)
    load_file_button.pack(pady=10)

    # Función para eliminar duplicados y encontrar duplicados, guardando ambos en hojas separadas
    def process_file():
        if not file_path.get():
            messagebox.showerror("Error", "Debe cargar un archivo antes de procesar.")
            return

        try:
            # Leer el archivo
            data = pd.read_excel(file_path.get())

            # Filtrar solo los registros con un número de contrato válido
            data_valid_contracts = data[data['NO. DE CONTRATO'].str.contains('CO1.PCCNTR.', na=False)]

            # Convertir columnas a string para evitar problemas
            data_valid_contracts['NO. DE CONTRATO'] = data_valid_contracts['NO. DE CONTRATO'].astype(str)
            data_valid_contracts['NO. DE CEDULA'] = data_valid_contracts['NO. DE CEDULA'].astype(str)

            # Ordenar por 'NO. DE CEDULA' y 'NO. DE CONTRATO'
            data_sorted = data_valid_contracts.sort_values(by=['NO. DE CEDULA', 'NO. DE CONTRATO'], ascending=[True, False])

            # Eliminar duplicados en base a 'NO. DE CEDULA', conservando el contrato más alto
            data_cleaned = data_sorted.drop_duplicates(subset='NO. DE CEDULA', keep='first')

            # Identificar registros duplicados en base a 'NO. DE CEDULA'
            duplicates = data[data.duplicated(subset='NO. DE CEDULA', keep=False)]

            # Preguntar al usuario si quiere seleccionar la ubicación de guardado
            save_choice = messagebox.askyesno("Guardar archivo", "¿Desea seleccionar la ubicación para guardar el archivo procesado?")

            if save_choice:
                # Permitir al usuario elegir la ubicación para guardar el archivo
                output_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                    title="Guardar archivo procesado como"
                )
                if not output_path:
                    # Si el usuario cancela la operación de guardado, terminar la función
                    return
            else:
                # Guardar en la carpeta Documentos por defecto
                documents_path = os.path.expanduser("~/Documents")
                output_path = os.path.join(documents_path, "Direccion_Territorial_NorOccidente_Procesado.xlsx")

            # Guardar el archivo con dos hojas
            with pd.ExcelWriter(output_path) as writer:
                data_cleaned.to_excel(writer, sheet_name='Eliminados Duplicados', index=False)
                duplicates.to_excel(writer, sheet_name='Duplicados', index=False)

            messagebox.showinfo("Éxito", f"Archivo procesado y guardado en: {output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al procesar: {str(e)}")

    # Botón para procesar el archivo y ejecutar ambas funcionalidades
    process_button = customtkinter.CTkButton(noroccidente_frame, text="Procesar Archivo",
                                             command=process_file)
    process_button.pack(pady=20)

    return noroccidente_frame

