import hashlib

def generate_hash(input_string):
    # Cria um objeto hash SHA-256
    sha256_hash = hashlib.sha256()

    # Atualiza o objeto hash com a string de entrada codificada em bytes
    sha256_hash.update(input_string.encode('utf-8'))

    # Retorna o hash hexadecimal
    return sha256_hash.hexdigest()
