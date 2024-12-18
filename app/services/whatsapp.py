from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

PRIVATE_KEY = b"""
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC03ADKEC9fnLk8
K0HYNvjLoRlNaMtfJuDry/u6nYfkBEGo+TdMPWVqLCz8ekbYFNo12OcTgLyfB7WA
pzXMWkDqSmk4yew+8zrgpqC/DNL3VuRuV57qmO7Q/7rkkK0iSwCuHvMXZD9AlZMi
pbjpmbyYDF8IWzyF9In8I1EdgP+gfDmvlyeklU58aP4ZhJoZaYdoCqKxS5FuOMaf
TmpbMkRNnRbUkpndCKg01l2GtgQruW9EpsyDEB2CVC3nxCDCYylT1Q0c7tEqQ2vr
cbXejiT16LfGAQcVpiTchl7y7UOL3AnnI5+wd5+O/qWEsCasI+1atITEUqETf2pF
D7ixM2R3AgMBAAECggEASkJu/IiKuwphsEfeoEVqAEokVnlpz6bqAUdfE6+s5T2u
LBAv2Vj4NBDxY7VdM0nUkvl9X6+jQvTqXGnLmB2Su+BTteKK4woBqc4hAHDminIe
FwRZFuA2ZpAqD8ErpYIARH4mt/sMUZtYr4g2FYxvOEsUFh1IC4Rtx55EpwWZcC4A
nnNLM23DlAZJVktnBFhWN06E+qsuZ7wpfUTezFsge98+6tvXfckJtThltDLOqoFe
Wj7g14QuHmqXVzxYoqQ2FnOB9qGZzcqROhD0MSBohg1S/aR3c+j7HIOvAX9TWsCn
vQiKJtHPcm+4DNeMFxyXHWX6KIvgcH/ZDyNdFx046QKBgQDihTkf1jy4EeODTyhc
aAYmS5pVrAyXbBRxnOeDbiwsLIGXGAqDFgiioLieD3KdKi8qN1oVO/hrai3qtrF1
0miHU+AV3jJNgWKhWyqUYWxJHu1wD87jhDdM/KcXvLlBiDdgovMqZ71c+54otRra
wQFIiOjaCzndvYfoWzyvYvHK2wKBgQDMZYhqqfdx1qnFOAth5PUwKGPkeW7z5FcQ
z+tvQykAQBYKSm2tEP3M6dd9uLsLxxQ8jO5jZwxgxsEbdIvEUdY6H+hAc1Jn1C4i
3y51sULCifOrO7Rg44pPBHaWDusnkD5qGXE5f1+t1qyU7pAo7lDeNJB34x4jaNbG
i1KBlLXplQKBgCptT4TCCL9lQlrO0b11EmnL0U1omzclXDLnc4lvckCX2XHmY9mn
n9huCAY62HnNc+YRVgMSJ3Ze/divfU+XKFLoh9kws/VGXaXhQHloQfL0Iv7RRyvg
EMePrvBIPd6jV9P20VrI8XPgAQCY4z3D1qyyUAK/BYidvj3sENK80pLvAoGBAKNL
Qo8ktwGFpCBhxAYzqwcMXbH8qf3DoSNXWRqMp0cB7BnQmIq5lmqNL5HLcfPY2nv9
g756Z1Mxtrk+hSMU1nedYimLeHxm8Wz+rNluAo31NGzKyDLX1nmGcU81H/19qb+O
D/0Fm+UAKuTZKubobkb366s8Eansaho42HOZ4TN5AoGAQdhblmaMidFZuQkcVfJK
CeQpvxX6qdN7qERMun5lNx3OjxxIYxpZsDE8UfdRsCiCBtZImv1okwGvh1zJw/C5
soG384dgp9z5jD6j7U/eUB1FE/0cerFYejPD+qpAgyuRPgR7RsYVZrQcWgHzyM27
/k1Ie1MNLf5LIcHuhVOoaSM=
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
