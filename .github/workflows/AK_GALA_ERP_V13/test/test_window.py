import sys
from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QGridLayout, QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy

)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QCursor, QFont

LANGUAGES = {
    "ru": {
        "sidebar_sklad": "<b>ТОВАРЫ</b><br><span style='font-size:11px; color:#8E939E;'>Управление товаром и складом</span> ",
        "sidebar_sales": "<b>ПРОДАЖИ</b><br><span style='font-size:11px; color:#8E939E;'>Продажи, клиенты и расчеты </span> ",
        "sidebar_analytics": "<b>АНАЛИТИКА</b><br><span style='font-size:11px; color:#8E939E;'>Отчёты и аналитика магазина</span> ",
        "sidebar_settings":"Настройки системы ",

        "top_sales": "Сегодня продаж:",
        "top_stock": "Товаров на складе:",
        "top_debt_client": "Долги клиентов:",
        "top_debt_supplier": "Долги поставшикам:",

        "dash_title": "ДОБРО ПОЖАЛОВАТЬ!",
        "dash_subtitle": "Выберите раздел для работы",

        "card_1":"<b>НОВАЯ ПРОДАЖА</b><span style='font-size:11px; color:#8E939E;'>Перейти к оформлению<br>новой продажи</span>",
        "card_2":"<b>ПРИХОД ТОВАРА</b><span style='font-size:11px; color:#8E939E;'>Добавить новый приход<br>на склад</span>",
        "card_3":"<b>ВСЕ ТОВАРЫ</b><span style='font-size:11px; color:#8E939E;'>Просмотр управление<br>товарами</span>",
        "card_4":"<b>КЛИЕНТЫ</b><span style='font-size:11px; color:#8E939E;'>Клиенты и база<br>должников</span>",
        "card_5":"<b>ОТЧЕТЫ</b><span style='font-size:11px; color:#8E939E;'>Просмотр отчетов<br>и аналитики</span>",
        "card_6":"<b>ТОВАРЫ НА ИСХОДЕ</b><span style='font-size:11px; color:#8E939E;'>Список товаров с низким<br>остатком</span>",
        "card_7":"<b>ПЕЧЕТЬ ЧЕКОВ</b><span style='font-size:11px; color:#8E939E;'>Печать последного<br>чека</span>",
        "card_8":"<b>Н</b><span style='font-size:11px; color:#8E939E;'>Перейти к оформлению<br>новой продажи</span>",

    }
}