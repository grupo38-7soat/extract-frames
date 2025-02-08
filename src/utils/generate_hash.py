import hashlib

def generate_hash(input_string):
    sha256_hash = hashlib.sha256()

    sha256_hash.update(input_string.encode('utf-8'))

    return sha256_hash.hexdigest()
