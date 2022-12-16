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


class OrderScreen(MDScreen):
    def clear(self):
        self.ids["tf_client_fullname"].text = ""
        self.ids["tf_auto_id"].text = ""

    def save(self):
        cl_fullname = self.ids["tf_client_fullname"]
        auto_id = self.ids["tf_auto_id"]
        prepeymant = self.ids["tf_prepeymant"]
        label = self.ids["label"]

        result = True
        client_id = 0
        id_auto = 0
        prep = 0

        if not test.is_right_name(cl_fullname.text):
            result = False
            cl_fullname.hint_text = "Не правильное ФИО"
            cl_fullname.text = ""
        else:
            data = get_data.get_data_from_dt("select id, ФИО from Клиент;")
            for row in data:
                # print(*row)
                if row[1].lower() == cl_fullname.text.lower():
                    client_id = int(row[0])
            # print("=====================")

            if client_id == 0:
                cl_fullname.hint_text = "В базе нет такого клиента"
                cl_fullname.text = ""
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

        if not test.is_int(prepeymant.text):
            prepeymant.text = ""
            prepeymant.hint_text = "Формат: целое число > 0"
            result = False

        print(result)
        if not result:
            return result

        id = self.get_order_id()
        query = "SELECT * FROM Заказ;"
        data = get_data.get_data_from_dt(query)

        for row in data:
            if int(row[0]) == id:
                continue
            if client_id == row[1] and auto_id == row[3]:
                label.text = "Предзаказ \n\n Это запись уже существует!"
                return False

        idd = get_data.get_data_from_dt(query="SELECT MAX(id) FROM Заказ")
        if len(idd) == 0:
            label.text = "Предзаказ \n\n Перепроверьте данные"
        else:
            idd = int(idd[0][0]) + 1
            query = "INSERT INTO Заказ VALUES(%s, %s, %s, %s)"
            values = [idd, client_id, id_auto, int(prepeymant.text)]
            res = get_data.insert(query, values)
            print(query, values)
            if not res:
                label.text = "Предзаказ \n\n Перепроверьте данные"
                return False

        return True

    def nothing(self):
        print("nothing")

    def get_order_id(self):
        f = open("order.txt", "r")
        lst = list(map(str, f.readline().split(";")))
        f.close()
        return int(lst[0])


class WindowManager(ScreenManager):
    pass


class OrderApp(MDApp):
    def build(self):
        Window.size = (700, 500)
        self.theme_cls.theme_style = theme.theme_style
        self.theme_cls.primary_palette = theme.primary_palette
        return Builder.load_file("order_add_window.kv")


OrderApp().run()
