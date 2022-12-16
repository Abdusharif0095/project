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
from kivymd.uix.pickers import MDDatePicker, MDTimePicker


class TestScreen(MDScreen):
    def clear(self):
        self.ids["tf_client_fullname"].text = ""
        self.ids["tf_emp_fullname"].text = ""
        self.ids["tf_auto_id"].text = ""
        self.ids["tf_date"].text = ""

    def on_save(self, instance, value, date_range):
        self.ids["tf_date"].text = str(value)

    def on_time_save(self, instance, value):
        lst = list(map(str, str(value).split(":")))
        hours = int(lst[0]) + 12 * (instance.am_pm == "pm")
        minutes = int(lst[1])
        time = f"{hours // 10}{hours % 10}:{minutes // 10}{minutes % 10}:00"
        self.ids["tf_time"].text = str(time)

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.on_time_save)
        time_dialog.open()

    def delete(self):
        query = "DELETE FROM Продажа WHERE id=%s"
        values = [self.get_sale_id()]
        if get_data.delete(query, values):
            return 1
        else:
            self.ids["label"].text = "Продажа \n\n Что то пошло не так!"

    def save(self):
        cl_fullname = self.ids["tf_client_fullname"]
        auto_id = self.ids["tf_auto_id"]
        date = self.ids["tf_date"]
        label = self.ids["label"]

        result = True
        client_id = 0
        id_auto = 0
        cur_date = ""

        if not test.is_right_name(cl_fullname.text):
            result = False
            cl_fullname.hint_text = "Не правильное ФИО"
            cl_fullname.text = ""
        else:
            client_id, ress = get_data.is_client_in_base(cl_fullname.text)
            if not ress:
                cl_fullname.text=""
                cl_fullname.hint_text="В базе данных нет такого клиента"
                return False

        if auto_id.text != "":
            flag = get_data.is_auto_in_base(int(auto_id.text))
            if not flag:
                result = False
                auto_id.hint_text = "Такого авто нет в базе данных"
                auto_id.text = ""
            else:
                id_auto = int(auto_id.text)

        if not test.is_right_date(date.text):
            result = False
            date.hint_text = "Формат: гггг-мм-дд"
            date.text = ""
        else:
            cur_date = date.text

        print(result)
        if not result:
            return result

        query="SELECT MAX(id) FROM Продажа;"
        id = get_data.get_next_id(query)

        query = "INSERT INTO Продажа VALUES(%s, %s, %s, %s, %s)"
        f = open("user.txt", "r")
        emp_id = int(f.readline())
        f.close()
        values = [id, emp_id, client_id, id_auto, cur_date]
        ress = get_data.fix_soled_auto(id_auto)
        if ress:
            get_data.insert(query, values)
            print(query, values)
            return True
        else:
            auto_id.hint_text="Такого авто сейчас нет"
            auto_id.text = ""

    def nothing(self):
        print("nothing")


class WindowManager(ScreenManager):
    pass


class SalesApp(MDApp):
    def build(self):
        Window.size = (700, 500)
        self.theme_cls.theme_style = theme.theme_style
        self.theme_cls.primary_palette = theme.primary_palette
        return Builder.load_file("sales_add_window.kv")


SalesApp().run()
