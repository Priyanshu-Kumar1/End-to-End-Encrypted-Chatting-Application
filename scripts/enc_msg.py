import rsa
from .database import append_data


def send(msg, key, receiver_id, sender_id):
    msg = msg.encode('utf-8')
    key = key.encode('utf-8')
    key = rsa.PublicKey.load_pkcs1(key, format='PEM')
    crypto_msg = rsa.encrypt(msg, key)
    append_data(str(crypto_msg), f"{receiver_id}/messages/{sender_id}")
    
def decrypt_msg(msg, key):
    key = key.encode('utf-8')
    key = rsa.PrivateKey.load_pkcs1(key, format='PEM')
    msg = rsa.decrypt(msg, key)
    msg = msg.decode('utf-8')
    return msg
    