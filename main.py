import logging
import os
os.environ['KIVY_TEXT'] = 'pango'

from datetime import datetime
from kivymd.app import MDApp
from kivy.lang import Builder  # For Kivy language
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior, CircularElevationBehavior, RectangularRippleBehavior, CircularRippleBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.fitimage.fitimage import FitImage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivyauth.google_auth import initialize_google, login_google, logout_google
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.label import MDLabel
from kivy.core.text import Label as CoreLabel
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex as C
from firebase_admin import db
from kivy.clock import Clock
from googletrans import Translator
from functools import partial
#from kivysome import icon
import kivysome
kivysome.enable("https://kit.fontawesome.com/1bd406a948.js", group=kivysome.FontGroup.SOLID)

#importing custom scripts
from scripts.database import append_data, get_data, store 
from scripts.login import get_users, sign_up
from scripts.localdb import auto_login, local_login
from scripts.enc_msg import send, decrypt_msg





#//user object
class User():
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.email = ""
        self.name = ""
        self.uid = ""
        self.dp = ""

#//receiver object
class Receiver():
    def __init__(self):
        self.email = ""
        self.name = ""
        self.uid = ""
        self.public_key = None

user = User()
receiver = Receiver()
translator = Translator()

class Card(RoundedRectangularElevationBehavior, MDFloatLayout):
    pass

class DisplayPic(CircularElevationBehavior, ButtonBehavior, FitImage):
    pass

class ButtonLayout(RectangularRippleBehavior, ButtonBehavior, MDFloatLayout):
    pass

class UserCard(ButtonBehavior, Card):
    def __init__(self, name, dp, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.dp = dp

class MsgLabel(Label):
    @staticmethod
    def create_sized_label(**kwargs):
        max_width = kwargs.pop('max_width', 0)
        if max_width <= 0:
            # just create a MsgLabel without a text_size
            return MsgLabel(**kwargs)

        # calculate what the MsgLabel size will be
        core_label = CoreLabel(padding=[10,10], **kwargs)  # use same padding as Msglabel
        core_label.refresh()

        if core_label.width > max_width:
            # width is too big, use text_size to force wrapping
            return MsgLabel(text_size=(max_width,None), **kwargs)
        else:
            # width is OK, no need for text_size
            return MsgLabel(**kwargs)
        
    
    

class Msg(MDBoxLayout):
    def __init__(self, text= "", time_stamp= "", chat_layout = ObjectProperty(None), **kwargs):
        super().__init__(**kwargs)
        self.chat_layout = chat_layout
        self.max_width = (self.chat_layout.width) * 0.9
        self.text= text
        self.time_stamp= time_stamp
        self.add_text()
    
    def add_text(self):
        self.msg_lb = MsgLabel.create_sized_label(text=self.text, max_width=self.max_width, font_name='Roboto', font_size=15)
        time_stamp_lb = MsgLabel.create_sized_label(text=self.time_stamp, max_width=self.max_width, font_name='Roboto', font_size=11)
        time_stamp_lb.color = C("#b3b3b3")
        self.add_widget(self.msg_lb)
        self.add_widget(time_stamp_lb)
        

class ChatView(MDBoxLayout):
    
    def create_chat(self, text, timstamp, sender, *args):
        self.max_width = ((self.width/2) + 10) * 0.9
        msg= Msg(text= text, adaptive_size= True, time_stamp= timstamp, chat_layout = self)
        
        if sender:
            msg.radius = ["10dp", "10dp", "0dp", "10dp"]
            space = MDFloatLayout(size_hint_x = 1)
            msg_layout = MDBoxLayout(adaptive_height= True)
            msg_layout.add_widget(space)
        else:
            msg.radius = ["10dp", "10dp", "10dp", "0dp"]
            msg_layout = MDBoxLayout(adaptive_height= True)
            
            
        msg_layout.add_widget(msg)
        self.add_widget(msg_layout)

#// SCREENS

sm = ScreenManager()
user_list = []
LoggingIn = False

class Login(MDScreen):
    def change_screen(self, *args):
        self.manager.transition.direction = "left"
        self.manager.current= "Main"
        
    
    def on_enter(self):
        global LoggingIn
        
        GOOGLE_CLIENT_ID = "703603563897-liquhr64bcf21u17m0fme1ukdavfq0en.apps.googleusercontent.com"
        GOOGLE_CLIENT_SECRET = "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"
        initialize_google(
            self.after_login,
            self.error_listener,
            GOOGLE_CLIENT_ID,
            GOOGLE_CLIENT_SECRET,
        )
        if auto_login() and not LoggingIn:
                LoggingIn = True
                login_google()
            
        
        
    def after_login(self, name, email, photo_uri):
        print("details: ",name, email, photo_uri)
        self.user =  sign_up(name, photo_uri, email)
        user.email = email
        user.name = name
        user.uid = self.user.uid
        user.dp = photo_uri
        user.private_key = get_data(f"users/{user.uid}/private_key")
        user.public_key = get_data(f"users/{user.uid}/public_key")
        local_login(email)
        Clock.schedule_once(self.change_screen, 0.5)
    
    def error_listener(self):
        print("error")
        
    def login(self):
            login_google()

class Main(MDScreen):
    
    def on_enter(self, *args):
        layout = self.ids.grid
        self.add_users(layout)
    
    def change_screen(self, screen, receiver_name, receiver_uid, *args):
        receiver.name = receiver_name
        receiver.uid = receiver_uid
        receiver.public_key = get_data(f"users/{receiver_uid}/public_key")
        self.manager.current = screen
        
    def add_users(self, layout):
        
        for u in get_users():
            print(u.display_name)
            if user.uid != u.uid and  (u.uid not in user_list):
                user_list.append(u.uid)
                scrn_change = partial(self.change_screen, "Chat", u.display_name, u.uid)
                usercard = UserCard(u.display_name, u.photo_url)
                btn_layout = usercard.children[1]
                btn_layout.bind(on_release = scrn_change)
                btn_layout.id = u.uid
                layout.add_widget(usercard)

class Chat(MDScreen):
    
    def on_pre_enter(self):
        self.ids.chat_name.text = receiver.name
        self.listen(f"{user.uid}/messages/{receiver.uid}")
        self.load_chats()
        
    def send_msg(self, msg):
        print(translator.translate(msg))
        msg = str([msg, user.uid, datetime.now().strftime("%I:%M %p")])
        send(msg, receiver.public_key, receiver.uid, user.uid)
        send(msg, user.public_key, user.uid, receiver.uid)
        
    def load_chats(self):
        chat_layout = self.ids.chat_view
        path = f"{user.uid}/messages/{receiver.uid}"
        
        try:
            msgs = get_data(path)
            for msg in msgs:
                try:
                    msg = eval(msg)
                    msg = decrypt_msg(msg, user.private_key)
                    msg = eval(msg)
                    message = msg[0]
                    sender = (msg[1] == user.uid)
                    time = msg[2]
                    
                    chat_layout.create_chat(message, time, sender= sender)
                except Exception as error:
                    print("error:", error)
        except Exception as error:
                    print("error:", error)
            
    def listener(self, event):
        chat_layout = self.ids.chat_view
        
            
        if event.path != "/":
            try:
                msgs = eval(event.data)
                msgs = decrypt_msg(eval(event.data), user.private_key)
                msgs = eval(msgs)
                print(msgs)
                message = msgs[0]
                sender = (msgs[1] == user.uid)
                time = msgs[2]
                Clock.schedule_once(partial(chat_layout.create_chat, message, time, sender))
            except Exception as error:
                print("Error-", error)

    def listen(self, path):
        db.reference(path).listen(self.listener)
            
    def on_leave(self):
        chat_layout = self.ids.chat_view
        layout_children = chat_layout.children
        for i in range(0, len(layout_children)):
            chat_layout.remove_widget(layout_children[0])


#// Main App

class MainApp(MDApp):
    
    def build(self):
        sm.add_widget(Login(name = "Login"))
        sm.add_widget(Main(name = "Main"))
        sm.add_widget(Chat(name = "Chat"))
        from kivy.config import Config
        Config.set('graphics', 'text_context', 'pango')

        return sm
    
    def Android_back_click(self,window,key,*largs):

        if key == 27:

            if sm.current == 'Main' or sm.current == 'login':

                MainApp().stop()

            else:

                sm.current='Main'

            return True
    
    
    
    
app = MainApp()

app.run()