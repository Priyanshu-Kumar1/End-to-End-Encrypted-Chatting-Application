import rsa
from .database import store



def generate_keys(uid):
    
    public_key, private_key = rsa.newkeys(1024)
    
    
    priPem = private_key.save_pkcs1(format='PEM').decode('utf-8')
    pubPem = public_key.save_pkcs1(format='PEM').decode('utf-8')
    
    print(type(priPem))
    
    keys= {"private_key": priPem,
           "public_key": pubPem}
    
    
    store(keys, f"users/{uid}")
    