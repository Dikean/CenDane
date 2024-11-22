import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return None

def get_count_barrido_frame(parent):
    frame = tk.Frame(parent)  # Define el frame

    def load_and_process_data():
        # Crear la ventana raíz de Tkinter
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana

        # Solicitar al usuario que seleccione el archivo de Excel
        filepath = filedialog.askopenfilename(title="Selecciona el archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
        if not filepath:
            messagebox.showinfo("Cancelado", "Operación cancelada por el usuario.")
            return

        # Cargar el archivo sin encabezados para evitar errores
        df = pd.read_excel(filepath, header=None)
        # Establecer manualmente los nombres de las columnas
        df.columns = ['ID SOLICITUD', 'FECHA SOLICITUD', 'TERRITORIAL', 'DEPARTAMENTO', 'MUNICIPIO', 'METODO', 'COM', 'OPERATIVO']

        # Eliminar filas superiores que no contienen datos relevantes
        df = df.drop([0], axis=0)  # Ajusta si es necesario

        # Solicitar al usuario el rango de fechas
        start_date_str = simpledialog.askstring("Fecha de inicio", "Ingrese la fecha de inicio (DD/MM/YYYY):")
        end_date_str = simpledialog.askstring("Fecha de fin", "Ingrese la fecha de fin (DD/MM/YYYY):")
        if not all([start_date_str, end_date_str]):
            messagebox.showinfo("Cancelado", "Operación cancelada por el usuario.")
            return

        try:
            df['FECHA SOLICITUD'] = df['FECHA SOLICITUD'].apply(parse_date)
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)

            if not start_date or not end_date:
                raise ValueError("Las fechas de inicio o fin son inválidas.")

            filtered_df = df[(df['FECHA SOLICITUD'] >= start_date) & (df['FECHA SOLICITUD'] <= end_date)]

            # Contar los registros por municipio
            result_df = filtered_df['MUNICIPIO'].value_counts().reset_index()
            result_df.columns = ['MUNICIPIO', 'CANTIDAD']

            # Guardar el resultado en un nuevo archivo Excel
            output_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Guardar archivo como")
            if output_path:
                result_df.to_excel(output_path, index=False)
                messagebox.showinfo("Completado", f"Archivo guardado en: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el archivo: {str(e)}")

        root.destroy()

    # Botón para cargar datos y procesarlos
    load_button = tk.Button(frame, text="Cargar y Procesar Datos", command=load_and_process_data)
    load_button.pack(pady=20)

    return frame  # Retornar el frame después de haberlo definido completamente

if __name__ == "__main__":
    root = tk.Tk()
    main_frame = get_count_barrido_frame(root)
    main_frame.pack(fill='both', expand=True)
    root.mainloop()
