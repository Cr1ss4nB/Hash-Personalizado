import os
import time

BLOCK_SIZE = 64  # 64 bytes = 512 bits

#Generador para leer un archivo en bloques de 64 bytes (512 bits)
def read_file_in_blocks(file_path):
    with open(file_path, 'rb') as f:
        while True:
            block = f.read(BLOCK_SIZE)
            if not block:
                break
            # Rellenar si el bloque es menor a 64 bytes (último bloque)
            if len(block) < BLOCK_SIZE:
                block = block.ljust(BLOCK_SIZE, b'\x00')
            yield block

# Devuelve el tamaño del archivo en bytes
def get_file_size(file_path):
    return os.path.getsize(file_path)

# Decorador para medir el tiempo de ejecución de una función
def measure_execution_time(func):
    def wrapper(*args, **kwargs): # Wrapper para medir el tiempo de ejecución
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start # Tiempo transcurrido
        return result, elapsed
    return wrapper
