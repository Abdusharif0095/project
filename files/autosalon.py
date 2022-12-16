from kivymd.app import MDApp
from kivy.lang import Builder


"""
class Test(MDApp):
    def build(self):
        return Builder.load_file("login.kv")
"""


class Autosalon(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('autosalon.kv')


Autosalon().run()
