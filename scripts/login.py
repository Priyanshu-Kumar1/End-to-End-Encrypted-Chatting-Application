from firebase_admin import credentials
from firebase_admin import auth
from .keys_gen import generate_keys

def check_user(email):
    try:
        auth.get_user_by_email(email)
    
    except auth.UserNotFoundError:
        return False #returns false if user not found
    
    else:
        return True #returns true if user found
    
def sign_up(name, photo_uri, email):
    
    print(check_user(email))
    
    if check_user(email):
        user = auth.get_user_by_email(email)
        
    
    else:
        user = auth.create_user(email= email, display_name = name, photo_url = photo_uri)
        generate_keys(user.uid)
        
        
        
    return user
        
    
def get_users():
    users = auth.list_users()
    return users.users





