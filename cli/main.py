import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from core.app_project import AppProject  # Ajusta la ruta si usas imports relativos

def guia():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 40)
    print("🧙 MitsPyGUIAppsWizard")
    print("  Creador de apps GUI estilo CLI")
    print("=" * 40)
    print("1. Create App")
    print("2. Exit")
    print("=" * 40)

    choice = input("Selecciona una opción (1-2): ")
    if choice == "1":
        create_app_flow()
    elif choice == "2":
        print("👋 Cerrando el asistente. ¡Hasta luego!")
        exit()
    else:
        print("❌ Opción no válida.")
        guia()

def create_app_flow():
    print("\n📝 Introduce el nombre de tu aplicación:")
    app_name = input("Nombre de la app: ").strip()

    if not app_name:
        print("⚠️ El nombre no puede estar vacío.")
        return guia()

    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Selecciona la carpeta del proyecto")
    
    framework_folder = Path(__file__).parent.parent.resolve()

    path = Path(folder)

    if path:
        print(f"📂 Carpeta seleccionada: {folder}")
        project = AppProject(app_name, path, framework_folder)
        print("🚀 AppProject inicializado con éxito.")
        project.bootstrap()
    else:
        print("⚠️ No se seleccionó carpeta.")
        guia()

