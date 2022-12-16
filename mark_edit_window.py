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

    def delete(self):
        query = "DELETE FROM Марка WHERE id=%s"
        values = [self.get_mark_id()]
        if get_data.delete(query, values):
            return 1
        else:
            self.ids["label"].text = "Марка \n\n Что то пошло не так!"

    def save(self):
        tf_model = self.ids["tf_model"]
        tf_class = self.ids["tf_class"]

        query = "UPDATE Марка SET Модель=%s, Класс=%s WHERE id=%s"
        values = [tf_model.text, tf_class.text, self.get_mark_id()]
        get_data.update(query, values)
        print(query, values)

        return True

    def nothing(self):
        print("nothing")

    def get_mark_id(self):
        f = open("mark.txt", "r")
        lst = list(map(str, f.readline().split(";")))
        f.close()
        return int(lst[0])

    def get_model(self):
        f = open("mark.txt", "r")
        lst = list(map(str, f.readline().split(";")))
        f.close()
        return lst[1]

    def get_class(self):
        f = open("mark.txt", "r")
        lst = list(map(str, f.readline().split(";")))
        f.close()
        return lst[2]


class WindowManager(ScreenManager):
    pass


class MarkApp(MDApp):
    def build(self):
        Window.size = (700, 500)
        self.theme_cls.theme_style = theme.theme_style
        self.theme_cls.primary_palette = theme.primary_palette
        return Builder.load_file("mark_edit_window.kv")


MarkApp().run()
