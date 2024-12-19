from base64 import b64decode
from typing import Dict, Union, Optional
from cryptography.exceptions import InvalidKey, InvalidTag
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization, hashes
import os
from app.services.utils import log_error

# Configuration
MAX_PAYLOAD_SIZE = 1024 * 1024  # 1MB limit
ERROR_FILE_PATH = 'errors.log'

def load_private_key() -> Optional[rsa.RSAPrivateKey]:
    """Safely load the private key from environment."""
    try:
        with open('/home/ubuntu/whatsapp-flows-api/private_key.pem', 'r') as key_file:
            key_data = key_file.read()
    except FileNotFoundError:
        log_error(ERROR_FILE_PATH, "private_key.pem file not found")
        key_data = None
    except IOError as e:
        log_error(ERROR_FILE_PATH, f"Error reading private_key.pem: {str(e)}")
        key_data = None
    if not key_data:
        log_error(ERROR_FILE_PATH, "WHATSAPP_FLOW_PRIVATE_KEY not set")
        return None
    
    try:
        return serialization.load_pem_private_key(key_data.encode(), password=None)
    except Exception as e:
        log_error(ERROR_FILE_PATH, f"Failed to load private key: {str(e)}")
        return None

PRIVATE_KEY = load_private_key()

def process_whatsapp_request(data: Dict[str, str]) -> Dict[str, Union[str, dict]]:
    """Process encrypted WhatsApp flow data and return appropriate response."""
    try:
        # Validate payload size
        for key in ['encrypted_aes_key', 'encrypted_flow_data', 'initial_vector']:
            if len(data.get(key, '')) > MAX_PAYLOAD_SIZE:
                raise ValueError(f"Payload size exceeds maximum allowed size for {key}")

        # Validate private key
        if not PRIVATE_KEY:
            raise RuntimeError("Private key not properly configured")

        # Decode base64 encrypted data
        encrypted_aes_key = b64decode(data["encrypted_aes_key"])
        encrypted_flow_data = b64decode(data["encrypted_flow_data"])
        initial_vector = b64decode(data["initial_vector"])

        # Decrypt AES key using private key
        aes_key = PRIVATE_KEY.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Decrypt flow data using AES key
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

    except KeyError as e:
        error_msg = f"Missing required field in data: {str(e)}"
        log_error(ERROR_FILE_PATH, error_msg)
        return {"error": error_msg}

    except ValueError as e:
        error_msg = f"Invalid data format or size: {str(e)}"
        log_error(ERROR_FILE_PATH, error_msg)
        return {"error": error_msg}

    except (InvalidKey, InvalidTag) as e:
        error_msg = f"Cryptographic error: {str(e)}"
        log_error(ERROR_FILE_PATH, error_msg)
        return {"error": "Invalid encryption data"}

    except Exception as e:
        error_msg = f"Error processing WhatsApp request: {str(e)}"
        log_error(ERROR_FILE_PATH, error_msg)
        return {"error": error_msg}
