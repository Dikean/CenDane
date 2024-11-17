import customtkinter
from tkinter import Menu
from PIL import Image, ImageTk  # Importa para manejar la imagen
import os
import sys
from gui.home import get_home_frame
from gui.relacionar import get_relacionar_frame
from gui.NorOccidente import get_noroccidente_frame

customtkinter.set_appearance_mode("dark")  # Modo oscuro
customtkinter.set_default_color_theme("blue")  # Tema de color azul

# Función para obtener la ruta de los recursos, para poder acceder a ellos en el ejecutable
def get_resource_path(relative_path):
    """ Obtiene la ruta al recurso empaquetado (o la ruta relativa si no está empaquetado). """
    try:
        # PyInstaller coloca archivos en una carpeta temporal.
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("CenDANE")
        self.geometry("900x500")

        # Sidebar y área de contenido
        self.setup_ui()
        
        # Cargar y establecer el ícono de la aplicación (para la barra de tareas)
        try:
            icon_path = get_resource_path("./assets/Logo.ico")
            self.iconbitmap(icon_path)  # Cambia a la ruta de tu archivo .ico
        except Exception as e:
            print(f"No se pudo cargar el icono: {e}")
        
        # Página de inicio por defecto
        self.current_frame = None
        self.show_home()

    def setup_ui(self):
        # Configuración del sidebar
        self.sidebar = customtkinter.CTkFrame(master=self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)  # Añadir padding al sidebar
        self.sidebar.configure(fg_color="#333440")

        # Cargar y mostrar la imagen en el sidebar
        try:
            image_path = get_resource_path("./assets/Logo.png")
            image = Image.open(image_path)
            image = image.resize((135, 60))
            self.image_tk = ImageTk.PhotoImage(image)

            self.image_label = customtkinter.CTkLabel(self.sidebar, image=self.image_tk, text="")
            self.image_label.pack(pady=10)  # Añadir padding para la imagen
        except FileNotFoundError:
            print(f"No se pudo encontrar la imagen en la ruta {image_path}")

        # Área de contenido
        self.content_area = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.content_area.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Botones en el sidebar con padding
        self.button_home = customtkinter.CTkButton(self.sidebar, text="HOME", command=self.show_home)
        self.button_home.pack(pady=10, padx=10, fill='x')

        self.button_assignments = customtkinter.CTkButton(self.sidebar, text="MIS ASIGNADOS",
                                                          command=lambda: self.button_action("Button 2"))
        self.button_assignments.pack(pady=10, padx=10, fill='x')

        self.button_with_menu = customtkinter.CTkButton(self.sidebar, text="OPCIONES")
        self.button_with_menu.pack(pady=10, padx=10, fill='x')
        self.button_with_menu.bind("<Button-1>", self.show_menu)

        # Submenú
        self.menu = Menu(self, tearoff=0)
        self.menu.add_command(label="RELACIONAR", command=self.show_relacionar)
        self.menu.add_command(label="NOROCCIDENTE", command=self.show_noroccidente)

    def show_home(self):
        self.switch_frame(get_home_frame)

    def show_relacionar(self):
        self.switch_frame(get_relacionar_frame)

    def show_noroccidente(self):
        self.switch_frame(get_noroccidente_frame)

    def switch_frame(self, frame_func):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
        self.current_frame = frame_func(self.content_area)
        self.current_frame.pack(fill="both", expand=True)

    def button_action(self, button):
        print(f"{button} was clicked!")

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def menu_action(self, option):
        print(f"{option} selected from menu")

if __name__ == "__main__":
    app = App()
    app.mainloop()

