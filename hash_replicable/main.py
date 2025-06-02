import os # Para manejar rutas y archivos
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime 
from hashing.custom_hasher import CustomHasher # Importa el hasher personalizado
from hashing.utils import read_file_in_blocks, get_file_size, measure_execution_time # Utilidades para leer archivos y medir tiempo
from tqdm import tqdm # Para mostrar el progreso del hashing

# Ruta donde están los archivos a probar
CARPETA_ARCHIVOS = r"hash_replicable\archivos"
# Carpeta destino de los hashes
CARPETA_SALIDA = r"hash_replicable\HashesGenerados"
os.makedirs(CARPETA_SALIDA, exist_ok=True)

@measure_execution_time
def hash_file(file_path): # Calcula el hash de un archivo usando el hasher personalizado
    hasher = CustomHasher()
    file_size = get_file_size(file_path)
    num_blocks = (file_size + 63) // 64

    # Usamos tqdm para mostrar el progreso del hashing
    for block in tqdm(read_file_in_blocks(file_path), total=num_blocks, desc="Hashing"):
        hasher.update(block)

    return hasher.hexdigest()

def guardar_hash(file_path, hash_str): # Guarda el hash en un archivo de texto con nombre basado en el archivo original
    nombre = os.path.basename(file_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_salida = f"hash_{os.path.splitext(nombre)[0]}_{timestamp}.txt"
    ruta_salida = os.path.join(CARPETA_SALIDA, nombre_salida)

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(f"Ruta del Archivo: {file_path}\n")
        f.write(f"Hash generado: {hash_str}\n")

    return ruta_salida

def seleccionar_y_procesar():
    # Abre diálogo en la carpeta fija
    ruta = filedialog.askopenfilename(
        initialdir=CARPETA_ARCHIVOS,
        title="Seleccionar archivo"
    )
    if not ruta:
        return  # Se canceló

    tamaño = get_file_size(ruta)
    if tamaño < 1024 * 1024:
        messagebox.showerror("Error", "El archivo debe tener al menos 1 MB.")
        return

    # Calcula hash y tiempo
    hash_str, tiempo = hash_file(ruta)
    # Guarda en txt
    ruta_txt = guardar_hash(ruta, hash_str)

    # Imprime en consola
    print(f"Archivo: {ruta}")
    print(f"Hash:    {hash_str}")
    print(f"Guardado en: {ruta_txt}")
    print(f"Tiempo ejecución: {tiempo:.4f} s")

    # Muestra en ventana emergente
    messagebox.showinfo(
        "Hash calculado ✅",
        f"Archivo: {os.path.basename(ruta)}\n"
        f"Hash: {hash_str}\n\n"
        f"Guardado en:\n{ruta_txt}\n"
        f"Tiempo: {tiempo:.4f} s"
    )

def main():
    ventana = tk.Tk()
    ventana.title("Hashing de Archivos")
    ventana.geometry("350x150")
    ventana.resizable(False, False)

    btn = tk.Button(
        ventana,
        text="Seleccionar archivo para hashear",
        command=seleccionar_y_procesar,
        width=30,
        height=2
    )
    btn.pack(expand=True)

    ventana.mainloop()

if __name__ == "__main__":
    main()
