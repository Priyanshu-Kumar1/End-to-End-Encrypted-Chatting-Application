from tinydb import TinyDB, Query



db = TinyDB('db.json')

User = Query()



def local_login(email):

    user = db.search(User.email == email)

    if user == []:

        db.insert({'email': email, 'logged_in': True})

    else:

        db.update({'logged_in': True}, User.email == email)



def auto_login():

    user = db.search(User.logged_in == True)

    if user != []:

        return True

    else:

        return False



def logout(*args):

    user = db.search(User.logged_in == True)

    if user != []:

        db.update({'logged_in': False}, User.logged_in == True)

    

#add_user("rprem058@gmail.com", "7319656722", True)

#auto_login("rprem058@gmail.com", "7319656722")

#logout()