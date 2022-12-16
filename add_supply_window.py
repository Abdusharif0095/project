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


class SupplyScreen(MDScreen):
    def clear(self):
        self.ids["tf_fullname"].text = ""
        self.ids["tf_auto_id"].text = ""
        self.ids["tf_count"].text = ""
        self.ids["tf_date"].text = ""

    def on_save(self, instance, value, date_range):
        self.ids["tf_date"].text = str(value)

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def delete(self):
        query = "DELETE FROM Поставка1 WHERE id=%s"
        values = [self.get_sale_id()]
        if get_data.delete(query, values):
            return 1
        else:
            self.ids["label"].text = "Поставка \n\n Что то пошло не так!"

    def make(self):
        query = "UPDATE Автомобиль SET Количество=Количество+%s WHERE id=%s"
        vals = [int(self.get_count()), self.get_supply_id()]
        if not get_data.update(query, vals):
            self.ids["label"].text = "Поставка \n\n Перепроверьте данные"

    def save(self):
        cl_fullname = self.ids["tf_fullname"]
        auto_id = self.ids["tf_auto_id"]
        count = self.ids["tf_count"]
        date = self.ids["tf_date"]
        label = self.ids["label"]

        result = True
        client_id = 0
        id_auto = 0
        cur_date = ""

        if not test.is_right_name(cl_fullname.text):
            result = False
            cl_fullname.hint_text = "Не правильное Название"
            cl_fullname.text = ""
        else:
            shipper_id, ress = get_data.is_shipper_in_base(cl_fullname.text)
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

        if not test.is_right_num(count.text):
            count.text = ""
            count.hint_text = "Количесьво > 0"
            return False

        if not test.is_right_date(date.text):
            result = False
            date.hint_text = "Формат: гггг-мм-дд"
            date.text = ""
        else:
            cur_date = date.text

        print(result)
        if not result:
            return result

        id = get_data.get_next_id("SELECT MAX(id) FROM Поставка1;")

        query = "INSERT INTO Поставка1 VALUES(%s, %s, %s, %s, %s)"
        values = [id, shipper_id, id_auto, int(count.text), cur_date]
        if get_data.insert(query, values):
            return 1
        else:
            self.ids["label"].text = "Поставка \n\n Перепроверьте данные!"
        print(query, values)

        return True

    def nothing(self):
        print("nothing")

    def get_supply_id(self):
        f = open("supply.txt", "r")
        lst = list(map(str, f.readline().split(";")))
        f.close()
        return int(lst[0])


class WindowManager(ScreenManager):
    pass


class SupplyApp(MDApp):
    def build(self):
        Window.size = (700, 500)
        self.theme_cls.theme_style = theme.theme_style
        self.theme_cls.primary_palette = theme.primary_palette
        return Builder.load_file("add_supply_window.kv")


SupplyApp().run()
