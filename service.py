from time import sleep



from jnius import autoclass



PythonService = autoclass('org.kivy.android.PythonService')

PythonService.mService.setAutoRestartService(True)





from firebase_admin import db


def listener(self, event):
	print("got changes...")


db.reference("Yh7gqPlntrdJ7y9S8cJjEBpxC4A3/messages/").listen(listener)


