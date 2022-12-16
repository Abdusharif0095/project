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


class EmployeeScreen(MDScreen):
    def clear(self):
        self.ids["tf_fullname"].text = ""
        self.ids["tf_phone_num"].text = ""
        self.ids["tf_position"].text = ""
        self.ids["tf_birth_day"].text = ""
        self.ids["tf_gender"].text = ""

    def delete(self):
        f = open("employee.txt")
        lst = list(map(str, f.readline().split(';')))
        id = int(lst[0])
        f.close()

        query = "DELETE FROM Сотрудник WHERE id=%s;"
        values = [id]
        print(query, id)

        if get_data.delete(query, values):
            return 1
        else:
            return 0

    def save(self):
        fullname = self.ids["tf_fullname"]
        phone_num = self.ids["tf_phone_num"]
        position = self.ids["tf_position"]
        birth_day = self.ids["tf_birth_day"]
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

        if not (test.is_right_position(position.text)):
            position.hint_text = "Не правильная Должность"
            position.text = ""
            result = False

        if not (test.is_right_birth_day(birth_day.text)):
            birth_day.text = ""
            birth_day.hint_text = "Формат: гггг-мм-дд, < 65 год"
            return False

        if not test.is_right_gender(gender.text):
            gender.hint_text = "м или ж"
            gender.text = ""
            result = False

        if not result:
            return False

        f = open("employee.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        id = int(lst[0])

        query = "UPDATE Сотрудник SET ФИО=%s, Телефон=%s, Должность=%s, ДатаРождения=%s, Пол=%s WHERE id=%s"
        values = [fullname.text, phone_num.text, position.text, birth_day.text, gender.text, id]
        print(query, values)
        if get_data.update(query=query, values=values):
            return True
        else:
            return False
        return result

    def nothing(self):
        pass

    def get_fullname(self):
        f = open("employee.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[1]

    def get_phone_num(self):
        f = open("employee.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[2]

    def get_position(self):
        f = open("employee.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[3]

    def get_birth_day(self):
        f = open("employee.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[4]

    def get_gender(self):
        f = open("employee.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[5]


class WindowManager(ScreenManager):
    pass


class EmployeeApp(MDApp):
    def build(self):
        Window.size = (700, 500)
        self.theme_cls.theme_style = theme.theme_style
        self.theme_cls.primary_palette = theme.primary_palette
        return Builder.load_file("edit_employees_window.kv")


EmployeeApp().run()
