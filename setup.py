from cx_Freeze import setup, Executable
import sys
import os

# Configuración del ejecutable
build_exe_options = {
    "packages": ["os", "pandas", "gspread", "google.auth", "re", "requests"],
    "include_files": [
        ("assets", "assets"),  # Incluye la carpeta "assets"
        ("gui", "gui"),        # Incluye la carpeta "gui"
        "Credentials.json",    # Incluye el archivo "Credentials.json"
    ],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Usa "Win32GUI" para aplicaciones sin consola (windowed)

setup(
    name="view",
    version="1.0",
    description="Mi aplicación con cx_Freeze",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script="view.py",
            base=base,
            icon="assets/Logo.ico"  # Incluye tu ícono
        )
    ],
)
