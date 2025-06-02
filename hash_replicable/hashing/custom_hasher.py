import struct  # Para desempaquetar bloques de bytes a enteros
import hashlib  # Solo se usa para convertir el chaining_value en 256 bits al final

# Clase que implementa un hasher personalizado con encadenamiento y mezcla de bloques.
class CustomHasher:

    def __init__(self):
        # Valor inicial de encadenamiento (Chaining Value)
        # Usamos un valor fijo para replicabilidad
        self.chaining_value = 0xA5A5A5A5A5A5A5A5
        
    # Convierte 64 bytes a 8 enteros , luego los mezcla con XOR y rotaciones
    def _bytes_to_uint64(self, b: bytes) -> int:
        # Divide el bloque de 64 bytes en 8 palabras de 8 bytes (uint64)
        assert len(b) == 64, "Cada bloque debe tener 512 bits (64 bytes)"
        # Desempaqueta los bytes en 8 enteros de 64 bits (big-endian)
        parts = struct.unpack('>8Q', b)  # '>8Q' = big-endian, 8 uint64
        result = 0
        for p in parts: 
            # Aplica una rotación de 1 bit a la izquierda  y luego XOR con el acumulado para mezclar
            result ^= ((p << 1) | (p >> 63)) & 0xFFFFFFFFFFFFFFFF
        return result

    def _compress(self, block_value: int) -> int:
        # Mezcla el chaining value con el valor del bloque
        combined = self.chaining_value ^ block_value
        # Multiplica por número primo grande y aplica difusión (como SHA)
        combined = (combined * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
        combined ^= (combined >> 33)  # XOR con sí mismo desplazado 33 bits a la derecha (Difusión final)
        return combined

    def update(self, block: bytes):
        # Procesa un bloque y actualiza el chaining value
        block_value = self._bytes_to_uint64(block)
        self.chaining_value = self._compress(block_value)

    def digest(self) -> bytes:
        # Devuelve el hash final como 256 bits (32 bytes)
        # Aquí se usa SHA-256 solo para normalizar el tamaño de salida
        return hashlib.sha256(self.chaining_value.to_bytes(8, byteorder='big')).digest()

    def hexdigest(self) -> str:
        # Devuelve el hash final como string hexadecimal
        return self.digest().hex()
    
    # Recorre todo el archivo por bloques y devuelve el hexdigest final.
    def hash_file(self, file_path):
        # Reiniciamos el chaining_value a su estado inicial
        self.chaining_value = 0xA5A5A5A5A5A5A5A5  
        from hashing.utils import read_file_in_blocks  # Import local

        for block in read_file_in_blocks(file_path):
            self.update(block)
        return self.hexdigest()
