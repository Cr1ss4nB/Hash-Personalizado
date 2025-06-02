class BlockReader:
    # Clase que permite leer un archivo en bloques de tamaño fijo (512 bits = 64 bytes).

    def __init__(self, filepath: str, block_size: int = 64): # Inicializa el lector de bloques.
        self.filepath = filepath
        self.block_size = block_size # Tamaño del bloque en bytes (64 bytes = 512 bits)

    # read_blocks: Generador que lee el archivo en bloques de tamaño fijo.
    def read_blocks(self):
        # Rinde cada bloque como bytes. Si el último bloque es más pequeño, se rellena con ceros (padding).
        with open(self.filepath, 'rb') as f:
            while True:
                block = f.read(self.block_size)
                if not block:
                    break
                if len(block) < self.block_size:
                    # Se añade padding con ceros si el bloque final es incompleto
                    block += b'\x00' * (self.block_size - len(block))
                yield block #Generador para que no cargue todo en memoria
