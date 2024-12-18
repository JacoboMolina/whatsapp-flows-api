from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

PRIVATE_KEY = b"""
-----BEGIN PRIVATE KEY-----
<YOUR_PRIVATE_KEY_HERE>
-----END PRIVATE KEY-----
"""
private_key = serialization.load_pem_private_key(PRIVATE_KEY, password=None)

def process_whatsapp_request(data: dict):
    encrypted_aes_key = b64decode(data["encrypted_aes_key"])
    encrypted_flow_data = b64decode(data["encrypted_flow_data"])
    initial_vector = b64decode(data["initial_vector"])

    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(initial_vector))
    decryptor = cipher.decryptor()
    decrypted_flow_data = decryptor.update(encrypted_flow_data) + decryptor.finalize()

    return {
        "screen": "MAIN",
        "data": {
            "options": [
                {"id": "1", "title": "Dynamic Option 1"},
                {"id": "2", "title": "Dynamic Option 2"}
            ]
        }
    }
