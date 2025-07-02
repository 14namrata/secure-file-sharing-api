from app.utils.encryption import generate_encrypted_file_token, decrypt_file_token

def test_encryption_decryption():
    original_id = "testfile123"
    token = generate_encrypted_file_token(original_id)
    decrypted = decrypt_file_token(token)

    assert decrypted == original_id, "Decryption did not match original file ID"
