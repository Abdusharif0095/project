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
        time = f"{hours//10}{hours%10}:{minutes//10}{minutes%10}:00"
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
        query = "DELETE FROM Тест WHERE id=%s"
        values = [self.get_test_id()]
        if get_data.delete(query, values):
            return 1
        else:
            self.ids["label"].text = "Тест \n\n Что то пошло не так!"

    def save(self):
        cl_fullname = self.ids["tf_client_fullname"]
        emp_fullname = self.ids["tf_emp_fullname"]
        auto_id = self.ids["tf_auto_id"]
        date = self.ids["tf_date"]
        time = self.ids["tf_time"]
        label = self.ids["label"]

        result = True
        client_id = 0
        employee_id = 0
        id_auto = 0
        cur_date = ""
        cur_time = ""

        if not test.is_right_name(cl_fullname.text):
            result = False
            cl_fullname.hint_text = "Не правильное ФИО"
            cl_fullname.text = ""
        else:
            data = get_data.get_data_from_dt("select id, ФИО from Клиент;")
            print(cl_fullname.text)
            for row in data:
                print(*row)
                if row[1].lower() == cl_fullname.text.lower():
                    client_id = int(row[0])
            print("=====================")
            if client_id == 0:
                cl_fullname.hint_text = "В базе нет такого клиента"
                cl_fullname.text = ""
                result = False

        if not test.is_right_name(emp_fullname.text):
            result = False
            emp_fullname.hint_text = "Не правильное ФИО"
            emp_fullname.text = ""
        else:
            data = get_data.get_data_from_dt("select id, ФИО from Сотрудник;")
            print(emp_fullname.text)
            for row in data:
                print(*row)
                if row[1].lower() == emp_fullname.text.lower():
                    employee_id = int(row[0])
            print("=====================")
            if employee_id == 0:
                emp_fullname.hint_text = "В базе нет такого сотрудника"
                emp_fullname.text = ""
                result = False

        if auto_id.text != "":
            id = int(auto_id.text)
            query = "select id from Автомобиль;"
            data = get_data.get_data_from_dt(query=query)
            flag = True
            for row in data:
                if id == int(row[0]):
                    id_auto = id
                    flag = False

            if flag:
                result = False
                auto_id.hint_text = "Такого авто нет в базе"
                auto_id.text = ""

        if not test.is_right_date(date.text):
            result = False
            date.hint_text = "Формат: гггг-мм-дд"
            date.text = ""
        else:
            cur_date = date.text

        if not test.is_right_time(time.text):
            result = False
            time.hint_text = "Формат: чч:мм:сс"
            time.text = ""
        else:
            cur_time = time.text

        print(result)
        if not result:
            return result
            
        id = self.get_test_id()
        query = "SELECT * FROM Тест;"
        data = get_data.get_data_from_dt(query)

        for row in data:
            if int(row[0]) == id:
                continue
            if client_id == row[1] and cur_date == row[5] and cur_time == row[4] and employee_id == row[2] and auto_id == row[3]:
                label.text = "Тест \n\n Это запись уже существует!"
                return False

        query = "SELECT * FROM Тест WHERE idСотрудника=%s AND Дата=%s AND Время=%s AND id<>%s;"
        values = [employee_id, cur_date, cur_time, id]
        data1 = get_data.get_data_vals(query, values)

        if len(data1) != 0:
            label.text = "Тест \n\n Этот сотрудник занят в выбранное время"
            return False

        query = "SELECT * FROM Тест WHERE idКлиента=%s AND Дата=%s AND Время=%s AND id<>%s;"
        values = [employee_id, cur_date, cur_time, id]
        data1 = get_data.get_data_vals(query, values)

        if len(data1) != 0:
            label.text = "Тест \n\n Этот клиент уже записан в выбранное время"
            return False

        query = "UPDATE Тест SET idКлиента=%s, idСотрудника=%s, idАвтомобиля=%s,  Дата=%s, Время=%s WHERE id=%s"
        values = [client_id, employee_id, id_auto, cur_date, cur_time, id]
        get_data.update(query, values)
        print(query, values)

        return True

    def nothing(self):
        print("nothing")

    def get_test_id(self):
        f = open("test.txt", "r")
        lst = list(map(str, f.readline().split(";")))
        f.close()
        return int(lst[0])

    def get_client_fullname(self):
        f = open("test.txt", "r")
        lst = list(map(str, f.readline().split(";")))
        f.close()
        return lst[1]

    def get_emp_fullname(self):
        f = open("test.txt", "r")
        lst = list(map(str, f.readline().split(";")))
        f.close()
        return lst[2]

    def get_auto_id(self):
        f = open("test.txt", "r")
        lst = list(map(str, f.readline().split(";")))
        f.close()
        return lst[3]

    def get_date(self):
        f = open("test.txt", "r")
        lst = list(map(str, f.readline().split(";")))
        f.close()
        return lst[4]

    def get_time(self):
        f = open("test.txt", "r")
        lst = list(map(str, f.readline().split(";")))
        f.close()
        return lst[5]


class WindowManager(ScreenManager):
    pass


class TestApp(MDApp):
    def build(self):
        Window.size = (700, 500)
        self.theme_cls.theme_style = theme.theme_style
        self.theme_cls.primary_palette = theme.primary_palette
        return Builder.load_file("test_edit_window.kv")


TestApp().run()
