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


class AutoScreen(MDScreen):
    def clear(self):
        self.ids["tf_mark_id"].text = ""
        self.ids["tf_category"].text = ""
        self.ids["tf_year"].text = ""
        self.ids["tf_transmission"].text = ""
        self.ids["tf_mileage"].text = ""
        self.ids["tf_color"].text = ""
        self.ids["tf_fuel"].text = ""
        self.ids["tf_price"].text = ""
        self.ids["tf_count"].text = ""


    def delete(self):
        f = open("auto.txt")
        lst = list(map(str, f.readline().split(';')))
        id = int(lst[0])
        f.close()

        query = "DELETE FROM Автомобиль WHERE id=%s;"
        values = [id]
        print(query, id)

        if get_data.delete(query, values):
            return 1
        else:
            return 0

    def save(self):
        mark = self.ids["tf_mark_id"]
        category = self.ids["tf_category"]
        year = self.ids["tf_year"]
        transmission = self.ids["tf_transmission"]
        mileage = self.ids["tf_mileage"]
        color = self.ids["tf_color"]
        fuel = self.ids["tf_fuel"]
        price = self.ids["tf_price"]
        count = self.ids["tf_count"]
        label = self.ids["label"]

        if test.is_right_num(mark.text):
            query = "SELECT * FROM Марка WHERE id=%s;"
            values = [int(mark.text)]
            data = get_data.get_data_vals(query, values)

            if len(data) == 0:
                mark.text = ""
                mark.hint_text = "В базе данных нет такой марки"
                return 0
        else:
            return 0

        if not test.is_right_category(category.text):
            category.text = ""
            category.hint_text = "Неправильная категория"
            return 0

        if not test.is_right_year(year.text):
            year.text = ""
            year.hint_text = "Формат: гггг, >=2000"
            return 0

        if not test.is_right_transmission(transmission.text):
            transmission.text = ""
            return 0

        if not test.is_right_num(mileage.text):
            mileage.text = ""
            mileage.hint_text = "Формат: число >= 0"
            return 0

        if not test.is_right_num(fuel.text):
            fuel.text = ""
            fuel.hint_text = "Формат: число >= 0"
            return 0

        if not test.is_right_num(price.text):
            price.text = ""
            price.hint_text = "Формат: число >= 0"
            return 0

        if not test.is_right_num(count.text):
            count.text = ""
            count.hint_text = "Формат: число >= 0"
            return 0

        query = "SELCT * FROM Автомобиль WHERE idМарки=%s and Категория=%s and ГодВыпуска=%s and КаробкаПередач=%s and Пробег = %s and Цвет = %s and РасходТопливо = %s and Цена = %s and Количество = %s"
        values = [int(mark.text), category.text, int(year.text), transmission.text, int(mileage.text), color.text, int(fuel.text), int(price.text), int(count.text)]
        print(query, values)
        data = get_data.get_data_vals(query=query, vals=values)

        if len(data) != 0:
            label.text = "Такой автомобиль уже существует"

        else:
            id = get_data.get_next_id("SELECT MAX(id) FROM Автомобиль;")
            query = "INSERT INTO Автомобиль(id, idМарки, Категория, ГодВыпуска, КаробкаПередач, Пробег, Цвет, РасходТопливо, Цена, Количество) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            values = [id, int(mark.text), category.text, int(year.text), transmission.text, int(mileage.text), color.text,
                      int(fuel.text), int(price.text), int(count.text)]
            print(query, values)
            if get_data.insert(query, values):
                print("ok")
            else:
                label.text = "Что то пошло не так!"
                return 0

        return 1

    def nothing(self):
        pass

    def get_mark_id(self):
        f = open("auto.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[1]

    def get_category(self):
        f = open("auto.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[2]

    def get_year(self):
        f = open("auto.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[3]

    def get_transmission(self):
        f = open("auto.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[4]

    def get_mileage(self):
        f = open("auto.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[5]

    def get_color(self):
        f = open("auto.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[6]

    def get_fuel(self):
        f = open("auto.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[7]

    def get_price(self):
        f = open("auto.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[8]

    def get_count(self):
        f = open("auto.txt", "r")
        lst = list(map(str, f.readline().split(';')))
        f.close()
        return lst[9]


class WindowManager(ScreenManager):
    pass


class AutoApp(MDApp):
    def build(self):
        Window.size = (700, 500)
        self.theme_cls.theme_style = theme.theme_style
        self.theme_cls.primary_palette = theme.primary_palette
        return Builder.load_file("auto_add_window.kv")


AutoApp().run()
