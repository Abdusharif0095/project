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


class ClientsScreen(MDScreen):
    def clear(self):
        self.ids["tf_fullname"].text = ""
        self.ids["tf_phone_num"].text = ""
        self.ids["tf_passport_num"].text = ""
        self.ids["tf_gender"].text = ""

    def delete(self):
        f = open("client.txt")
        lst = list(map(str, f.readline().split(';')))
        id = int(lst[0])
        f.close()

        query = "DELETE FROM Клиент WHERE id=%s;"
        values = [id]
        print(query, id)

        if get_data.delete(query, values):
            return 1
        else:
            return 0

    def save(self):
        fullname = self.ids["tf_fullname"]
        phone_num = self.ids["tf_phone_num"]
        passport_num = self.ids["tf_passport_num"]
        gender = self.ids["tf_gender"]
        result = True

        if not test.is_right_name(fullname.text):
            fullname.hint_text = "Не правильное ФИО"
            fullname.text = ""
            result = False

        if not test.is_right_phone_number(phone_num.text):
            phone_num.hint_text = "Формат: +7(777)777-77-77"
            phone_num.text = ""
            result = False

        if not (test.is_right_passport_num(passport_num.text)):
            passport_num.hint_text = "Только цифры"
            passport_num.text = ""
            result = False

        if not test.is_right_gender(gender.text):
            gender.hint_text = "м или ж"
            gender.text = ""
            result = False

        if not result:
            return False

        f = open("client.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        id = int(lst[0])

        query = "UPDATE Клиент SET ФИО=%s, Телефон=%s, НомерПаспорта=%s, Пол=%s WHERE id=%s"
        values = [fullname.text, phone_num.text, passport_num.text, gender.text, id]
        # print(query, values)
        get_data.update(query=query, values=values)
        return result

    def nothing(self):
        pass

    def get_fullname(self):
        f = open("client.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[1]

    def get_phone_num(self):
        f = open("client.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[2]

    def get_passport_num(self):
        f = open("client.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[3]

    def get_gender(self):
        f = open("client.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[4]


class WindowManager(ScreenManager):
    pass


class ClientApp(MDApp):
    def build(self):
        Window.size = (700, 500)
        self.theme_cls.theme_style = theme.theme_style
        self.theme_cls.primary_palette = theme.primary_palette
        return Builder.load_file("clients_edit_window.kv")


ClientApp().run()
