import test
import theme
import threading
import os
import time
import subprocess
import sys
from threading import Thread
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.core.window import Window
import get_data
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.button import MDIconButton
from kivy.uix.spinner import Spinner


class HomeWindow(Screen):
    pass


class LoginWindow(MDScreen):
    pass


class SalesWindow(Screen):
    def clear_cfs(self, instance):
        label_id = self.ids["tf_id"]
        label_id.text = ""
        label_model = self.ids["tf_model"]
        label_model.text = ""
        label_class = self.ids["tf_class"]
        label_class.text = ""
        label_category = self.ids["tf_category"]
        label_category.text = ""
        label_color = self.ids["tf_color"]
        label_color.text = ""

    def search_cfs(self, instance):
        s_id = self.ids["tf_id"].text
        s_model = self.ids["tf_model"].text
        s_class = self.ids["tf_class"].text
        s_category = self.ids["tf_category"].text
        s_color = self.ids["tf_color"].text
        query="SELECT Автомобиль.id, Марка.Модель, Марка.Класс, Автомобиль.Категория, Автомобиль.Цвет, Автомобиль.Количество FROM Марка JOIN Автомобиль ON Марка.id=Автомобиль.idМарки WHERE Автомобиль.Количество > 0"

        vals = []

        if s_id.isdigit():
            query += " AND Автомобиль.id = %s"
            vals.append(s_id)

        if s_model != "":
            query += " AND Марка.Модель = %s"
            vals.append(s_model.lower())

        if s_class != "":
            query += " AND Марка.Класс = %s"
            vals.append(s_class.lower())

        if s_category != "":
            query += " AND Автомобиль.Категория = %s"
            vals.append(s_category.lower())

        if s_color != "":
            query += " AND Автомобиль.Цвет = %s"
            vals.append(s_color.lower())

        query += "ORDER BY Автомобиль.id;"

        data, data_col = get_data.get_data_vals(query=query, vals=vals, get_col_names=True)
        print(data)

        data_table = self.ids["data_table"]
        data_table.column_data = [(col, dp(30)) for col in data_col]
        data_table.row_data = [(row[0], row[1], row[2], row[3], row[4], row[5], ) for row in data]+[("", "", "", "", "", "")]

    def search_cic(self, instance):
        s_id = self.ids["tf_id"].text
        s_model = self.ids["tf_model"].text
        s_class = self.ids["tf_class"].text
        s_category = self.ids["tf_category"].text
        s_color = self.ids["tf_color"].text
        query="SELECT Автомобиль.id, Марка.Модель, Марка.Класс, Автомобиль.Категория, Автомобиль.Цвет, Автомобиль.Количество FROM Марка JOIN Автомобиль ON Марка.id=Автомобиль.idМарки WHERE Марка.id=Марка.id"

        vals = []

        if s_id.isdigit():
            query += " AND Автомобиль.id = %s"
            vals.append(s_id)

        if s_model != "":
            query += " AND Марка.Модель = %s"
            vals.append(s_model.lower())

        if s_class != "":
            query += " AND Марка.Класс = %s"
            vals.append(s_class.lower())

        if s_category != "":
            query += " AND Автомобиль.Категория = %s"
            vals.append(s_category.lower())

        if s_color != "":
            query += " AND Автомобиль.Цвет = %s"
            vals.append(s_color.lower())

        query += "  BY Автомобиль.id;"

        data, data_col = get_data.get_data_vals(query=query, vals=vals, get_col_names=True)

        data_table = self.ids["data_table"]
        data_table.column_data = [(col, dp(30)) for col in data_col]
        data_table.row_data = [(row[0], row[1], row[2], row[3], row[4], row[5], ) for row in data]+[("", "", "", "", "", "")]

    def cars_for_sale(self):
        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data, data_col = get_data.get_data_from_dt(
            query="SELECT Автомобиль.id, Марка.Модель, Марка.Класс, Автомобиль.Категория, Автомобиль.Цвет, Автомобиль.Количество FROM Марка JOIN Автомобиль ON Марка.id=Автомобиль.idМарки WHERE Автомобиль.Количество > 0 ORDER BY Автомобиль.id;",
            get_col_names=True)
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                (col, dp(30)) for col in data_col
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_id = MDTextField(
            id="id",
            mode="round",
            hint_text="id",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_id"] = tf_id
        card.add_widget(tf_id)
        tf_model = MDTextField(
            id="model",
            mode="round",
            hint_text="Модель",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_model"] = tf_model
        card.add_widget(tf_model)
        tf_class = MDTextField(
            id="class",
            mode="round",
            hint_text="Класс",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_class"] = tf_class
        card.add_widget(tf_class)
        tf_category = MDTextField(
            id="category",
            mode="round",
            hint_text="Категория",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_category"] = tf_category
        card.add_widget(tf_category)
        tf_color = MDTextField(
            id="color",
            mode="round",
            hint_text="Цвет",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_color"] = tf_color
        card.add_widget(tf_color)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_cfs)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.clear_cfs)
        card.add_widget(clear_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=0.4,
            )
        )
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def cars_in_catalog(self):

        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data, data_col = get_data.get_data_from_dt(
            query="SELECT Автомобиль.id, Марка.Модель, Марка.Класс, Автомобиль.Категория, Автомобиль.Цвет, Автомобиль.Количество FROM Марка JOIN Автомобиль ON Марка.id=Автомобиль.idМарки ORDER BY Автомобиль.id;",
            get_col_names=True)
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                (col, dp(30)) for col in data_col
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_id = MDTextField(
            id="id",
            mode="round",
            hint_text="id",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_id"] = tf_id
        card.add_widget(tf_id)
        tf_model = MDTextField(
            id="model",
            mode="round",
            hint_text="Модель",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_model"] = tf_model
        card.add_widget(tf_model)
        tf_class = MDTextField(
            id="class",
            mode="round",
            hint_text="Класс",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_class"] = tf_class
        card.add_widget(tf_class)
        tf_category = MDTextField(
            id="category",
            mode="round",
            hint_text="Категория",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_category"] = tf_category
        card.add_widget(tf_category)
        tf_color = MDTextField(
            id="color",
            mode="round",
            hint_text="Цвет",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_color"] = tf_color
        card.add_widget(tf_color)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_cic)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.clear_cfs)
        card.add_widget(clear_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=0.4,
            )
        )
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def search_cic(self, instance):
        s_id = self.ids["tf_id"].text
        s_model = self.ids["tf_model"].text
        s_class = self.ids["tf_class"].text
        s_category = self.ids["tf_category"].text
        s_color = self.ids["tf_color"].text
        query="SELECT Автомобиль.id, Марка.Модель, Марка.Класс, Автомобиль.Категория, Автомобиль.Цвет, Автомобиль.Количество FROM Марка JOIN Автомобиль ON Марка.id=Автомобиль.idМарки WHERE Марка.id=Марка.id"

        vals = []

        if s_id.isdigit():
            query += " AND Автомобиль.id = %s"
            vals.append(s_id)

        if s_model != "":
            query += " AND Марка.Модель = %s"
            vals.append(s_model.lower())

        if s_class != "":
            query += " AND Марка.Класс = %s"
            vals.append(s_class.lower())

        if s_category != "":
            query += " AND Автомобиль.Категория = %s"
            vals.append(s_category.lower())

        if s_color != "":
            query += " AND Автомобиль.Цвет = %s"
            vals.append(s_color.lower())

        query += " ORDER BY Автомобиль.id;"

        data, data_col = get_data.get_data_vals(query=query, vals=vals, get_col_names=True)

        data_table = self.ids["data_table"]
        data_table.column_data = [(col, dp(30)) for col in data_col]
        data_table.row_data = [(row[0], row[1], row[2], row[3], row[4], row[5], ) for row in data]+[("", "", "", "", "", "")]

    def search_drivers(self, instance):
        s_fullname = self.ids["tf_fullname"].text
        s_gender = self.ids["tf_gender"].text
        query="SELECT ФИО, Телефон, ДатаРождения, Пол FROM Сотрудник WHERE Должность='водитель'"

        vals = []

        if s_gender != "":
            query += " AND Пол = %s"
            vals.append(s_gender.lower())

        data, data_col = get_data.get_data_vals(query=query, vals=vals, get_col_names=True)

        data1 = []

        if s_fullname != "":
            for row in data:
                if s_fullname.lower() in row[0].lower():
                    data1.append(row)
            data = data1

        data_table = self.ids["data_table"]
        data_table.column_data = [(col, dp(30)) for col in data_col]
        data_table.row_data = [tuple(row) for row in data]+[("", "", "", "",)]

    def search_clients(self, instance):
        s_fullname = self.ids["tf_fullname"].text
        s_passport_num = self.ids["tf_passport_num"].text
        s_phone_num = self.ids["tf_phone_num"].text
        s_gender = self.ids["tf_gender"].text
        query="SELECT ФИО, Телефон, НомерПаспорта, Пол FROM Клиент WHERE ФИО=ФИО"

        vals = []

        if s_gender != "":
            query += " AND Пол = %s"
            vals.append(s_gender.lower())

        if s_phone_num != "":
            query += " AND Телефон = %s"
            vals.append(s_phone_num.lower())

        if s_passport_num != "":
            query += " AND НомерПаспорта = %s"
            vals.append(s_passport_num.lower())

        data, data_col = get_data.get_data_vals(query=query, vals=vals, get_col_names=True)

        data1 = []

        if s_fullname != "":
            for row in data:
                if s_fullname.lower() in row[0].lower():
                    data1.append(row)
            data = data1

        data_table = self.ids["data_table"]
        data_table.column_data = [(col, dp(30)) for col in data_col]
        data_table.row_data = [tuple(row) for row in data]+[("", "", "", "",)]

    def clear_drivers(self, instance):
        self.ids["tf_fullname"].text = ""
        self.ids["tf_gender"].text = ""

    def cleaer_clients(self, instance):
        self.ids["tf_fullname"].text = ""
        self.ids["tf_gender"].text = ""
        self.ids["tf_phone_num"].text = ""
        self.ids["tf_passport_num"].text = ""

    def drivers(self, instance):
        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data, data_col = get_data.get_data_from_dt(query="SELECT ФИО, Телефон, ДатаРождения, Пол FROM Сотрудник WHERE Должность='водитель'", get_col_names=True)
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                ("ФИО", dp(70)),
                ("Телефон", dp(40)),
                ("ДатаРождения", dp(50)),
                ("Пол", dp(40)),
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_fullname = MDTextField(
            id="tf_fullname",
            mode="round",
            hint_text="ФИО",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_fullname"] = tf_fullname
        card.add_widget(tf_fullname)
        tf_gender = MDTextField(
            id="tf_gender",
            mode="round",
            hint_text="м или ж",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_gender"] = tf_gender
        card.add_widget(tf_gender)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_drivers)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.clear_drivers)
        card.add_widget(clear_button)
        card.add_widget(MDLabel())
        card.add_widget(MDLabel())
        self.ids["card"] = card
        search_layout.add_widget(card)
        n_layout = BoxLayout(
            size_hint_y=0.5,
        )
        # search_layout.add_widget(n_layout)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def clients_update(self):
        data = get_data.get_data_from_dt(query="SELECT ФИО, Телефон, НомерПаспорта, Пол FROM Клиент ORDER BY id;")
        self.ids["data_table"].row_data = [tuple(row) for row in data]

    def add_client_row(self, instance):
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "clients_add_window.py"]))
        th1.start()
        th1.join()
        self.clients_update()

    def clients(self):
        def on_check_press(instance, row_data):
            print(row_data)
            data = get_data.get_data_vals("SELECT id FROM Клиент WHERE ФИО=%s AND Телефон=%s AND НомерПаспорта=%s AND Пол=%s;", row_data)

            id = str(data[0][0])

            f = open("client.txt", "w")
            f.write(id+";")
            for i in range(len(row_data)):
                f.write(row_data[i]+';')
            f.close()

            th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "clients_edit_window.py"]))
            th1.start()
            th1.join()
            self.clients_update()

        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data = get_data.get_data_from_dt(query="SELECT ФИО, Телефон, НомерПаспорта, Пол FROM Клиент GROUP BY id;")
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                ("ФИО", dp(70)),
                ("Телефон", dp(40)),
                ("НомерПаспорта", dp(50)),
                ("Пол", dp(40)),
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )

        data_table.bind(on_check_press=on_check_press)
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_fullname = MDTextField(
            id="tf_fullname",
            mode="round",
            hint_text="ФИО",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_fullname"] = tf_fullname
        card.add_widget(tf_fullname)
        tf_phone_num = MDTextField(
            id="tf_phone_num",
            mode="round",
            hint_text="+7(777)777-77-77",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_phone_num"] = tf_phone_num
        card.add_widget(tf_phone_num)
        tf_passport_num = MDTextField(
            id="tf_passport_num",
            mode="round",
            hint_text="0123456789",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_passport_num"] = tf_passport_num
        card.add_widget(tf_passport_num)
        tf_gender = MDTextField(
            id="tf_gender",
            mode="round",
            hint_text="м или ж",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_gender"] = tf_gender
        card.add_widget(tf_gender)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_clients)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.cleaer_clients)
        card.add_widget(clear_button)
        add_button = MDRaisedButton(
            text="Добавить клиента",
            pos_hint={"center_x": 0.5},
        )
        add_button.bind(on_press=self.add_client_row)
        card.add_widget(add_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=0.4,
            )
        )
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def on_save(self, instance, value, date_range):
        self.ids["tf_date"].text = str(value)

    def show_date_picker(self, instance):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def clear_test(self, instance):
        self.ids["tf_client_fullname"].text = ""
        self.ids["tf_emp_fullname"].text = ""
        self.ids["tf_auto_id"].text = ""
        self.ids["tf_date"].text = ""

    def search_test(self, instance):
        cl_fullname = self.ids["tf_client_fullname"].text
        emp_fullname = self.ids["tf_emp_fullname"].text
        auto_id = self.ids["tf_auto_id"].text
        date = self.ids["tf_date"].text

        values = []
        query = f"select Клиент.ФИО AS Клиент, Сотрудник.ФИО AS Сотрудник, Автомобиль.id as idAuto, Тест.Дата, Тест.Время from Тест join Клиент on Тест.idКлиента=Клиент.id join Сотрудник on Тест.idСотрудника=Сотрудник.id join Автомобиль on Автомобиль.id=Тест.idАвтомобиля where Дата >= '{time.strftime('%Y-%m-%d', time.gmtime())}'"

        if auto_id != "":
            query += "and Автомобиль.id = %s"
            values.append(int(auto_id))

        if date != "":
            query += "and Тест.Дата = %s"
            values.append(date)

        query += " order by Дата, Время;"
        data = get_data.get_data_vals(query, values)

        if cl_fullname != "":
            data1 = []
            for row in data:
                if cl_fullname.lower() in row[0].lower():
                    data1.append(row)
            data = data1

        if emp_fullname != "":
            data1 = []
            for row in data:
                if emp_fullname.lower() in row[1].lower():
                    data1.append(row)
            data = data1

        self.ids["data_table"].row_data = [tuple(row) for row in data] + [("", "", "", "", "")]

    def test_update(self):
        data = get_data.get_data_from_dt(
            query=f"select Клиент.ФИО AS Клиент, Сотрудник.ФИО AS Сотрудник, Автомобиль.id as idAuto, Тест.Дата, Тест.Время from Тест join Клиент on Тест.idКлиента=Клиент.id join Сотрудник on Тест.idСотрудника=Сотрудник.id join Автомобиль on Автомобиль.id=Тест.idАвтомобиля where Дата >= '{time.strftime('%Y-%m-%d', time.gmtime())}' order by Дата, Время;",
            get_col_names=False)
        self.ids["data_table"].row_data = [tuple(row) for row in data]

    def clear_order(self, instance):
        self.ids["tf_client_fullname"].text = ""
        self.ids["tf_auto_id"].text = ""

    def search_order(self, instance):
        cl_fullname = self.ids["tf_client_fullname"].text
        auto_id = self.ids["tf_auto_id"].text

        values = []
        query = f"SELECT Клиент.ФИО AS ФИОКлиента, Заказ.idАвтомобиля, Заказ.Предоплата FROM Заказ JOIN Клиент ON Клиент.id=Заказ.idКлиента"

        if auto_id != "":
            query += " and Заказ.idАвтомобиля = %s"
            values.append(int(auto_id))

        print(query, values)
        data = get_data.get_data_vals(query, values)

        if cl_fullname != "":
            data1 = []
            for row in data:
                if cl_fullname.lower() in row[0].lower():
                    data1.append(row)
            data = data1

        self.ids["data_table"].row_data = [tuple(row) for row in data] + [("", "", "")]

    def order_update(self):
        data = get_data.get_data_from_dt(
            query="SELECT Клиент.ФИО AS ФИОКлиента, Заказ.idАвтомобиля, Заказ.Предоплата FROM Заказ JOIN Клиент ON Клиент.id=Заказ.idКлиента ORDER BY Заказ.id;",
            get_col_names=False)
        self.ids["data_table"].row_data = [tuple(row) for row in data]

    def add_row(self, instance) -> None:
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "order_add_window.py"]))
        th1.start()
        th1.join()
        self.order_update()

    def remove_row(self) -> None:
        pass

    def order(self):
        def on_check_press(instance, row_data):
            print(row_data)
            data = get_data.get_data_from_dt(
                f"SELECT  Заказ.id, Клиент.ФИО AS ФИОКлиента, Заказ.idАвтомобиля, Заказ.Предоплата FROM Заказ JOIN Клиент ON Клиент.id=Заказ.idКлиента;")

            print(row_data)
            for row in data:
                print ([str(col) for col in row], test.list_coincidence([str(col) for col in row], row_data))
                if test.list_coincidence([str(col) for col in row], row_data):
                    f = open("order.txt", "w")
                    for col in row:
                       f.write(str(col) + ";")
                    f.close()
            th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "order_edit_window.py"]))
            th1.start()
            th1.join()
            self.order_update()

        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data, col_data = get_data.get_data_from_dt(
            query="SELECT Клиент.ФИО AS ФИОКлиента, Заказ.idАвтомобиля, Заказ.Предоплата FROM Заказ JOIN Клиент ON Клиент.id=Заказ.idКлиента;",
            get_col_names=True)
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                (col_data[0], dp(60)),
                (col_data[1], dp(30)),
                (col_data[2], dp(60)),
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )
        data_table.bind(on_check_press=on_check_press)
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        layout.add_widget(table_layout)
        self.ids["table_layout"] = table_layout

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_fullname = MDTextField(
            mode="round",
            hint_text="ФИО Клиента",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_client_fullname"] = tf_fullname
        card.add_widget(tf_fullname)
        tf_auto_id = MDTextField(
            mode="round",
            hint_text="id Авто",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_auto_id"] = tf_auto_id
        card.add_widget(tf_auto_id)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_order)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.clear_order)
        card.add_widget(clear_button)
        add_button = MDRaisedButton(
            text="Добавить предзаказ",
            pos_hint={"center_x": 0.5},
        )
        add_button.bind(on_press=self.add_row)
        card.add_widget(add_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=1,
            )
        )
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)

        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def add_test_row(self, instance) -> None:
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "test_add_window.py"]))
        th1.start()
        th1.join()
        self.test_update()

    def test(self):
        def on_check_press(instance, row_data):
            print(row_data)
            data = get_data.get_data_from_dt(
                f"SELECT Тест.id, Клиент.ФИО AS Клиент, Сотрудник.ФИО AS Сотрудник, Автомобиль.id as idAuto, Тест.Дата, Тест.Время from Тест join Клиент on Тест.idКлиента=Клиент.id JOIN Сотрудник ON Тест.idСотрудника=Сотрудник.id JOIN Автомобиль ON Автомобиль.id=Тест.idАвтомобиля WHERE Дата >= '{time.strftime('%Y-%m-%d', time.gmtime())}' ORDER BY Дата, Время;")

            print(row_data)
            for row in data:
                print ([str(col) for col in row], test.list_coincidence([str(col) for col in row], row_data))
                if test.list_coincidence([str(col) for col in row], row_data):
                    f = open("test.txt", "w")
                    for col in row:
                       f.write(str(col) + ";")
                    f.close()
            th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "test_edit_window.py"]))
            th1.start()
            th1.join()
            self.test_update()

        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data, col_data = get_data.get_data_from_dt(
            query=f"select Клиент.ФИО AS Клиент, Сотрудник.ФИО AS Сотрудник, Автомобиль.id as idAuto, Тест.Дата, Тест.Время from Тест join Клиент on Тест.idКлиента=Клиент.id join Сотрудник on Тест.idСотрудника=Сотрудник.id join Автомобиль on Автомобиль.id=Тест.idАвтомобиля where Дата >= '{time.strftime('%Y-%m-%d', time.gmtime())}' order by Дата, Время;",
            get_col_names=True)
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                (col_data[0], dp(60)),
                (col_data[1], dp(60)),
                (col_data[2], dp(30)),
                (col_data[3], dp(30)),
                (col_data[4], dp(30)),
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )
        data_table.bind(on_check_press=on_check_press)
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_fullname = MDTextField(
            mode="round",
            hint_text="ФИО Клиента",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_client_fullname"] = tf_fullname
        card.add_widget(tf_fullname)
        tf_emp_fullname = MDTextField(
            mode="round",
            hint_text="ФИО Сотрудника",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_emp_fullname"] = tf_emp_fullname
        card.add_widget(tf_emp_fullname)
        tf_auto_id = MDTextField(
            mode="round",
            hint_text="id Авто",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_auto_id"] = tf_auto_id
        card.add_widget(tf_auto_id)

        date_layout = BoxLayout(
            size_hint_x=0.7,
            size_hint_y=0.1,
            pos_hint={"center_x": 0.5},
        )
        date_button = MDIconButton(
            icon="calendar.png",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        tf_date = MDTextField(
            mode="round",
            hint_text="Дата: гггг-мм-дд",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_date"] = tf_date
        date_button.bind(on_press=self.show_date_picker)
        date_layout.add_widget(tf_date)
        date_layout.add_widget(date_button)
        card.add_widget(date_layout)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_test)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.clear_test)
        card.add_widget(clear_button)
        drivers_button = MDRaisedButton(
            text="Список водителей",
            pos_hint={"center_x": 0.5},
        )
        drivers_button.bind(on_press=self.drivers)
        card.add_widget(drivers_button)
        add_button = MDRaisedButton(
            text="Добавить запись",
            pos_hint={"center_x": 0.5},
        )
        add_button.bind(on_press=self.add_test_row)
        card.add_widget(add_button)
        card.add_widget(BoxLayout(
            size_hint_y=0.27,
        ))
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def on_sales_save_start(self, instance, value, date_range):
        self.ids["tf_date_start"].text=str(value)

    def on_sales_save_end(self, instance, value, date_range):
        self.ids["tf_date_end"].text = str(value)

    def show_sales_date_picker(self, instance):
        print(instance==self.ids["date_button_start"])
        date_dialog = MDDatePicker()
        if instance==self.ids["date_button_start"]:
            date_dialog.bind(on_save=self.on_sales_save_start)
        else:
            date_dialog.bind(on_save=self.on_sales_save_end)
        date_dialog.open()

    def sales_clear(self, instance):
        self.ids["tf_client_fullname"].text = ""
        self.ids["tf_auto_id"].text = ""
        self.ids["tf_date_start"].text = ""
        self.ids["tf_date_end"].text = ""

    def search_sales(self, instance):
        cl_fullname = self.ids["tf_client_fullname"].text
        auto_id = self.ids["tf_auto_id"].text
        date_start = self.ids["tf_date_start"].text
        date_end = self.ids["tf_date_end"].text

        values = []

        f = open("user.txt", "r")
        user_id = int(f.readline())
        f.close()
        """
        data, col_data = get_data.get_data_vals(
        query=f"SELECT Клиент.ФИО AS Клиент, Продажа.idАвтомобиля, Продажа.Дата FROM Продажа JOIN Сотрудник ON Продажа.idСотрудника=Сотрудник.id JOIN Клиент ON Клиент.id=Продажа.idКлиента WHERE Продажа.idСотрудника=%s;",
        vals=[id],
        get_col_names=True)
        """
        values = [user_id]
        query = f"SELECT Клиент.ФИО AS Клиент, Продажа.idАвтомобиля, Продажа.Дата FROM Продажа JOIN Сотрудник ON Продажа.idСотрудника=Сотрудник.id JOIN Клиент ON Клиент.id=Продажа.idКлиента WHERE Продажа.idСотрудника=%s"

        if auto_id != "":
            query += " and Продажа.idАвтомобиля = %s"
            values.append(int(auto_id))

        if date_start != "":
            if test.is_right_date(date_start):
                query += "and Дата >= %s"
                values += [date_start]
            else:
                self.ids["tf_date_start"].text=""
                self.ids["tf_date_start"].hint_text="Формат: гггг-мм-дд"

        if date_end != "":
            if test.is_right_date(date_end):
                query += "and Дата <= %s"
                values += [date_end]
            else:
                self.ids["tf_date_end"].text = ""
                self.ids["tf_date_end"].hint_text = "Формат: гггг-мм-дд"

        data = get_data.get_data_vals(query, values)

        if cl_fullname != "":
            data1 = []
            for row in data:
                if cl_fullname.lower() in row[0].lower():
                    data1.append(row)
            data = data1

        self.ids["data_table"].row_data = [tuple(row) for row in data] + [("", "", "")]

    def sales_update(self):
        f = open("user.txt", "r")
        id = int(f.readline())
        f.close()
        data = get_data.get_data_vals(
        query=f"SELECT Клиент.ФИО AS Клиент, Продажа.idАвтомобиля, Продажа.Дата FROM Продажа JOIN Сотрудник ON Продажа.idСотрудника=Сотрудник.id JOIN Клиент ON Клиент.id=Продажа.idКлиента WHERE Продажа.idСотрудника=%s;",
        vals=[id],
        get_col_names=False)
        self.ids["data_table"].row_data = [tuple(row) for row in data]

    def add_sales_row(self, instance):
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "sales_add_window.py"]))
        th1.start()
        th1.join()
        self.sales_update()

    def sales(self):
        def on_check_press(instance, row_data):
            print(row_data)
            f = open("user.txt", "r")
            id = int(f.readline())
            f.close()
            data = get_data.get_data_vals(
                query=f"SELECT Продажа.id, Клиент.ФИО AS Клиент, Продажа.idАвтомобиля, Продажа.Дата FROM Продажа JOIN Сотрудник ON Продажа.idСотрудника=Сотрудник.id JOIN Клиент ON Клиент.id=Продажа.idКлиента WHERE Продажа.idСотрудника=%s;",
                vals=[id],
                get_col_names=False)
            print(row_data)
            for row in data:
                if test.list_coincidence([str(col) for col in row], row_data):
                    f = open("sale.txt", "w")
                    for col in row:
                        f.write(str(col) + ";")
                    f.close()
            th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "sales_edit_window.py"]))
            th1.start()
            th1.join()
            self.sales_update()

        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        f = open("user.txt", "r")
        id = int(f.readline())
        f.close()
        data, col_data = get_data.get_data_vals(
            query=f"SELECT Клиент.ФИО AS Клиент, Продажа.idАвтомобиля, Продажа.Дата FROM Продажа JOIN Сотрудник ON Продажа.idСотрудника=Сотрудник.id JOIN Клиент ON Клиент.id=Продажа.idКлиента WHERE Продажа.idСотрудника=%s;",
            vals=[id],
            get_col_names=True)

        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                (col_data[0], dp(60)),
                (col_data[1], dp(30)),
                (col_data[2], dp(30)),
            ],
            row_data=[
                tuple(row) for row in data
            ]+[("", "", "")],
            sorted_order="ASC",
            elevation=2,
        )
        data_table.bind(on_check_press=on_check_press)
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_fullname = MDTextField(
            mode="round",
            hint_text="ФИО Клиента",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_client_fullname"] = tf_fullname
        card.add_widget(tf_fullname)
        tf_auto_id = MDTextField(
            mode="round",
            hint_text="id Авто",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_auto_id"] = tf_auto_id
        card.add_widget(tf_auto_id)

        date_layout_start = BoxLayout(
            size_hint_x=0.7,
            size_hint_y=0.2,
            pos_hint={"center_x": 0.5},
        )
        date_button_start = MDIconButton(
            icon="calendar.png",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["date_button_start"] = date_button_start
        tf_date_start = MDTextField(
            mode="round",
            hint_text="Начало: гггг-мм-дд",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_date_start"] = tf_date_start
        date_button_start.bind(on_press=self.show_sales_date_picker)
        date_layout_start.add_widget(tf_date_start)
        date_layout_start.add_widget(date_button_start)
        card.add_widget(date_layout_start)
        date_layout_end = BoxLayout(
            size_hint_x=0.7,
            size_hint_y=0.2,
            pos_hint={"center_x": 0.5},
        )
        date_button_end = MDIconButton(
            icon="calendar.png",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["date_button_end"] = date_button_end
        tf_date_end = MDTextField(
            mode="round",
            hint_text="Конец: гггг-мм-дд",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_date_end"] = tf_date_end
        date_button_end.bind(on_press=self.show_sales_date_picker)
        date_layout_end.add_widget(tf_date_end)
        date_layout_end.add_widget(date_button_end)
        card.add_widget(date_layout_end)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_sales)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        clear_button.bind(on_press=self.sales_clear)
        card.add_widget(clear_button)
        add_button = MDRaisedButton(
            text="Зафиксировать продажу",
            pos_hint={"center_x": 0.5},
        )
        add_button.bind(on_press=self.add_sales_row)
        card.add_widget(add_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=1,
            )
        )
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def my_info(self):
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "my_info.py"]))
        th1.start()
        th1.join()


class AdminWindow(MDScreen):
    def clear_mark(self, instance):
        self.ids["tf_model"].text = ""
        self.ids["tf_class"].text = ""

    def search_mark(self, instance):
        s_model = self.ids["tf_model"].text
        s_class = self.ids["tf_class"].text
        query = "SELECT Модель, Класс FROM Марка WHERE Модель=Модель"

        vals = []

        if s_model != "":
            query += " AND Марка.Модель = %s"
            vals.append(s_model.lower())

        if s_class != "":
            query += " AND Марка.Класс = %s"
            vals.append(s_class.lower())

        query += ";"

        data = get_data.get_data_vals(query=query, vals=vals, get_col_names=False)
        print(data)

        data_table = self.ids["data_table"]
        data_table.row_data = [tuple(row) for row in data] + [("", "", "")]

    def mark_update(self):
        query = "SELECT * FROM Марка;"
        data = get_data.get_data_from_dt(query)
        self.ids["data_table"].row_data = [tuple(row) for row in data]

    def add_mark(self, instance):
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "add_mark_window.py"]))
        th1.start()
        th1.join()
        self.mark_update()

    def mark(self):
        def on_check_press(instance, row_data):
            data = get_data.get_data_from_dt("SELECT id, Модель, Класс FROM Марка")

            for row in data:
                if test.list_coincidence([str(col) for col in row], row_data):
                    f = open("mark.txt", "w")
                    for col in row:
                       f.write(str(col) + ";")
                    f.close()
            th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "mark_edit_window.py"]))
            th1.start()
            th1.join()
            self.mark_update()

        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data, data_col = get_data.get_data_from_dt(
            query="SELECT id, Модель, Класс FROM Марка",
            get_col_names=True)
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                (col, dp(30)) for col in data_col
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )
        data_table.bind(on_check_press=on_check_press)
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_model = MDTextField(
            id="model",
            mode="round",
            hint_text="Модель",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_model"] = tf_model
        card.add_widget(tf_model)
        tf_class = MDTextField(
            id="class",
            mode="round",
            hint_text="Класс",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_class"] = tf_class
        card.add_widget(tf_class)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_mark)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.clear_mark)
        card.add_widget(clear_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=0.4,
            )
        )
        add_button = MDRaisedButton(
            text="Добавить марку",
            pos_hint={"center_x": 0.5},
        )
        add_button.bind(on_press=self.add_mark)
        card.add_widget(add_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=1,
            )
        )
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def clear_cfs(self, instance):
        self.ids["tf_id"].text=""
        self.ids["tf_model"].text = ""
        self.ids["tf_class"].text = ""
        self.ids["tf_category"].text = ""
        self.ids["tf_color"].text = ""

    def search_cfs(self, instance):
        s_id = self.ids["tf_id"].text
        s_model = self.ids["tf_model"].text
        s_class = self.ids["tf_class"].text
        s_category = self.ids["tf_category"].text
        s_color = self.ids["tf_color"].text
        query="SELECT Автомобиль.id, Марка.Модель, Марка.Класс, Автомобиль.Категория, Автомобиль.Цвет, Автомобиль.Количество FROM Марка JOIN Автомобиль ON Марка.id=Автомобиль.idМарки WHERE Автомобиль.Количество > 0"

        vals = []

        if s_id.isdigit():
            query += " AND Автомобиль.id = %s"
            vals.append(s_id)

        if s_model != "":
            query += " AND Марка.Модель = %s"
            vals.append(s_model.lower())

        if s_class != "":
            query += " AND Марка.Класс = %s"
            vals.append(s_class.lower())

        if s_category != "":
            query += " AND Автомобиль.Категория = %s"
            vals.append(s_category.lower())

        if s_color != "":
            query += " AND Автомобиль.Цвет = %s"
            vals.append(s_color.lower())

        query += "ORDER BY Автомобиль.id;"

        data, data_col = get_data.get_data_vals(query=query, vals=vals, get_col_names=True)
        print(data)

        data_table = self.ids["data_table"]
        data_table.column_data = [(col, dp(30)) for col in data_col]
        data_table.row_data = [(row[0], row[1], row[2], row[3], row[4], row[5], ) for row in data]+[("", "", "", "", "", "")]

    def search_cic(self, instance):
        s_id = self.ids["tf_id"].text
        s_model = self.ids["tf_model"].text
        s_class = self.ids["tf_class"].text
        s_category = self.ids["tf_category"].text
        s_color = self.ids["tf_color"].text
        query="SELECT Автомобиль.id, Марка.Модель, Марка.Класс, Автомобиль.Категория, Автомобиль.Цвет, Автомобиль.Количество FROM Марка JOIN Автомобиль ON Марка.id=Автомобиль.idМарки WHERE Марка.id=Марка.id"

        vals = []

        if s_id.isdigit():
            query += " AND Автомобиль.id = %s"
            vals.append(s_id)

        if s_model != "":
            query += " AND Марка.Модель = %s"
            vals.append(s_model.lower())

        if s_class != "":
            query += " AND Марка.Класс = %s"
            vals.append(s_class.lower())

        if s_category != "":
            query += " AND Автомобиль.Категория = %s"
            vals.append(s_category.lower())

        if s_color != "":
            query += " AND Автомобиль.Цвет = %s"
            vals.append(s_color.lower())

        query += "  BY Автомобиль.id;"

        data, data_col = get_data.get_data_vals(query=query, vals=vals, get_col_names=True)

        data_table = self.ids["data_table"]
        data_table.column_data = [(col, dp(30)) for col in data_col]
        data_table.row_data = [(row[0], row[1], row[2], row[3], row[4], row[5], ) for row in data]+[("", "", "", "", "", "")]

    def cars_for_sale(self):
        def on_check_press(instance, row_data):
            print(row_data)
            data = get_data.get_data_vals("SELECT * FROM Автомобиль WHERE id=%s", [int(row_data[0])])

            f = open("auto.txt", "w")

            for symb in data[0]:
                f.write(str(symb)+";")

            f.close()

            th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "aic_edit_window.py"]))
            th1.start()
            th1.join()
            self.auto_update()
        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data, data_col = get_data.get_data_from_dt(
            query="SELECT Автомобиль.id, Марка.Модель, Марка.Класс, Автомобиль.Категория, Автомобиль.Цвет, Автомобиль.Количество FROM Марка JOIN Автомобиль ON Марка.id=Автомобиль.idМарки WHERE Автомобиль.Количество > 0 ORDER BY Автомобиль.id;",
            get_col_names=True)
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                (col, dp(30)) for col in data_col
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )
        data_table.bind(on_check_press=on_check_press)
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_id = MDTextField(
            id="id",
            mode="round",
            hint_text="id",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_id"] = tf_id
        card.add_widget(tf_id)
        tf_model = MDTextField(
            id="model",
            mode="round",
            hint_text="Модель",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_model"] = tf_model
        card.add_widget(tf_model)
        tf_class = MDTextField(
            id="class",
            mode="round",
            hint_text="Класс",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_class"] = tf_class
        card.add_widget(tf_class)
        tf_category = MDTextField(
            id="category",
            mode="round",
            hint_text="Категория",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_category"] = tf_category
        card.add_widget(tf_category)
        tf_color = MDTextField(
            id="color",
            mode="round",
            hint_text="Цвет",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_color"] = tf_color
        card.add_widget(tf_color)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_cfs)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.clear_cfs)
        card.add_widget(clear_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=0.4,
            )
        )
        add_button = MDRaisedButton(
            text="Добавить авто",
            pos_hint={"center_x": 0.5},
        )
        add_button.bind(on_press=self.add_auto_sale)
        card.add_widget(add_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=1,
            )
        )
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def auto_update(self):
        data = get_data.get_data_from_dt(query="SELECT Автомобиль.id, Марка.Модель, Марка.Класс, Автомобиль.Категория, Автомобиль.Цвет, Автомобиль.Количество FROM Марка JOIN Автомобиль ON Марка.id=Автомобиль.idМарки ORDER BY Автомобиль.id;")
        self.ids["data_table"].row_data = [tuple(row) for row in data]

    def auto_update_sale(self):
        data = get_data.get_data_from_dt(query="SELECT Автомобиль.id, Марка.Модель, Марка.Класс, Автомобиль.Категория, Автомобиль.Цвет, Автомобиль.Количество FROM Марка JOIN Автомобиль ON Марка.id=Автомобиль.idМарки ORDER BY Автомобиль.id;")
        self.ids["data_table"].row_data = [tuple(row) for row in data]

    def cars_in_catalog_update(self):
        data = get_data.get_data_from_dt(
            query="SELECT Автомобиль.id, Марка.Модель, Марка.Класс, Автомобиль.Категория, Автомобиль.Цвет, Автомобиль.Количество FROM Марка JOIN Автомобиль ON Марка.id=Автомобиль.idМарки ORDER BY Автомобиль.id;")
        self.ids["data_table"].row_data = [tuple(row) for row in data] + [("", "", "", "", "", "")]

    def cars_for_sale_update(self):
        data = get_data.get_data_from_dt(
            query="SELECT Автомобиль.id, Марка.Модель, Марка.Класс, Автомобиль.Категория, Автомобиль.Цвет, Автомобиль.Количество FROM Марка JOIN Автомобиль ON Марка.id=Автомобиль.idМарки WHERE Автомобиль.Количество > 0 ORDER BY Автомобиль.id;")
        self.ids["data_table"].row_data = [tuple(row) for row in data] + [("", "", "", "", "", "")]

    def add_auto(self, instance):
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "auto_add_window.py"]))
        th1.start()
        th1.join()
        self.cars_in_catalog_update()

    def add_auto_sale(self, instance):
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "auto_add_window.py"]))
        th1.start()
        th1.join()
        self.cars_for_sale_update()

    def cars_in_catalog(self):
        def on_check_press(instance, row_data):
            print(row_data)
            data = get_data.get_data_vals("SELECT * FROM Автомобиль WHERE id=%s", [int(row_data[0])])

            f = open("auto.txt", "w")

            for symb in data[0]:
                f.write(str(symb)+";")

            f.close()

            th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "aic_edit_window.py"]))
            th1.start()
            th1.join()
            self.auto_update()

        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data, data_col = get_data.get_data_from_dt(
            query="SELECT Автомобиль.id, Марка.Модель, Марка.Класс, Автомобиль.Категория, Автомобиль.Цвет, Автомобиль.Количество FROM Марка JOIN Автомобиль ON Марка.id=Автомобиль.idМарки ORDER BY Автомобиль.id;",
            get_col_names=True)
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                (col, dp(30)) for col in data_col
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )
        data_table.bind(on_check_press=on_check_press)
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_id = MDTextField(
            id="id",
            mode="round",
            hint_text="id",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_id"] = tf_id
        card.add_widget(tf_id)
        tf_model = MDTextField(
            id="model",
            mode="round",
            hint_text="Модель",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_model"] = tf_model
        card.add_widget(tf_model)
        tf_class = MDTextField(
            id="class",
            mode="round",
            hint_text="Класс",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_class"] = tf_class
        card.add_widget(tf_class)
        tf_category = MDTextField(
            id="category",
            mode="round",
            hint_text="Категория",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_category"] = tf_category
        card.add_widget(tf_category)
        tf_color = MDTextField(
            id="color",
            mode="round",
            hint_text="Цвет",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_color"] = tf_color
        card.add_widget(tf_color)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_cic)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.clear_cfs)
        card.add_widget(clear_button)
        add_button = MDRaisedButton(
            text="Добавить авто",
            pos_hint={"center_x": 0.5},
        )
        add_button.bind(on_press=self.add_auto)
        card.add_widget(add_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=0.4,
            )
        )
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def search_cic(self, instance):
        s_id = self.ids["tf_id"].text
        s_model = self.ids["tf_model"].text
        s_class = self.ids["tf_class"].text
        s_category = self.ids["tf_category"].text
        s_color = self.ids["tf_color"].text
        query="SELECT Автомобиль.id, Марка.Модель, Марка.Класс, Автомобиль.Категория, Автомобиль.Цвет, Автомобиль.Количество FROM Марка JOIN Автомобиль ON Марка.id=Автомобиль.idМарки WHERE Марка.id=Марка.id"

        vals = []

        if s_id.isdigit():
            query += " AND Автомобиль.id = %s"
            vals.append(s_id)

        if s_model != "":
            query += " AND Марка.Модель = %s"
            vals.append(s_model.lower())

        if s_class != "":
            query += " AND Марка.Класс = %s"
            vals.append(s_class.lower())

        if s_category != "":
            query += " AND Автомобиль.Категория = %s"
            vals.append(s_category.lower())

        if s_color != "":
            query += " AND Автомобиль.Цвет = %s"
            vals.append(s_color.lower())

        query += " ORDER BY Автомобиль.id;"

        data, data_col = get_data.get_data_vals(query=query, vals=vals, get_col_names=True)

        data_table = self.ids["data_table"]
        data_table.column_data = [(col, dp(30)) for col in data_col]
        data_table.row_data = [(row[0], row[1], row[2], row[3], row[4], row[5], ) for row in data]+[("", "", "", "", "", "")]

    def search_drivers(self, instance):
        s_fullname = self.ids["tf_fullname"].text
        s_gender = self.ids["tf_gender"].text
        query="SELECT ФИО, Телефон, ДатаРождения, Пол FROM Сотрудник WHERE Должность='водитель'"

        vals = []

        if s_gender != "":
            query += " AND Пол = %s"
            vals.append(s_gender.lower())

        data, data_col = get_data.get_data_vals(query=query, vals=vals, get_col_names=True)

        data1 = []

        if s_fullname != "":
            for row in data:
                if s_fullname.lower() in row[0].lower():
                    data1.append(row)
            data = data1

        data_table = self.ids["data_table"]
        data_table.column_data = [(col, dp(30)) for col in data_col]
        data_table.row_data = [tuple(row) for row in data]+[("", "", "", "",)]

    def search_clients(self, instance):
        s_fullname = self.ids["tf_fullname"].text
        s_passport_num = self.ids["tf_passport_num"].text
        s_phone_num = self.ids["tf_phone_num"].text
        s_gender = self.ids["tf_gender"].text
        query="SELECT ФИО, Телефон, НомерПаспорта, Пол FROM Клиент WHERE ФИО=ФИО"

        vals = []

        if s_gender != "":
            query += " AND Пол = %s"
            vals.append(s_gender.lower())

        if s_phone_num != "":
            query += " AND Телефон = %s"
            vals.append(s_phone_num.lower())

        if s_passport_num != "":
            query += " AND НомерПаспорта = %s"
            vals.append(s_passport_num.lower())

        data, data_col = get_data.get_data_vals(query=query, vals=vals, get_col_names=True)

        data1 = []

        if s_fullname != "":
            for row in data:
                if s_fullname.lower() in row[0].lower():
                    data1.append(row)
            data = data1

        data_table = self.ids["data_table"]
        data_table.column_data = [(col, dp(30)) for col in data_col]
        data_table.row_data = [tuple(row) for row in data]+[("", "", "", "",)]

    def clear_drivers(self, instance):
        self.ids["tf_fullname"].text = ""
        self.ids["tf_gender"].text = ""

    def cleaer_clients(self, instance):
        self.ids["tf_fullname"].text = ""
        self.ids["tf_gender"].text = ""
        self.ids["tf_phone_num"].text = ""
        self.ids["tf_passport_num"].text = ""

    def drivers(self, instance):
        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data, data_col = get_data.get_data_from_dt(query="SELECT ФИО, Телефон, ДатаРождения, Пол FROM Сотрудник WHERE Должность='водитель'", get_col_names=True)
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                ("ФИО", dp(70)),
                ("Телефон", dp(40)),
                ("ДатаРождения", dp(50)),
                ("Пол", dp(40)),
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_fullname = MDTextField(
            id="tf_fullname",
            mode="round",
            hint_text="ФИО",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_fullname"] = tf_fullname
        card.add_widget(tf_fullname)
        tf_gender = MDTextField(
            id="tf_gender",
            mode="round",
            hint_text="м или ж",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_gender"] = tf_gender
        card.add_widget(tf_gender)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_drivers)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.clear_drivers)
        card.add_widget(clear_button)
        card.add_widget(MDLabel())
        card.add_widget(MDLabel())
        self.ids["card"] = card
        search_layout.add_widget(card)
        n_layout = BoxLayout(
            size_hint_y=0.5,
        )
        # search_layout.add_widget(n_layout)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def clients_update(self):
        data = get_data.get_data_from_dt(query="SELECT ФИО, Телефон, НомерПаспорта, Пол FROM Клиент GROUP BY id;")
        self.ids["data_table"].row_data = [tuple(row) for row in data]

    def add_client_row(self, instance):
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "clients_add_window.py"]))
        th1.start()
        th1.join()
        self.clients_update()

    def clients(self):
        def on_check_press(instance, row_data):
            print(row_data)
            data = get_data.get_data_vals("SELECT id FROM Клиент WHERE ФИО=%s AND Телефон=%s AND НомерПаспорта=%s AND Пол=%s;", row_data)

            id = str(data[0][0])

            f = open("client.txt", "w")
            f.write(id+";")
            for i in range(len(row_data)):
                f.write(row_data[i]+';')
            f.close()

            th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "clients_edit_window.py"]))
            th1.start()
            th1.join()
            self.clients_update()

        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data = get_data.get_data_from_dt(query="SELECT ФИО, Телефон, НомерПаспорта, Пол FROM Клиент GROUP BY id;")
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                ("ФИО", dp(70)),
                ("Телефон", dp(40)),
                ("НомерПаспорта", dp(50)),
                ("Пол", dp(40)),
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )

        data_table.bind(on_check_press=on_check_press)
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_fullname = MDTextField(
            id="tf_fullname",
            mode="round",
            hint_text="ФИО",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_fullname"] = tf_fullname
        card.add_widget(tf_fullname)
        tf_phone_num = MDTextField(
            id="tf_phone_num",
            mode="round",
            hint_text="+7(777)777-77-77",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_phone_num"] = tf_phone_num
        card.add_widget(tf_phone_num)
        tf_passport_num = MDTextField(
            id="tf_passport_num",
            mode="round",
            hint_text="0123456789",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_passport_num"] = tf_passport_num
        card.add_widget(tf_passport_num)
        tf_gender = MDTextField(
            id="tf_gender",
            mode="round",
            hint_text="м или ж",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_gender"] = tf_gender
        card.add_widget(tf_gender)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_clients)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.cleaer_clients)
        card.add_widget(clear_button)
        add_button = MDRaisedButton(
            text="Добавить клиента",
            pos_hint={"center_x": 0.5},
        )
        add_button.bind(on_press=self.add_client_row)
        card.add_widget(add_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=0.4,
            )
        )
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def on_save(self, instance, value, date_range):
        self.ids["tf_date"].text = str(value)

    def show_date_picker(self, instance):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def clear_test(self, instance):
        self.ids["tf_client_fullname"].text = ""
        self.ids["tf_emp_fullname"].text = ""
        self.ids["tf_auto_id"].text = ""
        self.ids["tf_date"].text = ""

    def search_test(self, instance):
        cl_fullname = self.ids["tf_client_fullname"].text
        emp_fullname = self.ids["tf_emp_fullname"].text
        auto_id = self.ids["tf_auto_id"].text
        date = self.ids["tf_date"].text

        values = []
        query = f"select Клиент.ФИО AS Клиент, Сотрудник.ФИО AS Сотрудник, Автомобиль.id as idAuto, Тест.Дата, Тест.Время from Тест join Клиент on Тест.idКлиента=Клиент.id join Сотрудник on Тест.idСотрудника=Сотрудник.id join Автомобиль on Автомобиль.id=Тест.idАвтомобиля where Дата >= '{time.strftime('%Y-%m-%d', time.gmtime())}'"

        if auto_id != "":
            query += "and Автомобиль.id = %s"
            values.append(int(auto_id))

        if date != "":
            query += "and Тест.Дата = %s"
            values.append(date)

        query += " order by Дата, Время;"
        data = get_data.get_data_vals(query, values)

        if cl_fullname != "":
            data1 = []
            for row in data:
                if cl_fullname.lower() in row[0].lower():
                    data1.append(row)
            data = data1

        if emp_fullname != "":
            data1 = []
            for row in data:
                if emp_fullname.lower() in row[1].lower():
                    data1.append(row)
            data = data1

        self.ids["data_table"].row_data = [tuple(row) for row in data] + [("", "", "", "", "")]

    def test_update(self):
        data = get_data.get_data_from_dt(
            query=f"select Клиент.ФИО AS Клиент, Сотрудник.ФИО AS Сотрудник, Автомобиль.id as idAuto, Тест.Дата, Тест.Время from Тест join Клиент on Тест.idКлиента=Клиент.id join Сотрудник on Тест.idСотрудника=Сотрудник.id join Автомобиль on Автомобиль.id=Тест.idАвтомобиля where Дата >= '{time.strftime('%Y-%m-%d', time.gmtime())}' order by Дата, Время;",
            get_col_names=False)
        self.ids["data_table"].row_data = [tuple(row) for row in data]

    def clear_order(self, instance):
        self.ids["tf_client_fullname"].text = ""
        self.ids["tf_auto_id"].text = ""

    def search_order(self, instance):
        cl_fullname = self.ids["tf_client_fullname"].text
        auto_id = self.ids["tf_auto_id"].text

        values = []
        query = f"SELECT Клиент.ФИО AS ФИОКлиента, Заказ.idАвтомобиля, Заказ.Предоплата FROM Заказ JOIN Клиент ON Клиент.id=Заказ.idКлиента"

        if auto_id != "":
            query += " and Заказ.idАвтомобиля = %s"
            values.append(int(auto_id))

        print(query, values)
        data = get_data.get_data_vals(query, values)

        if cl_fullname != "":
            data1 = []
            for row in data:
                if cl_fullname.lower() in row[0].lower():
                    data1.append(row)
            data = data1

        self.ids["data_table"].row_data = [tuple(row) for row in data] + [("", "", "")]

    def order_update(self):
        data = get_data.get_data_from_dt(
            query="SELECT Клиент.ФИО AS ФИОКлиента, Заказ.idАвтомобиля, Заказ.Предоплата FROM Заказ JOIN Клиент ON Клиент.id=Заказ.idКлиента;",
            get_col_names=False)
        self.ids["data_table"].row_data = [tuple(row) for row in data]

    def add_row(self, instance) -> None:
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "order_add_window.py"]))
        th1.start()
        th1.join()
        self.order_update()

    def remove_row(self) -> None:
        pass

    def order(self):
        def on_check_press(instance, row_data):
            print(row_data)
            data = get_data.get_data_from_dt(
                f"SELECT  Заказ.id, Клиент.ФИО AS ФИОКлиента, Заказ.idАвтомобиля, Заказ.Предоплата FROM Заказ JOIN Клиент ON Клиент.id=Заказ.idКлиента;")

            print(row_data)
            for row in data:
                print ([str(col) for col in row], test.list_coincidence([str(col) for col in row], row_data))
                if test.list_coincidence([str(col) for col in row], row_data):
                    f = open("order.txt", "w")
                    for col in row:
                       f.write(str(col) + ";")
                    f.close()
            th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "order_edit_window.py"]))
            th1.start()
            th1.join()
            self.order_update()

        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data, col_data = get_data.get_data_from_dt(
            query="SELECT Клиент.ФИО AS ФИОКлиента, Заказ.idАвтомобиля, Заказ.Предоплата FROM Заказ JOIN Клиент ON Клиент.id=Заказ.idКлиента;",
            get_col_names=True)
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                (col_data[0], dp(60)),
                (col_data[1], dp(30)),
                (col_data[2], dp(60)),
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )
        data_table.bind(on_check_press=on_check_press)
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        layout.add_widget(table_layout)
        self.ids["table_layout"] = table_layout

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_fullname = MDTextField(
            mode="round",
            hint_text="ФИО Клиента",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_client_fullname"] = tf_fullname
        card.add_widget(tf_fullname)
        tf_auto_id = MDTextField(
            mode="round",
            hint_text="id Авто",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_auto_id"] = tf_auto_id
        card.add_widget(tf_auto_id)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_order)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.clear_order)
        card.add_widget(clear_button)
        add_button = MDRaisedButton(
            text="Добавить предзаказ",
            pos_hint={"center_x": 0.5},
        )
        add_button.bind(on_press=self.add_row)
        card.add_widget(add_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=1,
            )
        )
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)

        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def add_test_row(self, instance) -> None:
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "test_add_window.py"]))
        th1.start()
        th1.join()
        self.test_update()

    def test(self):
        def on_check_press(instance, row_data):
            print(row_data)
            data = get_data.get_data_from_dt(
                f"SELECT Тест.id, Клиент.ФИО AS Клиент, Сотрудник.ФИО AS Сотрудник, Автомобиль.id as idAuto, Тест.Дата, Тест.Время from Тест join Клиент on Тест.idКлиента=Клиент.id JOIN Сотрудник ON Тест.idСотрудника=Сотрудник.id JOIN Автомобиль ON Автомобиль.id=Тест.idАвтомобиля WHERE Дата >= '{time.strftime('%Y-%m-%d', time.gmtime())}' ORDER BY Дата, Время;")

            print(row_data)
            for row in data:
                print ([str(col) for col in row], test.list_coincidence([str(col) for col in row], row_data))
                if test.list_coincidence([str(col) for col in row], row_data):
                    f = open("test.txt", "w")
                    for col in row:
                       f.write(str(col) + ";")
                    f.close()
            th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "test_edit_window.py"]))
            th1.start()
            th1.join()
            self.test_update()

        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data, col_data = get_data.get_data_from_dt(
            query=f"select Клиент.ФИО AS Клиент, Сотрудник.ФИО AS Сотрудник, Автомобиль.id as idAuto, Тест.Дата, Тест.Время from Тест join Клиент on Тест.idКлиента=Клиент.id join Сотрудник on Тест.idСотрудника=Сотрудник.id join Автомобиль on Автомобиль.id=Тест.idАвтомобиля where Дата >= '{time.strftime('%Y-%m-%d', time.gmtime())}' order by Дата, Время;",
            get_col_names=True)
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                (col_data[0], dp(60)),
                (col_data[1], dp(60)),
                (col_data[2], dp(30)),
                (col_data[3], dp(30)),
                (col_data[4], dp(30)),
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )
        data_table.bind(on_check_press=on_check_press)
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_fullname = MDTextField(
            mode="round",
            hint_text="ФИО Клиента",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_client_fullname"] = tf_fullname
        card.add_widget(tf_fullname)
        tf_emp_fullname = MDTextField(
            mode="round",
            hint_text="ФИО Сотрудника",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_emp_fullname"] = tf_emp_fullname
        card.add_widget(tf_emp_fullname)
        tf_auto_id = MDTextField(
            mode="round",
            hint_text="id Авто",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_auto_id"] = tf_auto_id
        card.add_widget(tf_auto_id)

        date_layout = BoxLayout(
            size_hint_x=0.7,
            size_hint_y=0.1,
            pos_hint={"center_x": 0.5},
        )
        date_button = MDIconButton(
            icon="calendar.png",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        tf_date = MDTextField(
            mode="round",
            hint_text="Дата: гггг-мм-дд",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_date"] = tf_date
        date_button.bind(on_press=self.show_date_picker)
        date_layout.add_widget(tf_date)
        date_layout.add_widget(date_button)
        card.add_widget(date_layout)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_test)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.clear_test)
        card.add_widget(clear_button)
        drivers_button = MDRaisedButton(
            text="Список водителей",
            pos_hint={"center_x": 0.5},
        )
        drivers_button.bind(on_press=self.drivers)
        card.add_widget(drivers_button)
        add_button = MDRaisedButton(
            text="Добавить запись",
            pos_hint={"center_x": 0.5},
        )
        add_button.bind(on_press=self.add_test_row)
        card.add_widget(add_button)
        card.add_widget(BoxLayout(
            size_hint_y=0.27,
        ))
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def on_sales_save_start(self, instance, value, date_range):
        self.ids["tf_date_start"].text=str(value)

    def on_sales_save_end(self, instance, value, date_range):
        self.ids["tf_date_end"].text = str(value)

    def show_sales_date_picker(self, instance):
        print(instance==self.ids["date_button_start"])
        date_dialog = MDDatePicker()
        if instance==self.ids["date_button_start"]:
            date_dialog.bind(on_save=self.on_sales_save_start)
        else:
            date_dialog.bind(on_save=self.on_sales_save_end)
        date_dialog.open()

    def sales_clear(self, instance):
        self.ids["tf_client_fullname"].text = ""
        self.ids["tf_auto_id"].text = ""
        self.ids["tf_date_start"].text = ""
        self.ids["tf_date_end"].text = ""

    def search_sales(self, instance):
        cl_fullname = self.ids["tf_client_fullname"].text
        auto_id = self.ids["tf_auto_id"].text
        date_start = self.ids["tf_date_start"].text
        date_end = self.ids["tf_date_end"].text

        values = []

        f = open("user.txt", "r")
        user_id = int(f.readline())
        f.close()
        """
        data, col_data = get_data.get_data_vals(
        query=f"SELECT Клиент.ФИО AS Клиент, Продажа.idАвтомобиля, Продажа.Дата FROM Продажа JOIN Сотрудник ON Продажа.idСотрудника=Сотрудник.id JOIN Клиент ON Клиент.id=Продажа.idКлиента WHERE Продажа.idСотрудника=%s;",
        vals=[id],
        get_col_names=True)
        """
        values = [user_id]
        query = f"SELECT Клиент.ФИО AS Клиент, Продажа.idАвтомобиля, Продажа.Дата FROM Продажа JOIN Сотрудник ON Продажа.idСотрудника=Сотрудник.id JOIN Клиент ON Клиент.id=Продажа.idКлиента WHERE Продажа.idСотрудника=%s"

        if auto_id != "":
            query += " and Продажа.idАвтомобиля = %s"
            values.append(int(auto_id))

        if date_start != "":
            if test.is_right_date(date_start):
                query += "and Дата >= %s"
                values += [date_start]
            else:
                self.ids["tf_date_start"].text=""
                self.ids["tf_date_start"].hint_text="Формат: гггг-мм-дд"

        if date_end != "":
            if test.is_right_date(date_end):
                query += "and Дата <= %s"
                values += [date_end]
            else:
                self.ids["tf_date_end"].text = ""
                self.ids["tf_date_end"].hint_text = "Формат: гггг-мм-дд"

        data = get_data.get_data_vals(query, values)

        if cl_fullname != "":
            data1 = []
            for row in data:
                if cl_fullname.lower() in row[0].lower():
                    data1.append(row)
            data = data1

        self.ids["data_table"].row_data = [tuple(row) for row in data] + [("", "", "")]

    def sales_update(self):
        f = open("user.txt", "r")
        id = int(f.readline())
        f.close()
        data = get_data.get_data_vals(
        query=f"SELECT Клиент.ФИО AS Клиент, Продажа.idАвтомобиля, Продажа.Дата FROM Продажа JOIN Сотрудник ON Продажа.idСотрудника=Сотрудник.id JOIN Клиент ON Клиент.id=Продажа.idКлиента WHERE Продажа.idСотрудника=%s;",
        vals=[id],
        get_col_names=False)
        self.ids["data_table"].row_data = [tuple(row) for row in data]

    def add_sales_row(self, instance):
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "sales_add_window.py"]))
        th1.start()
        th1.join()
        self.sales_update()

    def sales(self):
        def on_check_press(instance, row_data):
            print(row_data)
            f = open("user.txt", "r")
            id = int(f.readline())
            f.close()
            data = get_data.get_data_vals(
                query=f"SELECT Продажа.id, Клиент.ФИО AS Клиент, Продажа.idАвтомобиля, Продажа.Дата FROM Продажа JOIN Сотрудник ON Продажа.idСотрудника=Сотрудник.id JOIN Клиент ON Клиент.id=Продажа.idКлиента WHERE Продажа.idСотрудника=%s;",
                vals=[id],
                get_col_names=False)
            print(row_data)
            for row in data:
                if test.list_coincidence([str(col) for col in row], row_data):
                    f = open("sale.txt", "w")
                    for col in row:
                        f.write(str(col) + ";")
                    f.close()
            th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "sales_edit_window.py"]))
            th1.start()
            th1.join()
            self.sales_update()

        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        f = open("user.txt", "r")
        id = int(f.readline())
        f.close()
        data, col_data = get_data.get_data_vals(
            query=f"SELECT Клиент.ФИО AS Клиент, Продажа.idАвтомобиля, Продажа.Дата FROM Продажа JOIN Сотрудник ON Продажа.idСотрудника=Сотрудник.id JOIN Клиент ON Клиент.id=Продажа.idКлиента WHERE Продажа.idСотрудника=%s;",
            vals=[id],
            get_col_names=True)

        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                (col_data[0], dp(60)),
                (col_data[1], dp(30)),
                (col_data[2], dp(30)),
            ],
            row_data=[
                tuple(row) for row in data
            ]+[("", "", "")],
            sorted_order="ASC",
            elevation=2,
        )
        data_table.bind(on_check_press=on_check_press)
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_fullname = MDTextField(
            mode="round",
            hint_text="ФИО Клиента",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_client_fullname"] = tf_fullname
        card.add_widget(tf_fullname)
        tf_auto_id = MDTextField(
            mode="round",
            hint_text="id Авто",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_auto_id"] = tf_auto_id
        card.add_widget(tf_auto_id)

        date_layout_start = BoxLayout(
            size_hint_x=0.7,
            size_hint_y=0.2,
            pos_hint={"center_x": 0.5},
        )
        date_button_start = MDIconButton(
            icon="calendar.png",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["date_button_start"] = date_button_start
        tf_date_start = MDTextField(
            mode="round",
            hint_text="Начало: гггг-мм-дд",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_date_start"] = tf_date_start
        date_button_start.bind(on_press=self.show_sales_date_picker)
        date_layout_start.add_widget(tf_date_start)
        date_layout_start.add_widget(date_button_start)
        card.add_widget(date_layout_start)
        date_layout_end = BoxLayout(
            size_hint_x=0.7,
            size_hint_y=0.2,
            pos_hint={"center_x": 0.5},
        )
        date_button_end = MDIconButton(
            icon="calendar.png",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["date_button_end"] = date_button_end
        tf_date_end = MDTextField(
            mode="round",
            hint_text="Конец: гггг-мм-дд",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_date_end"] = tf_date_end
        date_button_end.bind(on_press=self.show_sales_date_picker)
        date_layout_end.add_widget(tf_date_end)
        date_layout_end.add_widget(date_button_end)
        card.add_widget(date_layout_end)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_sales)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        clear_button.bind(on_press=self.sales_clear)
        card.add_widget(clear_button)
        add_button = MDRaisedButton(
            text="Зафиксировать продажу",
            pos_hint={"center_x": 0.5},
        )
        add_button.bind(on_press=self.add_sales_row)
        card.add_widget(add_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=1,
            )
        )
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def my_info(self):
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "my_info.py"]))
        th1.start()
        th1.join()

    def employees_update(self):
        data = get_data.get_data_from_dt(query="SELECT ФИО, Телефон, Должность, ДатаРождения, Пол FROM Сотрудник ORDER BY id;")
        self.ids["data_table"].row_data = [tuple(row) for row in data]

    def clear_employees(self, instance):
        self.ids["tf_fullname"].text = ""
        self.ids["tf_gender"].text = ""
        self.ids["tf_position"].text = ""

    def search_employees(self, instance):
        s_fullname = self.ids["tf_fullname"].text
        s_gender = self.ids["tf_gender"].text
        s_position = self.ids["tf_position"].text
        query="SELECT ФИО, Телефон, Должность, ДатаРождения, Пол FROM Сотрудник WHERE Должность=Должность"

        vals = []

        if s_gender != "":
            query += " AND Пол = %s"
            vals.append(s_gender.lower())

        if s_position != "":
            query += " AND Должность = %s"
            vals.append(s_position.lower())

        data, data_col = get_data.get_data_vals(query=query, vals=vals, get_col_names=True)

        data1 = []

        if s_fullname != "":
            for row in data:
                if s_fullname.lower() in row[0].lower():
                    data1.append(row)
            data = data1

        data_table = self.ids["data_table"]
        data_table.column_data = [(col, dp(30)) for col in data_col]
        data_table.row_data = [tuple(row) for row in data] + [("", "", "", "", "")]

    def add_employees(self, instance):
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "add_employees_window.py"]))
        th1.start()
        th1.join()
        self.employees_update()

    def employees(self):
        def on_check_press(instance, row_data):
            print(row_data)
            data = get_data.get_data_from_dt(
                query=f"SELECT id, ФИО, Телефон, Должность, ДатаРождения, Пол FROM Сотрудник ORDER BY id",
                get_col_names=False)
            print(row_data)
            for row in data:
                if test.list_coincidence([str(col) for col in row], row_data):
                    f = open("employee.txt", "w")
                    for col in row:
                        f.write(str(col) + ";")
                    f.close()
            th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "edit_employees_window.py"]))
            th1.start()
            th1.join()
            self.employees_update()

        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data, data_col = get_data.get_data_from_dt(
            query="SELECT ФИО, Телефон, Должность, ДатаРождения, Пол FROM Сотрудник ORDER BY id",
            get_col_names=True)
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                ("ФИО", dp(75)),
                ("Телефон", dp(35)),
                ("Должность", dp(40)),
                ("ДатаРождения", dp(30)),
                ("Пол", dp(15)),
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )
        data_table.bind(on_check_press=on_check_press)
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_fullname = MDTextField(
            id="tf_fullname",
            mode="round",
            hint_text="ФИО",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_fullname"] = tf_fullname
        card.add_widget(tf_fullname)
        tf_gender = MDTextField(
            id="tf_gender",
            mode="round",
            hint_text="м или ж",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_gender"] = tf_gender
        card.add_widget(tf_gender)
        tf_position = MDTextField(
            id="tf_position",
            mode="round",
            hint_text="Должность",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_position"] = tf_position
        card.add_widget(tf_position)
        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_employees)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.clear_employees)
        card.add_widget(clear_button)
        add_button = MDRaisedButton(
            text="Добавить сотрудника",
            pos_hint={"center_x": 0.5},
        )
        add_button.bind(on_press=self.add_employees)
        card.add_widget(add_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=1,
            )
        )
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def search_shipper(self, instance):
        s_fullname = self.ids["tf_fullname"].text
        s_phone = self.ids["tf_phone_num"].text
        query="SELECT Название, Телефон FROM Поставщик WHERE id=id"

        vals = []

        if s_phone != "":
            query += " AND Телефон=%s"
            vals.append(s_phone)

        if len(vals) == 0:
            data = get_data.get_data_from_dt("SELECT Название, Телефон FROM Поставщик ORDER BY id;")
        else:
            data = get_data.get_data_vals(query=query, vals=vals,)
        print(query, vals)

        if s_fullname != "":
            data1 = []
            for row in data:
                if row[0].lower() == s_fullname.lower():
                    data1.append(row)

            data = data1

        self.ids["data_table"].row_data = [tuple(row) for row in data] + [("", "",)]

    def clear_shipper(self, instance):
        self.ids["tf_fullname"].text = ""
        self.ids["tf_phone_num"].text = ""

    def shipper_update(self):
        data = get_data.get_data_from_dt("SELECT Название, Телефон FROM Поставщик ORDER BY id;")
        self.ids["data_table"].row_data=[tuple(row) for row in data]

    def add_shipper(self, instance):
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "add_shipper_window.py"]))
        th1.start()
        th1.join()
        self.shipper_update()

    def shipper(self):
        def on_check_press(instance, row_data):
            print(row_data)
            data = get_data.get_data_from_dt(
                query="SELECT * FROM Поставщик ORDER BY id;")
            for row in data:
                if test.list_coincidence([str(col) for col in row], row_data):
                    f = open("shipper.txt", "w")
                    for col in row:
                        f.write(str(col) + ";")
                    f.close()
            th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "edit_shipper_window.py"]))
            th1.start()
            th1.join()
            self.shipper_update()

        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data, data_col = get_data.get_data_from_dt(
            query="SELECT Название, Телефон FROM Поставщик ORDER BY id",
            get_col_names=True)
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                ("Название", dp(75)),
                ("Телефон", dp(75)),
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )
        data_table.bind(on_check_press=on_check_press)
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_fullname = MDTextField(
            id="tf_fullname",
            mode="round",
            hint_text="Название",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_fullname"] = tf_fullname
        card.add_widget(tf_fullname)

        tf_phone_num = MDTextField(
            id="tf_phone_num",
            mode="round",
            hint_text="Тел.: +7(777)777-77-77",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_phone_num"] = tf_phone_num
        card.add_widget(tf_phone_num)

        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_shipper)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.clear_shipper)
        card.add_widget(clear_button)
        add_button = MDRaisedButton(
            text="Добавить поставщика",
            pos_hint={"center_x": 0.5},
        )
        add_button.bind(on_press=self.add_shipper)
        card.add_widget(add_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=1,
            )
        )
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def supply_update(self):
        data = get_data.get_data_from_dt("SELECT Поставщик.Название, Поставка1.idАвтомобиля, Поставка1.Количество, Поставка1.Дата FROM Поставка1 JOIN Поставщик ON Поставка1.idПоставщика=Поставщик.id ORDER BY Поставка1.idАвтомобиля;")
        self.ids["data_table"] = [tuple(row) for row in data]

    def search_supply(self, instance):
        cl_fullname = self.ids["tf_fullname"].text
        auto_id = self.ids["tf_auto_id"].text
        date_start = self.ids["tf_date_start"].text
        date_end = self.ids["tf_date_end"].text

        values = []
        query = "SELECT Поставщик.Название, Поставка1.idАвтомобиля, Поставка1.Количество, Поставка1.Дата FROM Поставка1 JOIN Поставщик ON Поставка1.idПоставщика=Поставщик.id WHERE Поставщик.id=Поставщик.id"

        if auto_id != "":
            query += " and Поставка1.idАвтомобиля = %s"
            values.append(int(auto_id))

        if date_start != "":
            if test.is_right_date(date_start):
                query += " and Поставка1.Дата >= %s"
                values += [date_start]
            else:
                self.ids["tf_date_start"].text = ""
                self.ids["tf_date_start"].hint_text = "Формат: гггг-мм-дд"

        if date_end != "":
            if test.is_right_date(date_end):
                query += " and Поставка1.Дата <= %s"
                values += [date_end]
            else:
                self.ids["tf_date_end"].text = ""
                self.ids["tf_date_end"].hint_text = "Формат: гггг-мм-дд"

        data = get_data.get_data_vals(query, values)

        if cl_fullname != "":
            data1 = []
            for row in data:
                if cl_fullname.lower() in row[0].lower():
                    data1.append(row)
            data = data1

        self.ids["data_table"].row_data = [tuple(row) for row in data] + [("", "", "", "")]

    def clear_supply(self, instance):
        self.ids["tf_fullname"].text = ""
        self.ids["tf_auto_id"].text = ""
        self.ids["tf_date_start"].text = ""
        self.ids["tf_date_end"].text = ""

    def add_supply(self, instance):
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "add_supply_window.py"]))
        th1.start()
        th1.join()
        self.supply_update()

    def supply(self):
        def on_check_press(instance, row_data):
            print(row_data)
            data = get_data.get_data_from_dt(
                query="SELECT Поставка1.id,Поставщик.Название, Поставка1.idАвтомобиля, Поставка1.Количество, Поставка1.Дата FROM Поставка1 JOIN Поставщик ON Поставка1.idПоставщика=Поставщик.id ORDER BY Поставка1.idАвтомобиля;")
            for row in data:
                if test.list_coincidence([str(col) for col in row], row_data):
                    f = open("supply.txt", "w")
                    for col in row:
                        f.write(str(col) + ";")
                    f.close()
            th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "edit_supply_window.py"]))
            th1.start()
            th1.join()
            self.supply_update()

        layout = BoxLayout()
        table_layout = BoxLayout()
        table_layout.id = "table_layout"
        search_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.9),
        )
        search_layout.id = "search_layout"
        data, data_col = get_data.get_data_from_dt(
            query="SELECT Поставщик.Название, Поставка1.idАвтомобиля, Поставка1.Количество, Поставка1.Дата FROM Поставка1 JOIN Поставщик ON Поставка1.idПоставщика=Поставщик.id ORDER BY Поставка1.idАвтомобиля;",
            get_col_names=True)
        data_table = MDDataTable(
            rows_num=10,
            pos_hint={"left": 1, "top": 0.9},
            size_hint_y=0.9,
            use_pagination=True,
            check=True,
            column_data=[
                ("Название", dp(55)),
                ("idАвтомобиля", dp(35)),
                ("Количество", dp(35)),
                ("Дата", dp(35)),
            ],
            row_data=[
                tuple(row) for row in data
            ],
            sorted_order="ASC",
            elevation=2,
        )
        data_table.bind(on_check_press=on_check_press)
        self.ids["data_table"] = data_table
        table_layout.id = "table_layout"
        table_layout.add_widget(data_table)
        self.ids["table_layout"] = table_layout
        layout.add_widget(table_layout)

        card = MDCard(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "top": 1},
            padding=10,
            spacing=10,
            orientation='vertical',
        )
        card.id = "id"
        label = MDLabel(
            text="Поиск",
            id="search_label",
            font_size=20,
            halign='center',
            size_hint_y=None,
            pos_hint={"top": 1},
            padding_y=15,
        )
        self.ids["search_label"] = label
        label.id = "search_label"
        card.add_widget(label)

        tf_fullname = MDTextField(
            id="tf_fullname",
            mode="round",
            hint_text="Название",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_fullname"] = tf_fullname
        card.add_widget(tf_fullname)

        tf_auto_id = MDTextField(
            id="tf_auto_id",
            mode="round",
            hint_text="idАвтомобиля",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_auto_id"] = tf_auto_id
        card.add_widget(tf_auto_id)

        date_layout_start = BoxLayout(
            size_hint_x=0.7,
            size_hint_y=0.2,
            pos_hint={"center_x": 0.5},
        )
        date_button_start = MDIconButton(
            icon="calendar.png",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["date_button_start"] = date_button_start
        tf_date_start = MDTextField(
            mode="round",
            hint_text="Начало: гггг-мм-дд",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_date_start"] = tf_date_start
        date_button_start.bind(on_press=self.show_sales_date_picker)
        date_layout_start.add_widget(tf_date_start)
        date_layout_start.add_widget(date_button_start)
        card.add_widget(date_layout_start)
        date_layout_end = BoxLayout(
            size_hint_x=0.7,
            size_hint_y=0.2,
            pos_hint={"center_x": 0.5},
        )
        date_button_end = MDIconButton(
            icon="calendar.png",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["date_button_end"] = date_button_end
        tf_date_end = MDTextField(
            mode="round",
            hint_text="Конец: гггг-мм-дд",
            size_hint_x=0.7,
            font_size=18,
            pos_hint={"center_x": 0.5},
        )
        self.ids["tf_date_end"] = tf_date_end
        date_button_end.bind(on_press=self.show_sales_date_picker)
        date_layout_end.add_widget(tf_date_end)
        date_layout_end.add_widget(date_button_end)
        card.add_widget(date_layout_end)

        search_button = MDRoundFlatButton(
            text="Найти",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        search_button.bind(on_press=self.search_supply)
        self.ids["search_button"] = search_button
        card.add_widget(search_button)
        clear_button = MDRoundFlatButton(
            text="Очистить",
            font_size=12,
            pos_hint={"center_x": 0.5},
        )
        self.ids["clear_button"] = clear_button
        clear_button.bind(on_press=self.clear_supply)
        card.add_widget(clear_button)
        add_button = MDRaisedButton(
            text="Добавить поставку",
            pos_hint={"center_x": 0.5},
        )
        add_button.bind(on_press=self.add_supply)
        card.add_widget(add_button)
        card.add_widget(
            BoxLayout(
                size_hint_y=1,
            )
        )
        self.ids["card"] = card
        search_layout.add_widget(card)
        layout.add_widget(search_layout)
        self.ids["container_layout"] = layout
        self.ids["search_layout"] = search_layout
        self.add_widget(layout)

    def clear_analyses(self):
        files = ["emp.txt", "emp_time.txt", "auto_id.txt", "auto_time.txt"]
        for file in files:
            f = open(file, "w")
            f.close()

    def sales_analisys(self):
        self.clear_analyses()
        th1 = threading.Thread(target=lambda *largs: subprocess.run([sys.executable, "sales_analisys.py"]))
        th1.start()
        th1.join()


class WindowManager(ScreenManager):
    pass


class AutosalonApp(MDApp):
    def build(self):
        Window.size = (1400, 1000)
        self.theme_cls.theme_style = theme.theme_style
        self.theme_cls.primary_palette = theme.primary_palette
        return Builder.load_file("autosalon.kv")

    def logger(self):
        user = self.root.ids["login"]
        username = user.username.text.lower()
        password = user.password.text
        query = "SELECT Сотрудник.ФИО, Сотрудник.Должность, Аутентификация.Логин, Аутентификация.password, Сотрудник.id  FROM Аутентификация JOIN Сотрудник ON Аутентификация.idСотрудника=Сотрудник.id;"
        data = get_data.get_data_from_dt(query)
        flag = True
        for row in data:
            if username == row[2].lower() and password == row[3]:
                flag = False
                if row[1].lower() == "администратор":
                    user.manager.transition = NoTransition()
                    f = open("user.txt", "w")
                    f.write(str(row[-1]))
                    f.close()
                    self.root.current = "admin"
                elif row[1].lower() == "продовец-консультант":
                    user.manager.transition = NoTransition()
                    f = open("user.txt", "w")
                    f.write(str(row[-1]))
                    f.close()
                    self.root.current = "sales"
                    print(row)
        if flag:
            user.errorLabel.text = "Неправильный логин или пароль!"
            user.errorLabel.text_color = "#FF0000"

    def clear(self):
        login = self.root.ids['login'].ids['username']
        login.text = ""
        password = self.root.ids['login'].ids['password']
        password.text = ""


if __name__ == "__main__":
    AutosalonApp().run()
