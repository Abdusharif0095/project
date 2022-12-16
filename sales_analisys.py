import get_data
import theme
import threading
import subprocess
import sys
import test
import matplotlib.pyplot as plt
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
import get_data


class AnalisysScreen(MDScreen):
    def build(self):
        self.clear()

    def clear_analyses(self):
        files = ["emp.txt", "emp_time.txt", "auto_id.txt", "auto_time.txt"]
        for file in files:
            f = open(file, "w")
            f.close()

    def get_emps(self):
        query = "SELECT ФИО FROM Сотрудник WHERE Должность='продовец-консультант';"
        data = get_data.get_data_from_dt(query)
        emps = ["Все"]

        for row in data:
            emps.append(row[0])

        return emps

    def get_auto_ids(self):
        query = "SELECT id FROM Автомобиль;"
        data = get_data.get_data_from_dt(query)
        ids = ["Все"]

        for row in data:
            ids.append(str(row[0]))

        ids.sort()

        return ids

    def emp_press_spinner(self, value):
        f = open("emp.txt", "w")
        f.write(value.text)
        f.close()

    def auto_id_press_spinner(self, value):
        f = open("auto.txt", "w")
        f.write(value.text)
        f.close()

    def emp_time_press_spinner(self, value):
        f = open("emp_time.txt", "w")
        f.write(value.text)
        f.close()

    def auto_time_press_spinner(self, value):
        f = open("auto_time.txt", "w")
        f.write(value.text)
        f.close()

    def get_emp_count(self, query, vals):
        res = get_data.get_data_vals(query, vals)
        try:
            return int(res[0][0])
        except Exception as e:
            print(f"Error: {e}")
            return 0

    def emp_button(self):
        f = open("emp.txt")
        emp = f.readline()
        f.close()

        f = open("emp_time.txt")
        emp_time = f.readline()
        f.close()

        if emp == "Все":
            if emp_time == "за всё время":
                emps = self.get_emps()[1:]
                query="select COUNT(*) from Продажа JOIN Сотрудник ON Продажа.idСотрудника=Сотрудник.id where Сотрудник.ФИО=%s;"
                y_list = [self.get_emp_count(query, [emp]) for emp in emps]
                print(y_list)
                print(emps)

                plt.title("Продажи")
                plt.xlabel("Сотрудник")
                plt.ylabel("Кол-во продаж")

                plt.bar(emps, y_list, width=0.1)
                plt.show()


class WindowManager(ScreenManager):
    pass


class AnalisysApp(MDApp):
    def build(self):
        Window.size = (700, 500)
        self.theme_cls.theme_style = theme.theme_style
        self.theme_cls.primary_palette = theme.primary_palette
        return Builder.load_file("sales_analisys.kv")


AnalisysApp().run()
