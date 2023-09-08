from jnius import autoclass

TimeUnit = autoclass('java.util.concurrent.TimeUnit')

this = ('java.lang.this')

FirebaseApp = autoclass('com.google.firebase.FirebaseApp')
FirebaseApp.initializeApp(this)

FirebaseAuth = autoclass('com.google.firebase.auth.FirebaseAuth')



mAuth = FirebaseAuth.getInstance()

PhoneAuthProvider = autoclass('com.google.firebase.auth.PhoneAuthProvider')
PhoneAuth = PhoneAuthProvider()



def tryLogin(phoneNumber):
    PhoneAuth.newBuilder(mAuth).setPhoneNumber(phoneNumber).setTimeout(60, TimeUnit.SECONDS).setActivity(this).setCallbacks(afterLogin).build()

def afterLogin(*args):
    print("Logged in:", args)