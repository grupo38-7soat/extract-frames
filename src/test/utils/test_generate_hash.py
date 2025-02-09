from src.utils.generate_hash import generate_hash

def test_generate_hash():
    input_data = "test_string"
    expected_hash = "4b641e9a923d1ea57e18fe41dcb543e2c4005c41ff210864a710b0fbb2654c11"
    assert generate_hash(input_data) == expected_hash

def test_generate_hash_empty_string():
    input_data = ""
    expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert generate_hash(input_data) == expected_hash

def test_generate_hash_special_characters():
    input_data = "!@#$%^&*()"
    expected_hash = "95ce789c5c9d18490972709838ca3a9719094bca3ac16332cfec0652b0236141"
    assert generate_hash(input_data) == expected_hash