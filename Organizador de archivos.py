import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog

TIPOS = {
    'imagenes': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'documentos': ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.pptx'],
    'musica': ['.mp3', '.wav', '.aac'],
    'videos': ['.mp4', '.avi', '.mov', '.mkv'],
    'otros': ['.zip', '.rar', '.exe', '.iso', '.html', '.css', '.js']
}

CARPETAS_WINDOWS = {
    "Escritorio": "Desktop",
    "Descargas": "Downloads",
    "Documentos": "Documents",
    "Imágenes": "Pictures",
    "Música": "Music",
    "Videos": "Videos"
}

def mover_archivo(origen, destino_dir, nombre_archivo):
    destino = os.path.join(destino_dir, nombre_archivo)
    base, ext = os.path.splitext(nombre_archivo)
    i = 1
    while os.path.exists(destino):
        destino = os.path.join(destino_dir, f"{base}_{i}{ext}")
        i += 1
    try:
        shutil.move(origen, destino)
    except Exception as e:
        print(f"Error moviendo {nombre_archivo}: {e}")

def organizar_carpeta(carpeta):
    resumen = {k: 0 for k in TIPOS.keys()}
    for carpeta_tipo in TIPOS.keys():
        os.makedirs(os.path.join(carpeta, carpeta_tipo), exist_ok=True)
    for archivo in os.listdir(carpeta):
        if archivo.startswith('.'):
            continue
        ruta_archivo = os.path.join(carpeta, archivo)
        if os.path.isdir(ruta_archivo) and archivo in TIPOS.keys():
            continue
        if os.path.isfile(ruta_archivo):
            extension = os.path.splitext(archivo)[1].lower()
            movido = False
            for tipo, extensiones in TIPOS.items():
                if extension in extensiones:
                    mover_archivo(ruta_archivo, os.path.join(carpeta, tipo), archivo)
                    resumen[tipo] += 1
                    movido = True
                    break
            if not movido:
                mover_archivo(ruta_archivo, os.path.join(carpeta, 'otros'), archivo)
                resumen['otros'] += 1
    return resumen

def on_organizar(nombre_carpeta):
    ruta = os.path.join(os.path.expanduser("~"), CARPETAS_WINDOWS[nombre_carpeta])
    if not os.path.exists(ruta):
        messagebox.showerror("Error", f"No se encontró la carpeta {nombre_carpeta}")
        return
    resumen = organizar_carpeta(ruta)
    mostrar_resumen(resumen)

def on_organizar_personalizado():
    ruta = filedialog.askdirectory(title="Selecciona la carpeta a organizar")
    if not ruta:
        return
    resumen = organizar_carpeta(ruta)
    mostrar_resumen(resumen)

def mostrar_resumen(resumen):
    mensaje = "¡Organización completada!\n\nResumen:\n"
    for tipo, cantidad in resumen.items():
        mensaje += f"{tipo}: {cantidad} archivo(s)\n"
    messagebox.showinfo("Resultado", mensaje)

# Interfaz gráfica
root = tk.Tk()
root.title("Organizador de Carpetas")

label = tk.Label(root, text="Selecciona la carpeta que deseas organizar:", font=("Arial", 12))
label.pack(pady=10)

for nombre in CARPETAS_WINDOWS.keys():
    btn = tk.Button(root, text=nombre, width=20, command=lambda n=nombre: on_organizar(n))
    btn.pack(pady=3)

btn_personalizado = tk.Button(root, text="Elegir otra carpeta...", width=20, command=on_organizar_personalizado)
btn_personalizado.pack(pady=10)

root.mainloop()