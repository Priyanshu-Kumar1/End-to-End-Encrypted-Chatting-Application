from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.screen import MDScreen

class Main(MDScreen):
    
    def change_screen(self, screen, *args):
        self.manager.current = screen
        
    def add_users(self, layout):
        for k , v in users.items():
            scrn_change = partial(self.change_screen, "Login")
            usercard = UserCard(k, f"assets/images/users/{v}")
            btn_layout = usercard.children[1]
            btn_layout.bind(on_release = scrn_change)
            layout.add_widget(usercard)
