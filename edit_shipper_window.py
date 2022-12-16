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


class ShipperScreen(MDScreen):
    def clear(self):
        self.ids["tf_fullname"].text = ""
        self.ids["tf_phone_num"].text = ""

    def delete(self):
        f = open("shipper.txt")
        lst = list(map(str, f.readline().split(';')))
        id = int(lst[0])
        f.close()

        query = "DELETE FROM Поставщик WHERE id=%s;"
        values = [id]
        print(query, id)

        if get_data.delete(query, values):
            return 1
        else:
            return 0

    def save(self):
        fullname = self.ids["tf_fullname"]
        phone_num = self.ids["tf_phone_num"]
        result = True

        if not test.is_right_name(fullname.text):
            fullname.hint_text = "Не правильное Название"
            fullname.text = ""
            result = False

        if not test.is_right_phone_number(phone_num.text):
            phone_num.hint_text = "Формат: +7(777)777-77-77"
            phone_num.text = ""
            result = False
        else:
            vals = [phone_num.text]
            data = get_data.get_data_vals("SELECT * FROM Поставщик WHERE Телефон=%s", vals)
            if len(data) != 0:
                phone_num.text = ""
                phone_num.hint_text = "Этот тел. уже существует!"
                return False


        if not result:
            return False

        f = open("shipper.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        id = int(lst[0])

        query = "UPDATE Поставщик SET Название=%s, Телефон=%s WHERE id=%s"
        values = [fullname.text, phone_num.text, id]
        print(query, values)
        get_data.update(query=query, values=values)
        return result

    def nothing(self):
        pass

    def get_fullname(self):
        f = open("shipper.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[1]

    def get_phone_num(self):
        f = open("shipper.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[2]


class WindowManager(ScreenManager):
    pass


class ShipperApp(MDApp):
    def build(self):
        Window.size = (700, 500)
        self.theme_cls.theme_style = theme.theme_style
        self.theme_cls.primary_palette = theme.primary_palette
        return Builder.load_file("edit_shipper_window.kv")


ShipperApp().run()
