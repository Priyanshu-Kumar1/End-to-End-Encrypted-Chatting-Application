import firebase_admin

from firebase_admin import credentials

from firebase_admin import db



cred = credentials.Certificate("scripts/firebase-sdk.json")

firebase_admin.initialize_app(cred, {
    
    "databaseURL": "https://vibez-353508-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': 'vibez-353508.appspot.com',
        
        })





def store(data, path= "/"):

    ref= db.reference(path)

    ref.set(data)



def get_data(path= "/"):

    ref= db.reference(path)

    return ref.get()



def append_data(data, path= "/"):

    ref= db.reference(path)

    try:

        index = len(ref.get())

    except:

        index = 0

    path = path + f"/{index}"

    store(data, path)

    



    



    

if __name__ == "__main__":
    
    

    path= "/"

    print(append_data("hii", path))

    

    

    