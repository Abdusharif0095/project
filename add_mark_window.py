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


class MarkScreen(MDScreen):
    def clear(self):
        self.ids["tf_model"].text = ""
        self.ids["tf_class"].text = ""

    def save(self):
        tf_model = self.ids["tf_model"]
        tf_class = self.ids["tf_class"]

        query = "SELECT * FROM Марка WHERE Модель=%s and Класс=%s;"
        values = [tf_model.text, tf_class.text]
        data = get_data.get_data_vals(query, values)

        if len(data) != 0:
            self.ids["label"].text = "Марка \n\n Такая запись уже существует!"
            return False
        else:
            idd = get_data.get_next_id("SELECT MAX(id) FROM Марка;")
            query = "INSERT INTO Марка VALUES(%s, %s, %s)"
            values = [idd, tf_model.text, tf_class.text]
            get_data.insert(query, values)

        return True

    def nothing(self):
        print("nothing")


class WindowManager(ScreenManager):
    pass


class MarkApp(MDApp):
    def build(self):
        Window.size = (700, 500)
        self.theme_cls.theme_style = theme.theme_style
        self.theme_cls.primary_palette = theme.primary_palette
        return Builder.load_file("add_mark_window.kv")


MarkApp().run()
