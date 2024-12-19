from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64decode, b64encode
import logging

# Configurar logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Función para encriptar la respuesta, usando el mismo IV que se recibió
def encrypt_response(data, aes_key, iv):
    # Configuración del cifrado AES usando el mismo IV
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Asegúrate de que los datos sean múltiplos de 16 para el cifrado
    padding_length = 16 - (len(data) % 16)
    padded_data = data + (chr(padding_length) * padding_length).encode()

    # Encriptar los datos
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Loguear los datos cifrados
    logger.info(f"Encrypted response data (base64): {b64encode(encrypted_data).decode('utf-8')}")
    logger.info(f"IV used for encryption (base64): {b64encode(iv).decode('utf-8')}")

    # Retornar los datos cifrados y el IV como parte de la respuesta
    return b64encode(encrypted_data).decode('utf-8'), b64encode(iv).decode('utf-8')

@app.post("/flows_dinamic")
async def process_flow(request: Request):
    request_body = await request.json()

    # Verificar que los campos necesarios estén presentes
    if 'encrypted_flow_data' not in request_body or 'encrypted_aes_key' not in request_body or 'initial_vector' not in request_body:
        raise HTTPException(status_code=422, detail="Missing fields in the request body")
    
    # Desencriptar los datos usando el initial_vector recibido
    decrypted_data = process_decryption(
        request_body['encrypted_flow_data'],
        request_body['encrypted_aes_key'],
        request_body['initial_vector']  # Usar el 'initial_vector' recibido
    )

    # Loguear los datos desencriptados
    logger.info(f"Decrypted data: {decrypted_data}")

    # Enviar la respuesta cifrada usando el mismo IV recibido
    response_data, iv = encrypt_response(decrypted_data, b64decode(request_body['encrypted_aes_key']), b64decode(request_body['initial_vector']))
    
    # Loguear la respuesta cifrada
    logger.info(f"Encrypted response data: {response_data}")

    # Crear la respuesta para WhatsApp
    return {
        "encrypted_flow_data": response_data,
        "encrypted_aes_key": request_body['encrypted_aes_key'],  # Deberías retornar el mismo AES key
        "initial_vector": iv  # Asegúrate de enviar el IV con la respuesta
    }
