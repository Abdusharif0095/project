import get_data
import theme
import threading
import subprocess
import sys
import test
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatButton
from kivy.uix.screenmanager import ScreenManager
import autosalon


class InfoScreen(MDScreen):
    def get_username(self):
        f = open("user.txt")
        id = int(f.readline())
        f.close()
        query = "SELECT ФИО FROM Сотрудник WHERE id=%s"
        values = [id]
        data = get_data.get_data_vals(query, values)
        print(data[0][0])
        return str(data[0][0])

    def clear(self):
        self.ids["username"].text = ""
        self.ids["password"].text = ""

    def save(self):
        login = self.ids["username"]
        password = self.ids["password"]
        lg_text = login.text.strip()
        f = open("user.txt")
        id = int(f.readline())
        f.close()
        print(login.text, password.text)

        if lg_text == "":
            login.text=""
            login.hint_text = "Недопустимый логин"
            return False
        elif get_data.is_login_in_base(lg_text, id):
            self.ids["welcome_label"].text = self.get_username()+"\n\n Этот логин занят"
            return False

        if not test.is_right_password(password.text) or len(password.text) < 8:
            self.ids["welcome_label"].text = self.get_username() + "\n\n Пароль должен состоять из: \n а-я, \n А-Я, \n !@#$%&*, \n длина не < 8"
            return False
        else:
            get_data.save_log_pass(id, login.text, password.text)

        return True

    def nothing(self):
        pass


class WindowManager(ScreenManager):
    pass


class MyInfoApp(MDApp):
    def build(self):
        Window.size = (700, 500)
        self.theme_cls.theme_style = theme.theme_style
        self.theme_cls.primary_palette = theme.primary_palette
        return Builder.load_file("my_info.kv")


MyInfoApp().run()