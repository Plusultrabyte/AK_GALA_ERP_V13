
import os
import sys
from unittest import expectedFailure

from PyQt6.QtCore import QMargins


from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer, QDateTime

from twilio.rest import Client

from PyQt6.QtCharts import (
    QBarCategoryAxis,
    QBarSeries,
    QBarSet,
    QPieSeries
)



from PyQt6.QtWidgets import (
    QDateEdit,

)
from PyQt6.QtCharts import  QChart, QChartView,  QValueAxis

from PyQt6.QtGui import  QLinearGradient, QPen

# 🔌 DATABASE INTEGRATION (With robust fallback mock data)
try:
    from core.database import add_product, get_all_products, delete_product, complete_order, add_item_to_order, sell, \
        get_daily_sales
except ImportError:
    print("⚠️ DATABASE WARNING: Using high-fidelity mockup database.")
    _mock_db = [
        (1, "Цемент М-500 (45 кг)", "Строительные смеси", 12.00, 18.50, 120, 10),
        (2, "Арматура 12мм (метр)", "Металлопрокат", 3.10, 4.20, 850, 50),
        (3, "Краска Dulux Белая (10л)", "Лакокрасочные", 220.00, 320.00, 15, 5),
        (4, "Шпатлевка Knauf (25 кг)", "Строительные смеси", 30.00, 45.00, 43, 8),
        (5, "Гипсокартон Knauf 9.5мм", "Листовые материалы", 45.00, 65.00, 90, 15)
    ]


    def add_product(name, category, purchase_price, selling_price, stock, min_stock):
        new_id = len(_mock_db) + 1
        _mock_db.append((new_id, name, category, purchase_price, selling_price, stock, min_stock))


    def get_all_products():
        return _mock_db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# If main_window.py is inside the 'ui' folder, step up one level:
if os.path.basename(BASE_DIR) == "ui":
    BASE_DIR = os.path.dirname(BASE_DIR)

ANALYTICS_FILE = os.path.join(BASE_DIR, "analytics_data.json")
# 🌐 MULTILINGUAL DICTIONARY (Russian & Turkmen)
LANGUAGES = {
    "ru": {
        "app_title": "BUILD STORE PRO",
        "app_version": "V15 PRO",
        "sidebar_sklad_title": "ТОВАРЫ",
        "sidebar_sklad_sub": "Управление и склад",
        "sidebar_sales_title": "ПРОДАЖИ",
        "sidebar_sales_sub": "Оформление и клиенты",
        "sidebar_analytics_title": "АНАЛИТИКА",
        "sidebar_analytics_sub": "Отчеты магазина",
        "sidebar_settings": "⚙️ Настройки",
        "sidebar_lang": "🌐 Язык: RU",
        "top_sales": "Сегодня продаж:",
        "top_stock": "Товаров на складе:",
        "top_debt_client": "Долги клиентов:",
        "top_debt_supplier": "Долги поставщикам:",
        "top_user": "Пользователь:",
        "top_role": "Администратор",
        "dash_title": "ДОБРО ПОЖАЛОВАТЬ!",
        "dash_subtitle": "Выберите раздел для работы в меню",
        "card_1": "НОВАЯ ПРОДАЖА", "card_1_sub": "Перейти к оформлению новой продажи",
        "card_2": "ПРИХОД ТОВАРА", "card_2_sub": "Добавить новый приход на склад",
        "card_3": "ВСЕ ТОВАРЫ", "card_3_sub": "Просмотр и управление товарами",
        "card_4": "КЛИЕНТЫ", "card_4_sub": "Клиенты и база должников",
        "card_5": "ОТЧЕТЫ", "card_5_sub": "Просмотр отчетов и аналитики",
        "card_6": "ТОВАРЫ НА ИСХОДЕ", "card_6_sub": "Список товаров с низким остатком",
        "card_7": "ПЕЧАТЬ ЧЕКА", "card_7_sub": "Печать последнего чека",
        "card_8": "НАСТРОЙКИ", "card_8_sub": "Настройки программы и магазина",
        "backup_title": "Резервное копирование",
        "backup_sub": "Ваши данные надежно защищены",
        "backup_last": "Последнее копирование:",
        "backup_btn": "Создать сейчас",
        "sklad_title": "УПРАВЛЕНИЕ СКЛАДОМ",
        "sklad_subtitle": "Мониторинг остатков, добавление и редактирование товаров",
        "sklad_search": "Поиск по наименованию или артикулу...",
        "sklad_add_btn": "+ Новый товар",
        "sklad_back_btn": "← В меню",
        "sklad_th_id": "ID",
        "sklad_th_name": "Наименование товара",
        "sklad_th_category": "Категория",
        "sklad_th_p_price": "Закупка",
        "sklad_th_s_price": "Продажа",
        "sklad_th_qty": "Остаток",
        "sklad_th_min_qty": "Мин. остаток",
        # Analytics Translations
        "compare": "Сравнить",
        "filter": "Показать",
        "details": "Подробная информация о продажах",
        "top_sold": "Самые продаваемые товары",
        "time": "Время",
        "item_name": "Наименование товара",
        "quantity": "Количество",
        "price": "Цена",
        "total": "Итого",
        "customer": "Клиент",
        "payment": "Оплата",
        "today": "Сегодня",
        "specific_date": "Конкретная дата",
        "last_7_days": "Последние 7 дней",
        "last_30_days": "Последние 30 дней",
        "this_year": "Этот год",
        "all_time": "За все время",
        "net_profit": "Чистая прибыль (Торговля - Приход)",
        "gross_sales": "Общие продажи (Реализация)",
        "client_debt": "Долги клиентов (Нам)",
        "store_debt": "Долги предприятия (Кому)",
        "weekly_comparison": "Еженедельное сравнение",
        "days": ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
        "distribution2": "Распределение",
        "clients": "Клиенты",
        "store": "Предприятие",
        "debts_title": "Долги (В кредит)",

        # Payment Pop-up Translations
        "pay_debt_title": "Оплата долга",
        "name_label": "Имя",
        "your_debt": "Ваш долг",
        "pay_amount": "Сумма оплаты...",
        "paid_btn": "Оплачено ✔"

    },
    "tm": {
        "app_title": "BUILD STORE PRO",
        "app_version": "V15 PRO",
        "sidebar_sklad_title": "HARYTLAR",
        "sidebar_sklad_sub": "Haryt we ammar",
        "sidebar_sales_title": "SÖWDA",
        "sidebar_sales_sub": "Söwda we müşderiler",
        "sidebar_analytics_title": "ANALITIKA",
        "sidebar_analytics_sub": "Hasabatlar we analitika",
        "sidebar_settings": "⚙️ Sazlamalar",
        "sidebar_lang": "🌐 Dil: TM",
        "top_sales": "Şügünki söwda:",
        "top_stock": "Ammardaky harytlar:",
        "top_debt_client": "Müşderi bergileri:",
        "top_debt_supplier": "Kärhana bergileri:",
        "top_user": "Ulanyjy:",
        "top_role": "Administraton",
        "dash_title": "AMMAR DOLANDYRYŞY",
        "dash_subtitle": "Galyndylary gözegçilikde saklamak, täze haryt goşmak we redaktirlemek",
        "card_1": "TÄZE SÖWDA", "card_1_sub": "Söwda resmileşdirmäge geçmek",
        "card_2": "KABUL ETMEK", "card_2_sub": "Ammara täze haryt kabul etmek",
        "card_3": "ÄHLI HARYTLAR", "card_3_sub": "Harytlary dolandyrmak we görmek",
        "card_4": "MÜŞDERILER", "card_4_sub": "Müşderiler we bergiler bazasy",
        "card_5": "HASABATLAR", "card_5_sub": "Hasabatlary we analitikany görmek",
        "card_6": "GUTARYP BARÝAN", "card_6_sub": "Galyndysy az harytlaryň sanawy",
        "card_7": "ÇEK ÇAP", "card_7_sub": "Soňky çegi çap etmek",
        "card_8": "SAZLAMALAR", "card_8_sub": "Ulgam we dükan sazlamalary",
        "backup_title": "Ätiýaçlyk nusgalama",
        "backup_sub": "Maglumatlaryňyz ygtybarly goralýar",
        "backup_last": "Soňky nusgalama:",
        "backup_btn": "Nusga döretmek",
        "sklad_title": "AMMAR DOLANDYRYŞY",
        "sklad_subtitle": "Galyndylary gözegçilikde saklamak, täze haryt goşmak we redaktirlemek",
        "sklad_search": "Haryt ady ýa-da artikuly boýunça gözleg...",
        "sklad_add_btn": "+ Täze haryt goşmak",
        "sklad_back_btn": "← Menýuwa dolanmak",
        "sklad_th_id": "ID",
        "sklad_th_name": "Harydyň ady",
        "sklad_th_category": "Kategoriýa",
        "sklad_th_p_price": "Alyş bahasy",
        "sklad_th_s_price": "Satuw bahasy",
        "sklad_th_qty": "Galyndy",

        "sklad_th_min_qty": "Min. galyndy",

        # Analytics Translations
        "analytics_title": "ANALITIKA HASABATLARY",

        "debtors_total": "Müşderi borçlary:",

        "pie_distribution": "PAÝLANŞYK",
        "top_products_title": "IŇ KÖP SATYLAN HARYTLAR",
        "debtors_list_title": "MÜŞDERI BERGILERI",
        "th_product": "Haryt",
        "th_qty": "Sany",
        "th_revenue": "Girdeji",
        "th_name": "Ady",
        "th_debt": "Bergi",
        "th_phone": "Telefon",
        "daily_sales": {"ru": "Дневные продажи", "tm": "Gündelik satuw"},
        "debtors": {"ru": "Müşderi borçlary", "tm": "Müşderi borçlary"},
        "sales_growth": {"ru": "РОСТ ПРОДАЖ", "tm": "SÖWDA ÖSÜŞI"},
        "distribution": {"ru": "РАСПРЕДЕЛЕНИЕ", "tm": "PAÝLANŞYK"},
        "prod_header": {"ru": ["Товар", "Кол-во", "Выручка"], "tm": ["Haryt", "Sany", "Girdeji"]},
        "debt_header": {"ru": ["Имя", "Долг", "Телефон"], "tm": ["Ady", "Bergi", "Telefon"]},
        "compare": "Deňeşdir",
        "filter": "Görkez",
        "details": "Söwda barada jikme-jik maglumat",
        "top_sold": "Iň köp satylan harytlar",
        "time": "Wagty",
        "item_name": "Harydyň ady",
        "quantity": "Sany",
        "price": "Bahasy",
        "total": "Jemi",
        "customer": "Müşderi",
        "payment": "Töleg",
        "today": "Bugün",
        "specific_date": "Aýratyn sene",
        "last_7_days": "Soňky 7 gün",
        "last_30_days": "Soňky 30 gün",
        "this_year": "Şu ýyl",
        "all_time": "Ähli döwür",
        "net_profit": "Arassa Peýda (Söwda - Alnan)",
        "gross_sales": "Jemi Söwda (Satylyş)",
        "client_debt": "Müşderi Bergisi (Bize)",
        "store_debt": "Kärhana Bergisi (Kimiňki)",
        "weekly_comparison": "Hepdelik deňeşdirme",
        "days": ["Du", "Si", "Çar", "Pen", "An", "Şen", "Ýek"],
        "distribution2": "Paýlanşyk",
        "clients": "Müşderiler",
        "store": "Kärhana",
        "debts_title": "Bergiler (Nesiýe)",

        # Payment Pop-up Translations
        "pay_debt_title": "Nesiýäni Tölemek",
        "name_label": "Ady",
        "your_debt": "Garzyňyz",
        "pay_amount": "Töleg mukdary...",
        "paid_btn": "Tölendi ✔"
    },

}

from PyQt6.QtWidgets import (
    QWidget, QFrame

)

from PyQt6.QtGui import QFont

# Database module import
import core.database as db





class AnalyticsWidget(QWidget):
    """
    Full Analytics Dashboard: Connects live numbers directly from
    database aggregate calculations and renders KPI cards + transactions table.
    """

    def __init__(self, main_window, parent=None):
        super().__init__(parent)

        self.main_window = main_window
        self.init_ui()
        self.refresh_analytics()

    def init_ui(self):
        self.setWindowTitle("Analitika we Hasabat")
        self.resize(1200, 850)

        # Pure Black 🐈‍⬛ + Neon Green 🍏 Theme
        self.setStyleSheet(
            """
            QDialog {
                background-color: #08090C;
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
            }

            /* Top Header Card */
            #HeaderFrame {
                background-color: #111319;
                border-radius: 12px;
                padding: 8px 16px;
                border: 1px solid #1E222D;
            }

            /* Date Inputs */
            QDateEdit {
                background-color: #191C26;
                color: #00FF66;
                border: 1px solid #2A2F3D;
                border-radius: 8px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QDateEdit:hover {
                border: 2px solid #00FF66;
                border-radius: 14px; /* Corner radius expands on hover 💚 */
                background-color: #1E2330;
            }

            QDateEdit::drop-down {
                border: none;
                width: 20px;
            }

            /* ==========================================
            QCALENDARWIDGET POPUP STYLING 🗓️
            ========================================== */
            QCalendarWidget QWidget {
                alternate-background-color: #111319;
                color: #00FF66;
            }
        
            /* Header Bar (Month & Year) */
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #111319;
                border-bottom: 1px solid #1E222D;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }

            /* Month Navigation Arrows */
            QCalendarWidget QToolButton {
                color: #00FF66;
                background-color: transparent;
                font-weight: bold;
                border-radius: 6px;
                padding: 4px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #191C26;
                border: 1px solid #00FF66;
            }
            QCalendarWidget QToolButton::menu-indicator {
                image: none;
            }

            /* Calendar Grid & Numbers */
            QCalendarWidget QTableView {
                background-color: #08090C;
                color: #00FF66; /* Neon Green Day Numbers */
                selection-background-color: #00FF66; /* Active Selection */
                selection-color: #000000;
                gridline-color: #1E222D;
                border: 1px solid #1E222D;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                font-size: 13px;
                font-weight: bold;
            }

            /* Day Name Headers (Du, Si, Çar...) */
            QCalendarWidget QHeaderView::section {
                background-color: #111319;
                color: #7A8294;
                font-weight: bold;
                font-size: 12px;
                border: none;
                padding: 6px;
            }
   

            /* Quick Filter Preset Buttons */
            QPushButton.filter-btn {
                background-color: #191C26;
                color: #7A8294;
                border: 1px solid #2A2F3D;
                border-radius: 8px;
                padding: 7px 14px;
                font-weight: 600;
            }
            QPushButton.filter-btn:hover {
                background-color: #252A38;
                color: #00FF66;
                border-color: #00FF66;
            }

            /* Action Buttons */
            #BtnFilter {
                background-color: #00FF66;
                color: #000000;
                font-weight: bold;
                border-radius: 8px;
                padding: 7px 18px;
                border: none;
            }
            #BtnFilter:hover {
                background-color: #00CC52;
            }

                    #BtnDetails {
            background-color: #191C26;
            color: #00FF66;
            font-weight: bold;
            border-radius: 8px;
            padding: 7px 16px;
            border: 1px solid #00FF66;
        }
        #BtnDetails:hover {
            background-color: #00FF66;
            color: #000000;
        }

        /* Container Frames */
        QFrame.table-card {
            background-color: #111319;
            border-radius: 14px;
            border: 1px solid #1E222D;
            padding: 12px;
        }
        QLabel.section-title {
            color: #00FF66;
            font-size: 15px;
            font-weight: bold;
            margin-bottom: 6px;
        }

        /* QTableWidget Dark Style */
        QTableWidget {
            background-color: #111319;
            gridline-color: #1E222D;
            color: #E1E2EC;
            border: none;
            border-radius: 8px;
            font-size: 13px;
        }
        QTableWidget::item {
            padding: 6px;
            border-bottom: 1px solid #191C26;
        }
        QTableWidget::item:selected {
            background-color: #191C26;
            color: #00FF66;
        }
        QHeaderView::section {
            background-color: #191C26;
            color: #7A8294;
            font-weight: bold;
            font-size: 12px;
            border: none;
            padding: 8px;
        }
    """
        )

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(14)
        from PyQt6.QtGui import QTextCharFormat
        def setup_calendar_weekends(date_edit_widget):
            """Sets a custom color for Saturday and Sunday inside the popup calendar"""
            calendar = date_edit_widget.calendarWidget()

            # Weekend text format (e.g., Soft Red / Coral)
            weekend_format = QTextCharFormat()
            weekend_format.setForeground(QColor("#FF5555"))  # Soft red for weekends 🔴
            weekend_format.setFontWeight(700)

            # Apply to Saturday and Sunday
            calendar.setWeekdayTextFormat(Qt.DayOfWeek.Saturday, weekend_format)
            calendar.setWeekdayTextFormat(Qt.DayOfWeek.Sunday, weekend_format)



        # ==========================================
        # 1. TOP HEADER TOOLBAR
        # ==========================================
        header_frame = QFrame()
        header_frame.setObjectName("HeaderFrame")
        header_layout = QHBoxLayout(header_frame)



        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())



        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.start_date.dateChanged.connect(self.on_custom_date_range_changed)
        self.end_date.dateChanged.connect(self.on_custom_date_range_changed)
        # Call this in init_ui after date edits are created:
        setup_calendar_weekends(self.start_date)
        setup_calendar_weekends(self.end_date)
        # 1. CREATE DROPDOWN WIDGET
        self.range_picker = QComboBox()
        self.range_picker.addItems([
            "Bugün",
            "Aýratyn sene",
            "Soňky 7 gün",
            "Soňky 30 gün",
            "Soňky 3 aý",
            "Şu ýyl",
            "Ähli döwür"
        ])

        self.range_picker.setMinimumWidth(180)
        self.range_picker.setFixedHeight(40)


        self.range_picker.setStyleSheet("""
            QComboBox {
                background-color: #252530;
                color: #FFFFFF;
                border: 1px solid #3F3F4E;
                border-radius: 8px;
                padding: 5px 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QComboBox:hover {
                border: 1px solid #00E676; /* Cool green highlight on hover */
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: none;
            }
            QComboBox QAbstractItemView {
                background-color: #252530;
                color: #FFFFFF;
                selection-background-color: #00E676; /* Green selection */
                selection-color: #000000; /* Black text when selected */
                border: 1px solid #3F3F4E;
                border-radius: 4px;
                outline: none; /* Removes the dotted focus line */
            }
        """)

        # 2. CALENDAR PICKER
        self.date_picker = QDateEdit()
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDisplayFormat("yyyy-MM-dd")
        self.date_picker.setDate(QDate.currentDate())

        # 3. CONNECT SIGNALS (NO DUPLICATES)
        self.range_picker.currentIndexChanged.connect(self.refresh_analytics)

        # Only connect date_picker to on_calendar_date_changed (it will handle refresh)
        self.date_picker.dateChanged.connect(self.on_calendar_date_changed)

        # --- Create the Compare Button ---
        self.btn_compare = QPushButton("⚖️ Deňeşdir")
        self.btn_compare.setFixedHeight(40)
        self.btn_compare.setStyleSheet("""
            QPushButton {
                background-color: #252530;
                color: #FFFFFF;
                border: 1px solid #3F3F4E;
                border-radius: 8px;
                padding: 5px 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                border: 1px solid #00E676; /* Glows green on hover */
                color: #00E676;
            }
        """)

        # Connect it to the function that opens the window
        self.btn_compare.clicked.connect(self.open_comparison_dialog)




        # Action Buttons
        self.btn_filter = QPushButton("Görkez")
        self.btn_filter.setObjectName("BtnFilter")

        self.btn_details = QPushButton("Söwda barada jikme-jik maglumat")
        self.btn_details.setObjectName("BtnDetails")
        self.btn_details.clicked.connect(
            lambda _=False: ProductInsightsDialog(
                db=db,
                start_date=self.start_date.date(),
                end_date=self.end_date.date(),
                parent=self
            ).exec()
        )


        header_layout.addWidget(self.btn_compare)
        header_layout.addSpacing(15)
        header_layout.addWidget(self.range_picker)
        header_layout.addWidget(self.date_picker)
        header_layout.addWidget(self.btn_details)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_filter)
        header_layout.addWidget(self.btn_details)

        main_layout.addWidget(header_frame)

        dashboard_layout = QVBoxLayout()
        dashboard_layout.setSpacing(14)

        # ------------------------------------------
        # TOP ROW: 50 / 50 Split (Do not touch these charts!)
        # ------------------------------------------
        top_row = QHBoxLayout()
        top_row.setSpacing(14)
        top_row.addWidget(self.create_summary_cards(), stretch=1)
        top_row.addWidget(self.create_bar_chart(), stretch=1)

        # ------------------------------------------
        # BOTTOM ROW: ~65 / 35 Split (Table vs Pie Chart)
        # ------------------------------------------
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(14)

        # --- LEFT: Top Sold Items Table ---
        sold_items_card = QFrame()
        sold_items_card.setProperty("class", "table-card")
        v_sold = QVBoxLayout(sold_items_card)
        v_sold.setContentsMargins(10, 10, 10, 10)

        self.lbl_sold_title = QLabel("📦 Iň köp satylan harytlar")
        self.lbl_sold_title.setProperty("class", "section-title")

        self.table_sold_items = QTableWidget()
        headers = ["#", "Wagty", "Harydyň ady", "Sany", "Bahasy", "Jemi", "Müşderi", "Töleg"]
        self.table_sold_items.setColumnCount(len(headers))
        self.table_sold_items.setHorizontalHeaderLabels(headers)

        # Configure header column sizing to fit 8 columns cleanly
        header = self.table_sold_items.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # #
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Wagty
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Harydyň ady (Stretches to fill space)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Sany
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Bahasy
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Jemi
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Müşderi
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # Töleg

        self.table_sold_items.verticalHeader().hide()
        self.table_sold_items.verticalHeader().setDefaultSectionSize(30)



        v_sold.addWidget(self.lbl_sold_title)
        v_sold.addWidget(self.table_sold_items)

        # Stretch=2 gives the table ~66% of the bottom width
        bottom_row.addWidget(sold_items_card, stretch=2)

        # --- RIGHT: Product Distribution Donut Chart ---
        # Stretch=1 gives the pie chart ~33% of the bottom width
        bottom_row.addWidget(self.create_pie_chart(), stretch=1)

        # Add the rows to the main dashboard layout
        dashboard_layout.addLayout(top_row, stretch=1)
        dashboard_layout.addLayout(bottom_row, stretch=1)

        main_layout.addLayout(dashboard_layout, stretch=1)

    def on_custom_date_range_changed(self):
        """Watari Check 1: Triggers when the user clicks the calendar widgets."""
        if hasattr(self, "start_date") and hasattr(self, "end_date"):
            if self.start_date.date() > self.end_date.date():
                self.end_date.blockSignals(True)
                self.end_date.setDate(self.start_date.date())
                self.end_date.blockSignals(False)

        if hasattr(self, "range_picker"):
            self.range_picker.blockSignals(True)
            self.range_picker.setCurrentText("Aýratyn sene")
            self.range_picker.blockSignals(False)

        # This MUST call refresh_analytics to continue the chain
        self.refresh_analytics()



    # ==========================================
    # CHART BUILDER HELPER METHODS
    # ==========================================




    def create_bar_chart(self):
        """Chart 2: Neon Gradient Bar Chart - Dynamic Weekly Data"""
        self.bar_set = QBarSet("Söwda")

        # Bar Gradient (Cyan to Neon Green)
        bar_gradient = QLinearGradient(0.5, 0.0, 0.5, 1.0)
        bar_gradient.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectMode)
        bar_gradient.setColorAt(0.0, QColor("#00FF66"))  # Top Neon Green
        bar_gradient.setColorAt(1.0, QColor("#008844"))  # Bottom Forest Green

        self.bar_set.setBrush(bar_gradient)
        self.bar_set.setPen(QPen(QColor("#00FF66"), 1))

        # --- DYNAMIC DATA EXTRACTION ---
        weekly_totals = [0.0] * 7
        try:
            # Read the live analytics file
            with open(ANALYTICS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            today = date.today()
            from datetime import timedelta
            # Calculate the exact date of Monday for the current week
            monday = today - timedelta(days=today.weekday())

            # Loop through Monday (0) to Sunday (6)
            for i in range(7):
                current_day = monday + timedelta(days=i)
                date_str = current_day.strftime("%Y-%m-%d")

                # Check if the date exists in the JSON data
                if date_str in data:
                    # Extract the day's total sales
                    weekly_totals[i] = data[date_str].get("total", 0.0)

        except Exception as e:
            print(f"Watari log: Error loading weekly chart data: {e}")
            # Fallback to zeroes if the file hasn't been created yet
            weekly_totals = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.bar_set.append(weekly_totals)

        self.bar_series = QBarSeries()
        self.bar_series.append(self.bar_set)

        chart = QChart()
        chart.addSeries(self.bar_series)
        chart.legend().hide()
        chart.setBackgroundVisible(False)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # X-Axis setup
        categories = ["Du", "Si", "Çar", "Pen", "An", "Şen", "Ýek"]
        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(categories)
        self.axis_x.setGridLineColor(QColor("#1E222D"))
        self.axis_x.setLabelsColor(QColor("#7A8294"))
        chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.bar_series.attachAxis(self.axis_x)

        # Y-Axis setup
        self.bar_axis_y = QValueAxis()
        self.bar_axis_y.setGridLineColor(QColor("#1E222D"))
        self.bar_axis_y.setLabelsColor(QColor("#7A8294"))

        max_val = max(weekly_totals) if max(weekly_totals) > 0 else 100
        self.bar_axis_y.setRange(0, max_val * 1.2)

        chart.addAxis(self.bar_axis_y, Qt.AlignmentFlag.AlignLeft)
        self.bar_series.attachAxis(self.bar_axis_y)

        view = QChartView(chart)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        view.setStyleSheet("background: transparent;")

        card = QFrame()
        card.setProperty("class", "table-card")
        layout = QVBoxLayout(card)

        self.lbl = QLabel("📊 Hepdelik deñeşdirme")
        self.lbl.setProperty("class", "section-title")

        layout.addWidget(self.lbl)
        layout.addWidget(view)
        return card

    def update_weekly_chart(self, reference_date=None):
        """Watari Check 3: The final visual update for the bars."""
        import json
        from datetime import date, timedelta
        from PyQt6.QtCore import QDate


        if not hasattr(self, 'bar_set'):
            print("Watari Alert: self.bar_set does not exist. Chart cannot update!")
            return

        # Safely convert to Python date
        if reference_date is None:
            reference_date = date.today()
        elif isinstance(reference_date, QDate):
            reference_date = date(reference_date.year(), reference_date.month(), reference_date.day())

        weekly_totals = [0.0] * 7
        try:
            with open(ANALYTICS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Calculate Monday for the selected date
            monday = reference_date - timedelta(days=reference_date.weekday())

            for i in range(7):
                current_day = monday + timedelta(days=i)
                date_str = str(current_day)  # Auto-formats to YYYY-MM-DD

                if date_str in data:
                    weekly_totals[i] = float(data[date_str].get("total", 0.0))

        except Exception as e:
            print(f"Watari Alert [update_weekly_chart read error]: {e}")

        try:
            # Redraw the bars dynamically
            for i, total in enumerate(weekly_totals):
                self.bar_set.replace(i, total)

            # Rescale the height dynamically
            if hasattr(self, 'bar_axis_y'):
                max_val = max(weekly_totals) if max(weekly_totals) > 0 else 100
                self.bar_axis_y.setRange(0, max_val * 1.2)

            print(f"Watari Success: Chart repainted for week {monday} -> {weekly_totals}")

        except Exception as e:
            print(f"Watari Alert [update_weekly_chart draw error]: {e}")
    def on_pie_slice_clicked(self, slice_item):
        label_text = slice_item.label()

        # 🔴 1. EXPAND TO DEBT VIEW (FIRST TIME CLICK FROM MAIN DONUT)
        if not getattr(self, 'is_debt_view', False) and (
                "nesiye" in label_text.lower() or "bergi" in label_text.lower() or "долг" in label_text.lower()):
            self.is_debt_view = True
            self.rebuild_debt_pie_chart()

            if hasattr(self, 'lbl_paylansyk'):
                self.lbl_paylansyk.setText("🔴 Bergiler (Nesiýe)")
                self.lbl_paylansyk.setStyleSheet("color: #FF4444; font-weight: bold;")
        elif getattr(self, 'is_debt_view', False):
            # If clicking "..." or "Beýlekiler", return to the main chart view
            if label_text in ["...", "Beýlekiler"]:
                self.is_debt_view = False
                self.refresh_analytics()
                return

            # --- SECOND CLICK ON SAME DEBT ITEM: OPEN POPUP ---
            if getattr(self, 'selected_debt_name', None) == label_text:
                # FIX 1: Removed "default=" to stop the crash!
                debt_amount = self.display_debts.get(label_text, 0.0)

                # FIX 2: Dynamic language variables
                lang = getattr(self, 'current_lang', 'tm')
                title_text = "Оплата долга" if lang == "ru" else "Nesiýäni Tölemek"
                name_text = "Имя:" if lang == "ru" else "Ady:"
                debt_text = "Ваш долг:" if lang == "ru" else "Garzyňyz:"
                placeholder_text = "Сумма оплаты..." if lang == "ru" else "Töleg mukdary..."
                btn_text = "Оплачено ✔" if lang == "ru" else "Tölendi ✔"

                dialog = QDialog(self)
                # Apply the translation to the window title
                dialog.setWindowTitle(title_text)
                dialog.setFixedSize(320, 250)
                dialog.setStyleSheet("background-color: #1e1e1e; border-radius: 10px;")

                layout = QVBoxLayout(dialog)

                # Top Row: Ady + x Button
                top_layout = QHBoxLayout()
                # Apply translation to Name
                lbl_name = QLabel(f"{name_text} {label_text}", dialog)
                lbl_name.setStyleSheet("color: white; font-weight: bold; font-size: 15px;")

                btn_close = QPushButton("x", dialog)
                btn_close.setFixedSize(30, 30)
                btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
                btn_close.setStyleSheet(
                        "background-color: #444; color: white; font-size: 18px; border-radius: 15px;")
                btn_close.clicked.connect(dialog.reject)

                top_layout.addWidget(lbl_name)
                top_layout.addStretch()
                top_layout.addWidget(btn_close)
                layout.addLayout(top_layout)

                # Middle Row: Garzyňyz
                # Apply translation to Debt Amount
                lbl_debt = QLabel(f"{debt_text} {debt_amount:.2f} TMT", dialog)
                lbl_debt.setStyleSheet("#ff4444; font-size: 14px; margin-top: 10px;")
                layout.addWidget(lbl_debt)

                # Input box for Partial Payments
                input_pay = QLineEdit(dialog)
                # Apply translation to Placeholder
                input_pay.setPlaceholderText(placeholder_text)
                input_pay.setText(str(debt_amount))
                input_pay.setStyleSheet(
                "background-color: #222; color: white; padding: 5px; border-radius: 4px; border: 1px solid #555;"
                )
                layout.addWidget(input_pay)

                # Bottom Row: Tölendi Button
                # Apply translation to Pay button
                btn_pay = QPushButton(btn_text, dialog)

                btn_pay.setCursor(Qt.CursorShape.PointingHandCursor)
                # Increased padding and font-size to make it BIGGER
                btn_pay.setStyleSheet("""
                    QPushButton {
                        background-color: #00FF66;
                        color: black;
                        font-weight: bold;
                        font-size: 18px; 
                        border-radius: 6px;
                        padding: 15px; 
                        margin-top: 15px;
                    }
                    QPushButton:hover { background-color: #00cc55; }
                """)

                # Upgraded process_payment to read the input box!
                def process_payment():
                    try:
                        # Read the typed amount
                        pay_amount = float(input_pay.text().strip() or 0.0)
                        if pay_amount > 0:

                            # --- NEW LOGIC: Check which chart is currently active! ---
                            if getattr(self, 'viewing_client_debts', False):
                                # 👥 We are in Müşderiler (Client) mode
                                self.pay_client_debt_in_json(label_text, pay_amount)
                            else:
                                # 🏢 We are in Kärhana (Store) mode
                                self.pay_debt_in_json(label_text, pay_amount)
                            # ---------------------------------------------------------

                            self.selected_debt_name = None
                            dialog.accept()
                            self.refresh_analytics()

                    except ValueError:
                        pass  # Ignore if they type letters instead of numbers

                btn_pay.clicked.connect(process_payment)
                layout.addWidget(btn_pay)

                dialog.exec()

            else:
                # --- FIRST CLICK: HIGHLIGHT SELECTED SLICE ---
                self.selected_debt_name = label_text
                for s in self.pie_series.slices():
                    if s.label() == label_text:
                        s.setExploded(True)
                        s.setBorderColor(QColor("#00FF66"))
                        s.setBorderWidth(3)
                    else:
                        s.setExploded(False)
                        s.setBorderColor(QColor("#FFFFFF"))
                        s.setBorderWidth(1)

    def rebuild_debt_pie_chart(self):
        self.pie_series.clear()
        self.pie_series.setPieSize(0.62)
        self.pie_series.setHoleSize(0.35)

        if hasattr(self, 'chart'):
            self.chart.setMargins(QMargins(5, 5, 5, 5))

        debts = getattr(self, 'display_debts', {})
        if not debts or sum(debts.values()) <= 0.01:
            self.is_debt_view = False
            self.refresh_analytics()
            return

        red_shades = ["#FF2222", "#FF4444", "#FF6666", "#FF8888", "#FFAAAA", "#FFCCCC", "#880000"]

        for idx, (item_name, item_amount) in enumerate(debts.items()):
            s = self.pie_series.append(f"{item_name}", item_amount)
            if item_name in ["...", "Beýlekiler"]:
                s.setColor(QColor("#777777"))
            else:
                s.setColor(QColor(red_shades[idx % len(red_shades)]))
            s.setLabelVisible(False)

    def pay_debt_in_json(self, target_name, pay_amount):
        file_path = "analytics_data.json"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for date_str, stats in data.items():
                if isinstance(stats, dict) and "store_debt_history" in stats:
                    remaining_history = []
                    actual_deduction = 0.0

                    for item in stats["store_debt_history"]:
                        if item.get("prod_name") == target_name:
                            current_debt = float(item.get("debt_amount", 0.0))
                            new_debt = current_debt - pay_amount

                            if new_debt > 0:
                                # 1. Partial payment: Keep item, update the debt amount
                                item["debt_amount"] = new_debt
                                remaining_history.append(item)
                                actual_deduction += pay_amount
                            else:
                                # 2. Fully paid: Do not append to remaining_history
                                actual_deduction += current_debt
                        else:
                            remaining_history.append(item)

                    stats["store_debt_history"] = remaining_history
                    # Safely reduce the master store_debt total
                    stats["store_debt"] = max(0.0, float(stats.get("store_debt", 0.0)) - actual_deduction)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"JSON Save Error: {e}")

    def pay_client_debt_in_json(self, client_name, pay_amount):
        import json
        import os

        file_path = "analytics_data.json"
        if not os.path.exists(file_path):
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            remaining_payment = float(pay_amount)

            # Loop through EVERY day in the JSON
            for date_str, stats in data.items():
                if remaining_payment <= 0:
                    break  # We finished deducting the payment!

                # Check if this day has client debts
                if isinstance(stats, dict) and "client_debts" in stats:
                    # Check if our specific client owes money on this day
                    if client_name in stats["client_debts"]:
                        current_debt = float(stats["client_debts"][client_name])

                        if current_debt > 0:
                            # Figure out how much we can deduct from this specific day
                            deduction = min(current_debt, remaining_payment)

                            # 1. Deduct from the specific client
                            stats["client_debts"][client_name] -= deduction

                            # 2. NEW: Deduct from the daily master debt_amount for the top card!
                            if "debt_amount" in stats:
                                current_master_debt = float(stats["debt_amount"])
                                stats["debt_amount"] = max(0.0, current_master_debt - deduction)

                            remaining_payment -= deduction

                            # Clean up: If they fully paid off this day's debt, remove them from this day
                            if stats["client_debts"][client_name] <= 0:
                                del stats["client_debts"][client_name]

            # Save the cleanly updated data back to the JSON file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print(f"💰 Successfully paid {pay_amount} TMT for {client_name}! Master debt updated.")

        except Exception as e:
            print(f"JSON Client Payment Error: {e}")
    def create_pie_chart(self):
        """Chart 3: Donut chart showing top sold products & debt distribution"""
        self.pie_series = QPieSeries()
        self.pie_series.setHoleSize(0.48)  # Donut inner cutout

        # Click signal listener setup
        self.pie_series.clicked.connect(self.on_pie_slice_clicked)
        self.is_debt_view = False

        # Turn off labels on the slices themselves for a clean look
        for slice_item in self.pie_series.slices():
            slice_item.setLabelVisible(False)

        chart = QChart()
        chart.addSeries(self.pie_series)
        chart.setBackgroundVisible(False)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setMargins(QMargins(0, 0, 0, 0))

        # Interactive legend setup
        legend = chart.legend()
        legend.setVisible(True)
        legend.setAlignment(Qt.AlignmentFlag.AlignRight)
        legend.setLabelColor(QColor("#FFFFFF"))
        legend.setFont(QFont("Segoe UI", 9))
        legend.setMarkerShape(legend.MarkerShape.MarkerShapeCircle)

        # Chart View setup
        view = QChartView(chart)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        view.setStyleSheet("background: transparent;")

        # --- CARD CONTAINER FIX ---
        card = QFrame()  # Must be QFrame, not QChartView!
        card.setProperty("class", "table-card")

        layout = QVBoxLayout(card)

        # Store label on self so on_pie_slice_clicked can change it dynamically
        self.lbl_paylansyk = QLabel("🍩 Paýlanşyk")
        self.lbl_paylansyk.setProperty("class", "section-title")

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.lbl_paylansyk)

        # Add a flexible spacer so the button is pushed to the far right
        header_layout.addStretch()

        # Create the switch button
        self.btn_switch_debt = QPushButton("🔄 Müşderiler")
        self.btn_switch_debt.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_switch_debt.setStyleSheet("""
            QPushButton {
                background-color: #2D2D30; 
                color: #00FF66; 
                border-radius: 6px; 
                padding: 4px 10px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #3E3E42; }
        """)
        self.btn_switch_debt.clicked.connect(self.toggle_debt_mode)
        header_layout.addWidget(self.btn_switch_debt)

        # Add the header row and the chart to the main card layout
        layout.addLayout(header_layout)
        layout.addWidget(view)

        # Set our starting state variable
        self.viewing_client_debts = False

        return card

    def toggle_debt_mode(self):
        self.viewing_client_debts = not getattr(self, 'viewing_client_debts', False)

        # 1. Grab the current language
        lang = getattr(self, 'current_lang', 'tm')

        # 2. Safely apply translations based on the language
        if self.viewing_client_debts:
            btn_text = "🏢 Предприятие" if lang == "ru" else "🏢 Kärhana"
            lbl_text = "Долги клиентов (Нам) 👥" if lang == "ru" else "Müşderi Bergisi (Bize) 👥"

            self.btn_switch_debt.setText(btn_text)
            self.lbl_paylansyk.setText(lbl_text)
            self.lbl_paylansyk.setStyleSheet("color: #00BFFF; font-weight: bold;")
        else:
            btn_text = "👥 Клиенты" if lang == "ru" else "👥 Müşderiler"
            lbl_text = "🍩 РАСПРЕДЕЛЕНИЕ" if lang == "ru" else "🍩 PAÝLANŞYK"

            self.btn_switch_debt.setText(btn_text)
            self.lbl_paylansyk.setText(lbl_text)
            self.lbl_paylansyk.setStyleSheet("")

        self.is_debt_view = False
        self.refresh_analytics()
    def open_insights_dialog(self):
        # 1. Safely retrieve start and end dates from your widget controls
        start_date = None
        end_date = None

        for attr in ['date_start', 'start_date', 'date_from', 'start_date_edit']:
            if hasattr(self, attr):
                widget = getattr(self, attr)
                if hasattr(widget, 'date'):
                    start_date = widget.date()
                    break

        for attr in ['date_end', 'end_date', 'date_to', 'end_date_edit']:
            if hasattr(self, attr):
                widget = getattr(self, attr)
                if hasattr(widget, 'date'):
                    end_date = widget.date()
                    break

        # 2. Launch the dialog
        dialog = ProductInsightsDialog(
            db=db,
            analytics_data=None,  # Automatically loads fresh JSON inside load_data()
            start_date=start_date,
            end_date=end_date,
            parent=self
        )
        dialog.exec()
    def on_calendar_date_changed(self):
        """When user interacts with the calendar, set dropdown to 'Aýratyn sene'"""
        if hasattr(self, "range_picker"):
            # Block signals temporarily to prevent double refreshing
            self.range_picker.blockSignals(True)
            self.range_picker.setCurrentText("Aýratyn sene")
            self.range_picker.blockSignals(False)

        self.refresh_analytics()

    def load_history_to_table(self, data: dict, start_date, end_date):
        # 1. Directly target the EXACT table you created (no guessing!)
        table = self.table_sold_items

        if not table:
            return

        headers = ["#", "Wagty", "Harydyň ady", "Sany", "Bahasy", "Jemi", "Müşderi", "Töleg"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(0)

        row = 0
        for date_str, stats in data.items():
            # Skip if there's no history array
            if not isinstance(stats, dict) or "history" not in stats:
                continue

            try:
                # Convert string date to a datetime date object for comparison
                rec_date = datetime.strptime(date_str, "%Y-%m-%d").date()

                # Check if it falls within our dropdown range
                if start_date <= rec_date <= end_date:
                    for item in stats["history"]:
                        table.insertRow(row)

                        # Safely convert to float so bad data doesn't crash the table
                        try:
                            price_val = float(item.get('price', 0))
                            total_val = float(item.get('total', 0))
                        except (ValueError, TypeError):
                            price_val = 0.0
                            total_val = 0.0

                        table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                        table.setItem(row, 1, QTableWidgetItem(f"{item.get('date', date_str)} {item.get('time', '')}"))
                        table.setItem(row, 2, QTableWidgetItem(str(item.get('name', 'Nätanyş'))))
                        table.setItem(row, 3, QTableWidgetItem(str(item.get('qty', 1))))
                        table.setItem(row, 4, QTableWidgetItem(f"{price_val:.2f} m"))
                        table.setItem(row, 5, QTableWidgetItem(f"{total_val:.2f} m"))
                        table.setItem(row, 6, QTableWidgetItem(str(item.get('client', 'Nätanyş'))))
                        table.setItem(row, 7, QTableWidgetItem(str(item.get('payment', 'Nagt'))))

                        row += 1

            except Exception as e:
                # If there's an error with the date format, print it instead of silently failing
                print(f"Error loading table for date {date_str}: {e}")
                continue

    def create_summary_cards(self):
        """4 Real-time Financial Cards in a Beautiful 2x2 Grid"""
        from PyQt6.QtWidgets import QFrame, QGridLayout, QVBoxLayout, QLabel
        from PyQt6.QtCore import Qt

        # Container for all 4 cards
        container = QFrame()

        # USE QGridLayout for the perfect 2x2 design
        layout = QGridLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        def build_card(title, color_hex):
            card = QFrame()
            # Added a subtle border and slightly rounded edges for a premium look
            card.setStyleSheet("""
                QFrame {
                    background-color: #1E222D;
                    border-radius: 12px;
                    border: 1px solid #2B3040;
                }
            """)

            vbox = QVBoxLayout(card)
            # Give the text some breathing room inside the square cards
            vbox.setContentsMargins(20, 25, 20, 25)
            vbox.setSpacing(10)

            lbl_title = QLabel(title)
            lbl_title.setWordWrap(True)
            # Slightly larger font (15px) for the square layout
            lbl_title.setStyleSheet("color: #7A8294; font-size: 15px; font-weight: bold; border: none;")

            lbl_value = QLabel("0.00 m")
            # Bumped value font to 24px so it pops!
            lbl_value.setStyleSheet(f"color: {color_hex}; font-size: 24px; font-weight: bold; border: none;")
            lbl_value.setAlignment(Qt.AlignmentFlag.AlignLeft)

            vbox.addWidget(lbl_title)
            vbox.addWidget(lbl_value)

            # Vertically center the text inside the card perfectly
            vbox.setAlignment(Qt.AlignmentFlag.AlignVCenter)

            # We must return BOTH the card (to place in grid) and the label (to update later)
            return card, lbl_title, lbl_value

        # Create the 4 cards
        card_1,self.lbl_net_profit_title, self.card_real_profit = build_card("Arassa Peýda (Söwda - Alnan)", "#00FF66")
        card_2,self.lbl_total_sales_title, self.card_total_sales = build_card("Jemi Söwda (Satylyş)", "#00EAFF")
        card_3, self.lbl_client_debt_title, self.card_customer_debt = build_card("Müşderi Bergisi (Bize)", "#FFAA00")
        card_4,self.lbl_store_debt_title, self.card_store_debt = build_card("Kärhana Bergisi (Kimiňki)", "#FF4444")

        # Place them in the 2x2 Grid Layout (row, column)
        layout.addWidget(card_1, 0, 0) # Top Left
        layout.addWidget(card_2, 0, 1) # Top Right
        layout.addWidget(card_3, 1, 0) # Bottom Left
        layout.addWidget(card_4, 1, 1) # Bottom Right

        # Guarantee the grid stretches completely evenly (25% each card)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)

        return container
    def open_comparison_dialog(self):
        # ANALYTICS_FILE is the variable you mentioned holding your JSON path
        dialog = CompareDatesDialog(ANALYTICS_FILE, self)
        dialog.exec()
    def return_to_main_donut(self):
        """Resets the view back to the main Paýlanyşyk donut chart."""
        self.is_debt_view = False

        # Revert the label back to its original state
        if hasattr(self, 'lbl_paylansyk'):
            self.lbl_paylansyk.setText("Paýlanyşyk 🍩")
            # Reset the style to your default (e.g., removing the red bold text)
            self.lbl_paylansyk.setStyleSheet("")

            # Rebuild the main chart
        self.refresh_analytics()
    def refresh_analytics(self):
        try:
            import json
            import os
            from datetime import datetime, timedelta, date
            from PyQt6.QtCore import QDate
            from PyQt6.QtGui import QColor

            analytics_file = ANALYTICS_FILE

            # 1. READ ALL RECORDS FROM JSON
            data = {}
            if os.path.exists(analytics_file):
                try:
                    with open(analytics_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    data = {}

            # 2. DETERMINE DATE RANGE BASED ON DROPDOWN SELECTION

            selected_option = self.range_picker.currentText().strip()
            today = date.today()

            # Handle both "Bugün" and "Bügün" spellings safely
            if selected_option in ["Bugün", "Bügün"]:
                start_date = today
                end_date = today
            elif selected_option == "Aýratyn sene":
                # Read the exact date from your single date picker
                q_date = self.date_picker.date()
                chosen_date = date(q_date.year(), q_date.month(), q_date.day())

                # Since we are checking one specific day, start and end are the same
                start_date = chosen_date
                end_date = chosen_date


            elif selected_option == "Soňky 7 gün":
                start_date = today - timedelta(days=7)
                end_date = today

            elif selected_option == "Soňky 30 gün":
                start_date = today - timedelta(days=30)
                end_date = today

            elif selected_option == "Soňky 3 aý":
                start_date = today - timedelta(days=90)
                end_date = today

            elif selected_option == "Şu ýyl":
                start_date = date(today.year, 1, 1)
                end_date = today

            else:  # "Ähli döwür"
                start_date = date(1970, 1, 1)
                end_date = today

            # Synchronize Calendar Widget without triggering extra signals
            if selected_option != "Aýratyn sene":
                self.date_picker.blockSignals(True)

                # Update the UI date picker to match the dynamically chosen start_date
                self.date_picker.setDate(QDate(start_date.year, start_date.month, start_date.day))

                self.date_picker.blockSignals(False)

            # Reload data into your table widget
            if hasattr(self, "analytics_data") and self.analytics_data:
                self.load_history_to_table(self.analytics_data, start_date, end_date)
            self.update_weekly_chart(end_date)



            # 4. ACCUMULATE STATS FOR [start_date <= record_date <= end_date]
            v_total = 0.0
            v_items = 0
            v_debt = 0.0
            v_sales = 0
            v_store_debt = 0.0
            v_real_profit = 0.0  # <--- Add this new variable


            purchase_prices = {}
            try:
                products = get_all_products()
                for p in products:
                    # p[1] is name, p[3] is purchase_price based on your database photo
                    purchase_prices[p[1]] = float(p[3])
            except Exception as e:
                print(f"Error loading products for profit calculation: {e}")
            # Include global store debt if saved at root level
            if "global_store_debt" in data:
                try:
                    v_store_debt += float(data["global_store_debt"])
                except (ValueError, TypeError):
                    pass

            self.debt_products = {}
            for date_str, stats in data.items():
                if date_str == "global_store_debt" or not isinstance(stats, dict):
                    continue

                try:
                    # 1. THE FOREVER DATE FIX ♾️
                    clean_date = str(date_str).split(" ")[0].split("T")[0]
                    record_date = datetime.strptime(clean_date, "%Y-%m-%d").date()

                    # 2. COLLECT DEBTS FOR ALL TIME (Outside the date filter so it NEVER forgets)
                    for item in stats.get("store_debt_history", []):
                        p_name = item.get("prod_name", "Nätanyş Haryt")
                        d_amt = float(item.get("debt_amount", 0.0))
                        if d_amt > 0:
                            self.debt_products[p_name] = self.debt_products.get(p_name, 0.0) + d_amt

                    # 3. DATE-FILTERED STATS (Only for the selected calendar dates)
                    if start_date <= record_date <= end_date:
                        v_total += float(stats.get("total", 0.0))
                        v_items += int(stats.get("sold_items", 0))
                        v_debt += float(stats.get("debt_amount", 0.0))
                        v_sales += int(stats.get("sale_count", 0))

                        # --- CALCULATE TRUE PROFIT ---
                        daily_history = stats.get("history", [])
                        for sale in daily_history:
                            name = sale.get("name", "")
                            qty = int(sale.get("qty", 0))
                            selling_price = float(sale.get("price", 0.0))

                            # Get purchase price from DB dictionary (defaults to 0.0 if not found)
                            buy_price = purchase_prices.get(name, 0.0)

                            # Your exact formula: (Bahasy - Alnan bahasy) * Sany
                            item_profit = (selling_price - buy_price) * qty
                            v_real_profit += item_profit

                except ValueError:
                    continue

            # 🛑 OUTSIDE THE LOOP! (Make sure this touches the left wall of your function) 🛑

            # 4. FORCE THE RED SLICE TO USE ALL-TIME DEBT 🔴
            v_store_debt = sum(self.debt_products.values())
            self.v_debt = v_store_debt

            # Calculate green slice (Tölenen) for the selected period
            v_real_money = max(0.0, v_total - v_debt)
            self.v_real_money = v_real_money

            # 5. SORT DEBTS & RENAME "..." TO "Beýlekiler" (Fixes the blank dot in your 4th image!)
            sorted_debts = sorted(self.debt_products.items(), key=lambda x: x[1], reverse=True)
            self.display_debts = {}

            if len(sorted_debts) > 6:
                for name, amount in sorted_debts[:6]:
                    self.display_debts[name] = amount
                self.display_debts["Beýlekiler"] = sum(amount for _, amount in sorted_debts[6:])
            else:
                self.display_debts = dict(sorted_debts)

            # Keep your table loading function intact!
            self.load_history_to_table(data, start_date, end_date)

            # 5. UPDATE UI CARDS SAFELY
            if hasattr(self, "lbl_store_debt"):
                self.lbl_store_debt.setText(f"{v_store_debt:.2f} m")

            cards = []
            for attr in dir(self):
                if "card" in attr.lower():
                    obj = getattr(self, attr)
                    if hasattr(obj, "setValue") or hasattr(obj, "setText"):
                        cards.append(obj)




                # Update the newly created layout cards dynamically
                if hasattr(self, 'card_real_profit'):
                    self.card_real_profit.setText(f"{v_real_profit:.2f} m")
                if hasattr(self, 'card_total_sales'):
                    self.card_total_sales.setText(f"{v_total:.2f} m")
                if hasattr(self, 'card_customer_debt'):
                    self.card_customer_debt.setText(f"{v_debt:.2f} m")
                if hasattr(self, 'card_store_debt'):
                    self.card_store_debt.setText(f"{v_store_debt:.2f} m")
                # 6. DRAW DONUT CHART
                if hasattr(self, 'pie_series'):
                    self.pie_series.clear()

                    t_total = v_total

                    t_paid = t_total

                    if getattr(self, 'viewing_client_debts', False):
                        # --- ♾️ FOREVER DEBT READER START ♾️ ---
                        import os, json
                        all_time_debts = {}
                        if os.path.exists("analytics_data.json"):
                            try:
                                with open("analytics_data.json", "r", encoding="utf-8") as f:
                                    data = json.load(f)
                                    # Loop through EVERY day in history to find all debts
                                    for date_key, stats in data.items():
                                        if isinstance(stats, dict) and "client_debts" in stats:
                                            for name, amount in stats["client_debts"].items():
                                                all_time_debts[name] = all_time_debts.get(name, 0.0) + float(amount)
                            except Exception as e:
                                print(f"Error reading forever debts: {e}")

                        # Filter out people who paid off their debt completely (> 0)
                        self.display_debts = {k: v for k, v in all_time_debts.items() if v > 0}

                        # Update the main chart total to be the ALL-TIME total!
                        t_debt = sum(self.display_debts.values())
                    lang = getattr(self, 'current_lang', 'tm')
                    client_lbl = "Долги клиентов" if lang == "ru" else "Müşderi bergisi"
                    store_lbl = "Долги предприятия" if lang == "ru" else "Kärhana bergisi"
                    paid_lbl = "Оплачено" if lang == "ru" else "Tölenen"

                    if getattr(self, 'viewing_client_debts', False):
                        t_debt = sum(self.display_debts.values())
                        debt_label = client_lbl  # Use dynamic label
                        debt_color = "#00BFFF"
                    else:
                        # Kärhana (Store) debts stay exactly the same!
                        t_debt = v_store_debt
                        debt_label = store_lbl  # Use dynamic label
                        debt_color = "#FF4444"

                    if getattr(self, 'is_debt_view', False) and t_debt <= 0:
                        self.return_to_main_donut()
                    if getattr(self, 'is_debt_view', False):
                        self.rebuild_debt_pie_chart()
                    else:
                        self.pie_series.setPieSize(0.62)
                        self.pie_series.setHoleSize(0.35)

                        if t_paid <= 0 and t_debt <= 0:
                            # Use dynamic label here
                            s_empty = self.pie_series.append(paid_lbl, 1)
                            s_empty.setColor(QColor("#00FF66"))
                        else:
                            if t_paid > 0:
                                # And use dynamic label here!
                                s1 = self.pie_series.append(paid_lbl, t_paid)
                                s1.setColor(QColor("#00FF66"))  # Green paid segment
                            if t_debt > 0:
                                s2 = self.pie_series.append(debt_label, t_debt)
                                s2.setColor(QColor(debt_color))  # Red store debt segment

                        for s in self.pie_series.slices():
                            s.setLabelVisible(False)
            self.update_weekly_chart()
        except Exception as e:
            print(f"❌ Analytics refresh error: {e}")

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_analytics()

    def update_texts(self, current_lang):
        # 1. Pull the correct dictionary
        t = LANGUAGES[current_lang]
        self.current_lang = current_lang

        # 2. Pull the correct dictionary safely
        t = LANGUAGES.get(current_lang, LANGUAGES.get('tm', {}))

        # 3. Instantly translate the stubborn button and title based on the new language
        if getattr(self, 'viewing_client_debts', False):
            self.btn_switch_debt.setText("🏢 Предприятие" if current_lang == "ru" else "🏢 Kärhana")
            self.lbl_paylansyk.setText("Долги клиентов (Нам) 👥" if current_lang == "ru" else "Müşderi Bergisi (Bize) 👥")
        else:
            self.btn_switch_debt.setText("👥 Клиенты" if current_lang == "ru" else "👥 Müşderiler")
            self.lbl_paylansyk.setText("🍩 РАСПРЕДЕЛЕНИЕ" if current_lang == "ru" else "🍩 PAÝLANŞYK")

        # 4. Force the pie chart to redraw so "Tölenen" instantly translates!
        self.refresh_analytics()
        # 2. Update Buttons
        # Retain your emojis by formatting them with the translated text!
        self.btn_compare.setText(f"⚖ {t['compare']}")
        self.btn_filter.setText(t['filter'])
        self.btn_details.setText(t['details'])

        # 3. Update the Title Label (Now that we added self. to it!)
        self.lbl_sold_title.setText(f"📦 {t['top_sold']}")

        # 4. Update Table Headers
        headers = [
            "#",
            t["time"],
            t["item_name"],
            t["quantity"],
            t["price"],
            t["total"],
            t["customer"],
            t["payment"]
        ]
        self.table_sold_items.setHorizontalHeaderLabels(headers)

        # 5. Update Dropdown (Combo Box) Items safely
        # Using setItemText changes the text without resetting the user's current selection!
        self.range_picker.setItemText(0, t["today"])
        self.range_picker.setItemText(1, t["specific_date"])
        self.range_picker.setItemText(2, t["last_7_days"])
        self.range_picker.setItemText(3, t["last_30_days"])
        self.range_picker.setItemText(4, t["this_year"])
        self.range_picker.setItemText(5, t["all_time"])


        self.lbl_net_profit_title.setText(t["net_profit"])
        self.lbl_total_sales_title.setText(t["gross_sales"])
        self.lbl_client_debt_title.setText(t["client_debt"])
        self.lbl_store_debt_title.setText(t["store_debt"])


        self.lbl.setText(f"📊 {t['weekly_comparison']}")
        self.lbl_paylansyk.setText(f"🍩 {t['distribution2']}")

        # 3. Update Bar Chart X-Axis Days

        self.axis_x.clear()
        self.axis_x.append(t["days"])

        # Check current language, default to 'tm' if missing
        lang = getattr(self, 'current_lang', 'tm')

        # Set text based on language
        donut_title = "РАСПРЕДЕЛЕНИЕ" if lang == "ru" else "PAÝLANŞYK"
        self.lbl_paylansyk.setText(f"🍩 {donut_title}")


class CompareDatesDialog(QDialog):
    def __init__(self, analytics_file, parent=None):
        super().__init__(parent)
        super().__init__(parent)
        self.analytics_file = analytics_file

        # --- NEW: Safely get the language from the parent widget ---
        self.lang = getattr(parent, 'current_lang', 'tm') if parent else 'tm'

        # --- Translate Window Title ---
        title_text = "Сравнение дат" if self.lang == "ru" else "Sene Deňeşdirme"
        self.setWindowTitle(title_text)

        self.setFixedSize(550, 350)

        self.setStyleSheet("""
            QDialog { background-color: #1E1E28; }
            QLabel { 
                color: #FFFFFF; 
                font-size: 14px; 
                background-color: transparent;
            }
            QDateEdit {
                background-color: #252530;
                color: #FFFFFF;
                border: 1px solid #3F3F4E;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #00E676;
                color: #000000;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #00C853; }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # --- Top: Date Pickers ---
        date_layout = QHBoxLayout()

        self.date1_picker = QDateEdit(QDate.currentDate().addDays(-1))
        self.date1_picker.setCalendarPopup(True)
        self.date1_picker.setDisplayFormat("yyyy-MM-dd")

        self.date2_picker = QDateEdit(QDate.currentDate())
        self.date2_picker.setCalendarPopup(True)
        self.date2_picker.setDisplayFormat("yyyy-MM-dd")

        # --- NEW: Translated Date Labels ---
        lbl1_text = "Дата 1:" if self.lang == "ru" else "1-nji Sene:"
        lbl_vs_text = "Против" if self.lang == "ru" else "Garşy"
        lbl2_text = "Дата 2:" if self.lang == "ru" else "2-nji Sene:"

        # Style the labels directly for a modern look
        lbl_date1 = QLabel(lbl1_text)
        lbl_date1.setStyleSheet("font-weight: bold; background-color: transparent;")

        lbl_vs = QLabel(lbl_vs_text) # "Vs"
        lbl_vs.setStyleSheet("color: #7A8294; font-weight: bold; background-color: transparent;")
        lbl_vs.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_date2 = QLabel(lbl2_text)
        lbl_date2.setStyleSheet("font-weight: bold; background-color: transparent;")

        # Add them all to the layout
        date_layout.addWidget(lbl_date1)
        date_layout.addWidget(self.date1_picker)
        date_layout.addWidget(lbl_vs)
        date_layout.addWidget(lbl_date2)
        date_layout.addWidget(self.date2_picker)

        # --- Middle: Compare Button ---
        # --- NEW: Translated Button ---
        btn_text = "Сравнить" if self.lang == "ru" else "Deňeşdir (Compare)"
        btn_compare = QPushButton(btn_text)
        btn_compare.clicked.connect(self.run_comparison)

        # --- Bottom: Results Grid ---
        self.results_frame = QFrame()
        self.results_frame.setStyleSheet("background-color: #252530; border-radius: 5px;")
        self.grid = QGridLayout(self.results_frame)

        # --- NEW: Translated Grid Headers ---
        if self.lang == "ru":
            headers = ["Дата", "Общая сумма (m)", "Количество"]
        else:
            headers = ["Sene", "Jemi Söwda (m)", "Satylan sany"]

        for col, text in enumerate(headers):
            lbl = QLabel(text)
            lbl.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            lbl.setStyleSheet("color: #7A8294;")
            self.grid.addWidget(lbl, 0, col)

            # We will populate the rows dynamically in run_comparison

        layout.addLayout(date_layout)
        layout.addWidget(btn_compare)
        layout.addWidget(self.results_frame)
        layout.addStretch()

    def get_day_stats(self, date_str):
        # Read JSON safely
        if not os.path.exists(self.analytics_file):
            return {"total": 0.0, "sale_count": 0}

        try:
            with open(self.analytics_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Return the stats for that date, or empty zeros if date not found
                return data.get(date_str, {"total": 0.0, "sale_count": 0})
        except Exception:
            return {"total": 0.0, "sale_count": 0}

    def run_comparison(self):
        # 1. Get chosen dates as strings
        d1_str = self.date1_picker.date().toString("yyyy-MM-dd")
        d2_str = self.date2_picker.date().toString("yyyy-MM-dd")

        # 2. Fetch data from JSON
        stats1 = self.get_day_stats(d1_str)
        stats2 = self.get_day_stats(d2_str)

        # 3. Clear old results from the grid (skipping row 0 headers)
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget and self.grid.getItemPosition(i)[0] > 0:
                widget.setParent(None)

        # 4. Extract metrics
        t1 = float(stats1.get("total", 0.0))
        t2 = float(stats2.get("total", 0.0))
        s1 = int(stats1.get("sale_count", 0))
        s2 = int(stats2.get("sale_count", 0))

        # --- NEW LOGIC: Find the max sales ever recorded in analytics to use as 100% ---
        max_analytics_sales = 0.0
        try:
            with open(self.analytics_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for date_key, date_stats in data.items():
                    daily_total = float(date_stats.get("total", 0.0))
                    if daily_total > max_analytics_sales:
                        max_analytics_sales = daily_total
        except Exception:
            max_analytics_sales = max(t1, t2)  # Fallback just in case

        if max_analytics_sales == 0:
            max_analytics_sales = 1.0  # Prevent division by zero errors

        if self.lang == "ru":
            date1_display = f"Дата 1 ({d1_str})"
            date2_display = f"Дата 2 ({d2_str})"
        else:
            date1_display = f"1-nji Sene ({d1_str})"
            date2_display = f"2-nji Sene ({d2_str})"

        color1 = "#FFFFFF"  # Default white
        color2 = "#FFFFFF"

        # Determine Winner and Loser based on Total Sales (Jemi Söwda)
        if t1 > t2:
            # 1-nji Sene Wins
            date1_display += " 🏆"
            color1 = "#FFD700"  # Yellow/Gold

            # 2-nji Sene Loses (Calculate % against max ever)
            loser_percent = (t2 / max_analytics_sales) * 100
            if loser_percent < 50:
                color2 = "#FF3B30"  # Emergency Red
            else:
                color2 = "#C0C0C0"  # Silver
                date2_display += " 🥈"

        elif t2 > t1:
            # 2-nji Sene Wins
            date2_display += " 🏆"
            color2 = "#FFD700"  # Yellow/Gold

            # 1-nji Sene Loses (Calculate % against max ever)
            loser_percent = (t1 / max_analytics_sales) * 100
            if loser_percent < 50:
                color1 = "#FF3B30"  # Emergency Red
            else:
                color1 = "#C0C0C0"  # Silver
                date1_display += " 🥈"
        else:
            # Tie
            color1 = "#7A8294"  # Gray
            color2 = "#7A8294"

        # 5. Build the Rows dynamically (Row 3 is completely gone!)

        # Row 1: 1-nji Sene
        lbl_date1 = QLabel(date1_display)
        lbl_date1.setStyleSheet(f"color: {color1}; font-weight: bold;")

        lbl_t1 = QLabel(f"{t1:.2f}")
        lbl_t1.setStyleSheet(f"color: {color1}; font-weight: bold;")

        lbl_s1 = QLabel(f"{s1}")
        lbl_s1.setStyleSheet(f"color: {color1}; font-weight: bold;")

        self.grid.addWidget(lbl_date1, 1, 0)
        self.grid.addWidget(lbl_t1, 1, 1)
        self.grid.addWidget(lbl_s1, 1, 2)

        # Row 2: 2-nji Sene
        lbl_date2 = QLabel(date2_display)
        lbl_date2.setStyleSheet(f"color: {color2}; font-weight: bold;")

        lbl_t2 = QLabel(f"{t2:.2f}")
        lbl_t2.setStyleSheet(f"color: {color2}; font-weight: bold;")

        lbl_s2 = QLabel(f"{s2}")
        lbl_s2.setStyleSheet(f"color: {color2}; font-weight: bold;")

        self.grid.addWidget(lbl_date2, 2, 0)
        self.grid.addWidget(lbl_t2, 2, 1)
        self.grid.addWidget(lbl_s2, 2, 2)

import json
from datetime import datetime, date
from collections import Counter
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QDate, QFileSystemWatcher


class ProductInsightsDialog(QDialog):
    def __init__(self, db, analytics_data=None, start_date=None, end_date=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Söwda barada jikme-jik maglumat")
        self.resize(780, 520)

        self.db = db
        self.start_date = self._to_py_date(start_date)
        self.end_date = self._to_py_date(end_date)

        # 1. Setup UI
        self.init_ui()

        # 2. Live File Watcher for Real-Time Updates
        try:
            self.file_watcher = QFileSystemWatcher(["analytics_data.json"], self)
            self.file_watcher.fileChanged.connect(self.load_data)
        except Exception as e:
            print(f"⚠️ Watcher info: {e}")

        # 3. Initial Data Load
        self.load_data()

    def _to_py_date(self, val):
        if isinstance(val, QDate):
            return date(val.year(), val.month(), val.day())
        elif isinstance(val, str):
            try:
                return datetime.strptime(val, "%Y-%m-%d").date()
            except ValueError:
                return None
        elif isinstance(val, date):
            return val
        return None

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("📊 Haryt we Söwda Analizi", self)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #111827; margin-bottom: 8px;")
        layout.addWidget(title)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #E5E7EB; border-radius: 6px; background: white; }
            QTabBar::tab { background: #F3F4F6; padding: 8px 16px; margin-right: 4px; font-weight: bold; color: #4B5563; }
            QTabBar::tab:selected { background: #2563EB; color: white; }
        """)

        self.table_most_sold = self.create_table()
        self.tabs.addTab(self.table_most_sold, "🔥 Iň köp satylanlar")

        self.table_least_sold = self.create_table()
        self.tabs.addTab(self.table_least_sold, "📉 Iň az satylanlar")

        self.table_restock = self.create_table()
        self.tabs.addTab(self.table_restock, "🚨 Satyn almaly (Gutaryp barýan)")

        layout.addWidget(self.tabs)

        btn_close = QPushButton("Ýap", self)
        btn_close.setStyleSheet(
            "background-color: #EF4444; color: white; font-weight: bold; padding: 8px 20px; border-radius: 6px;")
        btn_close.clicked.connect(self.close)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)

    def create_table(self):
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Harydyň ady", "Sany / Mukdary", "Maglumat"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setStyleSheet("background-color: white; color: #111827; gridline-color: #F3F4F6;")
        return table

    def load_data(self):
        sold_counts = Counter()

        # 1. READ VALUES FROM ANALYTICS_FILE (JSON)
        if os.path.exists(ANALYTICS_FILE):
            try:
                with open(ANALYTICS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Loop through every date entry in the JSON file
                for date_key, stats in data.items():
                    if not isinstance(stats, dict):
                        continue

                    # Check different possible ways history/items might be stored
                    # It could be under 'history' list or directly items
                    transactions = stats.get('history', [])
                    if not transactions and isinstance(stats, list):
                        transactions = stats
                    elif not transactions:
                        # If the date itself contains items or is a transaction list
                        transactions = [stats]

                for item in transactions:  # Look directly at the items in the history list
                    if not isinstance(item, dict):
                        continue

                    name = item.get('name')
                    # Handle different quantity key names
                    qty_val = item.get('qty', item.get('quantity', item.get('sany', 0)))

                    try:
                        qty = int(qty_val)
                    except (ValueError, TypeError):
                        qty = 0

                    if name:
                        sold_counts[name] += qty

            except Exception as e:
                print(f"❌ Analytics JSON read error in insights: {e}")


        print("DEBUG - Aggregated Sold Counts:", sold_counts)



        self.load_all_time_tables()

            # Set text on your UI labels

        # --- POPULATE RESTOCK / LOW STOCK (Satyn almaly / Gutaryp barýan) ---
        try:
            all_products = self.db.get_all_products()
            restock_items = []

            for p in all_products:
                if isinstance(p, dict):
                    name = str(p.get('name', 'Nätanys'))
                    stock = float(p.get('stock', 0))
                    min_stock = float(p.get('min_stock', 5))
                elif hasattr(p, 'keys'): # sqlite3.Row
                    name = str(p['name'])
                    stock = float(p['stock'])
                    min_stock = float(p['min_stock'])
                else: # Tuple format: (id, name, category, purchase_price, selling_price, stock, min_stock)
                    name = str(p[1]) if len(p) > 1 else 'Nätanys'
                    stock = float(p[5]) if len(p) > 5 else 0.0  # Index 5 is stock

                    if len(p) >= 7:
                        min_stock = float(p[6])
                    elif len(p) > 4:
                        min_stock = float(p[4])
                    else:
                        min_stock = 5.0

                if stock <= min_stock:
                    restock_items.append((name, stock))

            self.populate_table(self.table_restock, restock_items, is_sold=False)

        except Exception as e:
            print(f"❌ Database error in insights restock: {e}")

    def populate_table(self, table, data_list, is_sold=True, is_top_list=False):
        # Make sure QBrush is imported alongside QColor and QFont
        from PyQt6.QtGui import QColor, QFont, QBrush

        table.setRowCount(0)
        for row_idx, (name, val) in enumerate(data_list):
            table.insertRow(row_idx)

            prefix = ""
            bg_color = None
            is_top_3 = False

            # --- 1. Only apply Medals & Colors if this is the TOP list ---
            if is_top_list:
                if row_idx == 0:
                    prefix = "🥇 "
                    bg_color = QColor("#FFF4CC")  # Gold
                    is_top_3 = True
                elif row_idx == 1:
                    prefix = "🥈 "
                    bg_color = QColor("#F2F2F2")  # Silver
                    is_top_3 = True
                elif row_idx == 2:
                    prefix = "🥉 "
                    bg_color = QColor("#FCE4D6")  # Bronze
                    is_top_3 = True

            display_name = f"{prefix}{name}"
            item_name = QTableWidgetItem(str(display_name))

            if isinstance(val, dict):
                qty = val.get("qty", 0)
                total = float(val.get("total", 0.0))

                qty_text = f"{qty} sany ({total:.2f} m)"
                status_text = f"Jemi satylan: {qty} sany — {total:.2f} m"
            else:
                qty_text = f"{val} sany"
                status_text = f"Satylan: {val} sany" if is_sold else f"Ammarda galan: {val} sany"

            item_qty = QTableWidgetItem(qty_text)
            item_status = QTableWidgetItem(status_text)

            # --- 3. Apply Styling WITHOUT Errors (Using QBrush) ---
            if is_top_3 and bg_color:
                font = QFont()
                font.setBold(True)
                brush = QBrush(bg_color)  # This fixes the background error!

                for item in (item_name, item_qty, item_status):
                    item.setBackground(brush)
                    item.setFont(font)

            # --- 4. Add Items to Table ---
            table.setItem(row_idx, 0, item_name)
            table.setItem(row_idx, 1, item_qty)
            table.setItem(row_idx, 2, item_status)
    def load_all_time_tables(self):
        if not os.path.exists(ANALYTICS_FILE):
            return

        try:
            with open(ANALYTICS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error loading analytics file: {e}")
            return

        # 1. Aggregate totals across ALL dates in JSON
        item_stats = {}  # {"Item Name": {"qty": total_qty, "total": total_money}}

        if isinstance(data, dict):
            for date_key, date_data in data.items():
                if isinstance(date_data, dict) and "history" in date_data:
                    history = date_data.get("history", [])
                    if isinstance(history, list):
                        for record in history:
                            if isinstance(record, dict):
                                name = record.get("name")
                                qty = int(record.get("qty", 1))
                                total = float(record.get("total", 0.0))

                                if name:
                                    if name not in item_stats:
                                        item_stats[name] = {"qty": 0, "total": 0.0}
                                    item_stats[name]["qty"] += qty
                                    item_stats[name]["total"] += total

        if not item_stats:
            return

        # 2. Sort items by total quantity sold
        # Most sold: Highest quantity first
        sorted_most = sorted(item_stats.items(), key=lambda x: x[1]["qty"], reverse=True)

        # Least sold: Lowest quantity first
        sorted_least = sorted(item_stats.items(), key=lambda x: x[1]["qty"])

        # 3. Populate both table widgets
        self.populate_table(self.table_most_sold, sorted_most, is_sold=True, is_top_list=True)
        self.populate_table(self.table_least_sold, sorted_least, is_sold=True, is_top_list=False)

# =========================================================
# CRASH-FREE TEXT SAFE WRAPPER
# =========================================================
def safe_set_text(widget, text):
    if widget is None:
        return
    try:
        _ = widget.objectName()  # Direct check to see if C++ reference is alive
        if hasattr(widget, "setText"):
            widget.setText(text)
    except RuntimeError:
        pass

def save_sold_items_history( cart_items, client_name="Nätanyş", payment_type="Nagt", sale_total=0.0,debt_amount=0.0):
    """
    Saves each sold product individually by name into analytics_data.json
    cart_items expected format: [{'name': 'Cola 1.5L', 'qty': 2, 'price': 15.0}, ...]
    """
    if not cart_items:
        return

    today_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M")

    records = {}
    if os.path.exists(ANALYTICS_FILE):
        try:
            with open(ANALYTICS_FILE, "r", encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            records = {}

    # Ensure today's record exists
    if today_str not in records:
        records[today_str] = {
            "total": 0.0,
            "sold_items": 0,
            "debt_amount": 0.0,
            "store_debt": 0.0,
            "sale_count": 0,
            "history": []  # 📋 Itemized sales history list
        }

    if "history" not in records[today_str]:
        records[today_str]["history"] = []

    # Append each sold product separately
    for item in cart_items:
        product_name = item.get("name", "Nätanyş haryt")
        quantity = int(item.get("qty", item.get("quantity", 1)))
        unit_price = float(item.get("price", 0.0))
        item_total = float(item.get("total", quantity * unit_price))

        history_entry = {
            "time": time_str,
            "date": today_str,
            "name": product_name,
            "qty": quantity,
            "price": unit_price,
            "total": item_total,
            "client": client_name,
            "payment": payment_type
        }
        records[today_str]["history"].append(history_entry)
        # --- NEW LOGIC: UPDATE DAILY TOTALS ---
        records[today_str]["total"] += float(sale_total)
        records[today_str]["debt_amount"] += float(debt_amount)
        records[today_str]["sale_count"] += 1

        # --- NEW LOGIC: UPDATE CLIENT DEBTS ---
        if float(debt_amount) > 0:
            # Create the client_debts dictionary if it doesn't exist yet
            if "client_debts" not in records[today_str]:
                records[today_str]["client_debts"] = {}

            # Double check the name isn't empty
            if not client_name or client_name.strip() == "":
                client_name = "Nätanyş"

            # Add the new debt to their existing debt
            current_debt = records[today_str]["client_debts"].get(client_name, 0.0)
            records[today_str]["client_debts"][client_name] = current_debt + float(debt_amount)
    # Save to JSON
    with open(ANALYTICS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4)

    print(f"📋 Logged {len(cart_items)} sold items to Sales History!")


from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QScrollArea, QTabWidget, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QLabel)

from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtCore import Qt, QPropertyAnimation, pyqtProperty, QEasingCurve
from PyQt6.QtGui import QPainter, QColor


class AnimatedToggle(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(52, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._bg_off = QColor("#1f242d")
        self._bg_on = QColor("#00ff66")  # Neo Green
        self._handle_color = QColor("#ffffff")
        self._circle_position = 3.0
        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setDuration(220)
        self.stateChanged.connect(self.start_transition)

    def start_transition(self, value):
        self.animation.stop()
        self.animation.setEndValue(self.width() - 25.0 if value else 3.0)
        self.animation.start()

    def get_circle_position(self): return self._circle_position

    def set_circle_position(self, pos):
        self._circle_position = pos
        self.update()

    circle_position = pyqtProperty(float, get_circle_position, set_circle_position)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(self._bg_on if self.isChecked() else self._bg_off)
        p.drawRoundedRect(0, 0, self.width(), self.height(), 14, 14)
        p.setBrush(self._handle_color)
        p.drawEllipse(int(self._circle_position), 3, 22, 22)


class SalesWidget(QWidget):
    def __init__(self, page_index=None, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.lang = "tm"
        self.page_index = page_index
        # Список для хранения связок (виджет_карточки, имя_товара) для быстрого поиска
        self.all_cards = []
        self.setup_ui()


    def setup_ui(self):
        self.carts = [[]]
        self.tables = []

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(15, 15, 15, 15)

        # =================================================================
        # ⬅️ ЛЕВАЯ СТОРОНА: Поиск + Сетка товаров
        # =================================================================
        self.left_panel_container = QWidget()
        self.left_panel = QVBoxLayout(self.left_panel_container)
        self.left_panel.setContentsMargins(0, 0, 0, 0)
        self.left_panel.setSpacing(10)

        # 🔍 ВЕРХНЯЯ ПАНЕЛЬ: Умная строка поиска товара
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Haryt gözle... (Введите название для поиска)")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background-color: #1e222a; 
                color: #eceff4;
                border: 2px solid #2d3139; /* Сделали 2px, чтобы рамка не прыгала */
                border-radius: 10px;
                padding: 12px 15px; 
                font-size: 14px; 
                font-weight: bold;
            }
            /* И при наведении мышки, и при клике внутри — загорается зеленый Итачи-неон */
            QLineEdit:hover, QLineEdit:focus { 
                border: 2px solid #2ecc71; 
                background-color: #242933; 
            }
        """)
        self.search_bar.textChanged.connect(self.filter_products)
        self.left_panel.addWidget(self.search_bar)

        # Скролл-зона для карточек
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        self.scroll_content = QWidget()
        self.tiles_layout = QGridLayout(self.scroll_content)
        self.tiles_layout.setSpacing(15)
        self.tiles_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.scroll_area.setWidget(self.scroll_content)
        self.left_panel.addWidget(self.scroll_area)

        # Отрисовка карточек
        self.load_product_tiles()

        # =================================================================
        # ➡️ ПРАВАЯ СТОРОНА: Корзина чеков, Сумма, Действия
        # =================================================================
        self.right_panel_container = QWidget()
        self.right_panel = QVBoxLayout(self.right_panel_container)
        self.right_panel.setContentsMargins(0, 0, 0, 0)
        self.right_panel.setSpacing(15)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_cart_tab)
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #3b4252; background-color: #2e3440; border-radius: 8px; }
            QTabBar::tab { background: #3b4252; color: #eceff4; padding: 10px 20px; margin-right: 2px; border-top-left-radius: 6px; border-top-right-radius: 6px; font-weight: bold; }
            QTabBar::tab:selected { background: #5e81ac; color: white; }
        """)
        self.right_panel.addWidget(self.tabs)

        # Панель вывода итоговой суммы чека
        self.lbl_total = QLabel("Jemi: 0.00 TMT")
        self.lbl_total.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_total.setStyleSheet("""
            QLabel {
                font-size: 24px; font-weight: bold; color: #a3be8c;
                background-color: #2e3440; padding: 15px;
                border-radius: 8px; border: 1px solid #3b4252;
            }
        """)
        self.right_panel.addWidget(self.lbl_total)

        # Инициализируем стартовый чек
        self.create_tab_ui("Sebet 1")
        checkout_buttons_layout = QHBoxLayout()
        # 🧾 НИЖНЯЯ ПАНЕЛЬ: Кнопка закрытия / отправки готового чека

        # 2. Левая кнопка: Полная оплата наличными
        self.btn_full_checkout = QPushButton("💵 Nagt / Doly Töleg")
        self.btn_full_checkout.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71; 
                color: white; 
                font-weight: bold; 
                padding: 10px; 
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #27ae60; }
        """)
        self.btn_full_checkout.clicked.connect(self.process_full_cash_checkout)

        # 3. Правая кнопка: Запись в долг (Nesiýe)
        self.btn_debt_checkout = QPushButton("📝 Karz Ýazmak")
        self.btn_debt_checkout.setStyleSheet("""
            QPushButton {
                background-color: #e67e22; 
                color: white; 
                font-weight: bold; 
                padding: 10px; 
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #d35400; }
        """)
        self.btn_debt_checkout.clicked.connect(self.process_debt_checkout)
        # 4. Упаковываем кнопки с одинаковым весом stretch=1 (это даст ровно 50% на 50%)
        checkout_buttons_layout.addWidget(self.btn_full_checkout, stretch=1)
        checkout_buttons_layout.addWidget(self.btn_debt_checkout, stretch=1)

        # 5. Добавляем получившуюся строку в твой основной правый макет
        # ВНИМАНИЕ: Проверь, как называется твой вертикальный лейаут справа.
        # Если в коде было self.right_layout.addWidget(self.btn_ceckout), то пишем так:
        self.right_panel.addLayout(checkout_buttons_layout)
        # Системные кнопки навигации
        self.buttons_layout = QHBoxLayout()
        self.btn_back_to_menu = QPushButton("⬅️ Esasy Menýu")
        self.btn_back_to_menu.setStyleSheet(
            "background-color: #bf616a; color: white; padding: 10px; border-radius: 8px; font-weight: bold;")
        self.btn_back_to_menu.clicked.connect(self.go_back_to_menu)

        self.btn_add_tab = QPushButton("+ Täze sebet")
        self.btn_add_tab.setStyleSheet(
            "background-color: #5e81ac; color: white; padding: 10px; border-radius: 8px; font-weight: bold;")
        self.btn_add_tab.clicked.connect(self.add_new_tab)

        self.buttons_layout.addWidget(self.btn_back_to_menu)
        self.buttons_layout.addWidget(self.btn_add_tab)
        self.right_panel.addLayout(self.buttons_layout)

        self.main_layout.addWidget(self.left_panel_container, stretch=6)
        self.main_layout.addWidget(self.right_panel_container, stretch=4)

    # =================================================================
    # ⚙️ ЛОГИКА ФИЛЬТРАЦИИ ПОИСКА
    # =================================================================
    def filter_products(self, text):
        """Сканирует введенный текст и мгновенно перестраивает сетку для видимых карточек"""
        search_text = text.lower().strip()

        # Шаг 1: Убираем ВСЕ карточки из разметки, чтобы сбросить старые позиции ячеек
        for card_widget, _ in self.all_cards:
            self.tiles_layout.removeWidget(card_widget)

        # Шаг 2: Распределяем только подходящие карточки в компактную сетку
        visible_count = 0
        COLUMNS = 3  # Устанавливаем 3 колонки в ряд, как на исходном дизайне

        for card_widget, product_name in self.all_cards:
            if search_text in product_name.lower():
                card_widget.show()

                # Вычисляем новые красивые координаты без пустот и растягиваний
                row = visible_count // COLUMNS
                col = visible_count % COLUMNS

                self.tiles_layout.addWidget(card_widget, row, col)
                visible_count += 1
            else:
                card_widget.hide()

    # =================================================================
    # 📦 ОТРИСОВКА КАРТОЧЕК
    # =================================================================
    def load_product_tiles(self):
        """Generates item tiles by mapping the correct database columns safely"""
        from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
        from PyQt6.QtCore import Qt

        # Clear existing layout components
        for i in reversed(range(self.tiles_layout.count())):
            widget = self.tiles_layout.itemAt(i).widget()
            if widget: widget.deleteLater()

        self.all_cards.clear()

        try:
            from core.database import get_all_products
            warehouse_products = get_all_products()
        except Exception as e:
            print(f"Database access error: {e}")
            return

        row, col = 0, 0
        max_columns = 2

        for product in warehouse_products:
            try:
                # 🧠 MATCHING YOUR EXACT DATABASE STRUCTURE:
                # [0: id, 1: name, 2: category, 3: buy_price, 4: sell_price, 5: stock]
                if isinstance(product, dict):
                    p_id = product.get("id")
                    p_name = product.get("name")
                    p_category = product.get("category", "Haryt")
                    p_price = float(product.get("selling_price", 0))
                    p_stock = int(product.get("stock", 0))
                else:
                    p_id = product[0]
                    p_name = product[1]
                    p_category = product[2] if len(product) > 2 else "Haryt"
                    p_price = float(product[4]) if len(product) > 4 else float(product[2])
                    p_stock = int(product[5]) if len(product) > 5 else int(product[3])

                # Exclude items out of stock
                if p_stock <= 0:
                    continue
                card = QFrame()
                card.setObjectName("ProductCard")
                card.setFixedSize(190, 135)
                card.setCursor(Qt.CursorShape.PointingHandCursor)
                card.setStyleSheet("""
                    QFrame#ProductCard { 
                        background-color: #1e222a; 
                        border: 2px solid #2d3139; /* Сделали 2px по умолчанию */
                        border-radius: 12px; 
                    }
                    /* При наведении включается фирменный зеленый Итачи-неон */
                    QFrame#ProductCard:hover { 
                        border: 2px solid #2ecc71; 
                        background-color: #242933; 
                    }
                """)

                card_layout = QVBoxLayout(card)
                card_layout.setContentsMargins(10, 10, 10, 10)
                card_layout.setSpacing(10)

                img_placeholder = QLabel("📦")
                img_placeholder.setFixedHeight(75)
                img_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
                img_placeholder.setStyleSheet("font-size: 24px; background-color: #2e3440; border-radius: 8px;")
                card_layout.addWidget(img_placeholder)

                info_layout = QHBoxLayout()
                text_layout = QVBoxLayout()

                lbl_name = QLabel(p_name)
                lbl_name.setStyleSheet("color: #eceff4; font-weight: bold; font-size: 13px; background: transparent;")
                lbl_cat = QLabel(str(p_category))
                lbl_cat.setStyleSheet("color: #4c566a; font-size: 11px; background: transparent;")

                text_layout.addWidget(lbl_name)
                text_layout.addWidget(lbl_cat)
                info_layout.addLayout(text_layout, stretch=7)

                lbl_price = QLabel(f"{p_price:.2f}\nTMT")
                lbl_price.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl_price.setStyleSheet(
                    "color: #8fbcbb; font-weight: bold; font-size: 11px; background-color: #2e3440; border-radius: 8px; padding: 5px;")
                info_layout.addWidget(lbl_price, stretch=3)

                card_layout.addLayout(info_layout)
                card.mousePressEvent = lambda event, name=p_name: self.add_to_cart(name)

                self.tiles_layout.addWidget(card, row, col)
                self.all_cards.append((card, p_name))

                col += 1
                if col >= 2:
                    col = 0
                    row += 1
            except Exception as item_err:
                print(f"Skipping problematic product row: {item_err}")
                continue

        self.filter_products(self.search_bar.text())

    # =================================================================
    # 🛒 УПРАВЛЕНИЕ КОРЗИНОЙ И КНОПКАМИ ИЗМЕНЕНИЯ КОЛИЧЕСТВА
    # =================================================================
    def add_to_cart(self, item_name):
        self.change_item_qty_by_name(item_name, 1)

    def change_item_qty_by_name(self, item_name, delta):
        """Manages shopping cart quantity with strict column mappings"""
        current_tab_index = self.tabs.currentIndex()
        if current_tab_index == -1: return

        from core.database import get_all_products
        from PyQt6.QtWidgets import QMessageBox

        warehouse_products = get_all_products()
        target_product = None

        for p in warehouse_products:
            name_check = p.get("name") if isinstance(p, dict) else p[1]
            if name_check == item_name:
                target_product = p
                break

        if not target_product: return

        try:
            if isinstance(target_product, dict):
                p_id = target_product.get("id")
                bahasy = float(target_product.get("selling_price", 0))
                sany_na_skladu = int(target_product.get("stock", 0))
            else:
                p_id = target_product[0]
                # Index 4 is Selling Price, Index 5 is Current Stock
                bahasy = float(target_product[4]) if len(target_product) > 4 else float(target_product[2])
                sany_na_skladu = int(target_product[5]) if len(target_product) > 5 else int(target_product[3])
        except Exception as e:
            print(f"Data conversion crash prevented: {e}")
            return
        current_cart = self.carts[current_tab_index]
        already_in_cart = next((item for item in current_cart if item["name"] == item_name), None)
        already_qty = int(already_in_cart["qty"]) if already_in_cart else 0

        if delta == -1:
            if already_in_cart:
                already_in_cart["qty"] -= 1
                if already_in_cart["qty"] <= 0:
                    current_cart.remove(already_in_cart)
        elif delta == 1:
            if already_qty >= sany_na_skladu:
                QMessageBox.warning(self, "Üns beriň!", "Ammarda ýeterlik haryt ýok!")
                return
            if already_in_cart:
                already_in_cart["qty"] += 1
            else:
                current_cart.append({"id": p_id, "name": item_name, "price": float(bahasy), "qty": 1})

        self.refresh_cart_table()
        db.update_total_price(self)

    def execute_checkout_logic(self, debt_amount, client_name):

        """Единый движок списания склада и логирования транзакции в память"""
        current_tab_index = self.tabs.currentIndex()
        current_cart = self.carts[current_tab_index]

        from PyQt6.QtWidgets import QMessageBox
        import os
        import sqlite3

        self.total = sum(float(item["price"]) * int(item["qty"]) for item in current_cart)
        self.paid_amount = self.total - debt_amount

        # Сканирование реальной базы данных
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        real_db_path = None
        target_table = None
        target_column = None
        ignored_dirs = {'.venv', 'venv', '.git', '__pycache__', 'build', 'dist'}

        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]
            if "store_database.db" in files:
                test_path = os.path.join(root, "store_database.db")
                try:
                    conn = sqlite3.connect(test_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = [t[0] for t in cursor.fetchall() if t[0] != 'sqlite_sequence']
                    conn.close()
                    if tables:
                        real_db_path = test_path
                        break
                except Exception:
                    continue

        if not real_db_path:
            QMessageBox.critical(self, "Baza tapylmady!", "⚠️ 'store_database.db' tapylmady.")
            return

        # Динамический поиск таблицы и колонки остатков
        try:
            conn = sqlite3.connect(real_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [t[0] for t in cursor.fetchall() if t[0] != 'sqlite_sequence']

            for table in tables:
                cursor.execute(f"PRAGMA table_info({table});")
                columns = [col[1].lower() for col in cursor.fetchall()]
                for col_name in ['galyndy', 'stock', 'sany', 'quantity']:
                    if col_name in columns:
                        target_table = table
                        target_column = col_name
                        break
                if target_table: break
            if not target_table and tables: target_table = tables[0]
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Ýalňyşlyk!", f"Baza okalmady: {e}")
            return

        # Проведение транзакции списания в БД
        try:
            conn = sqlite3.connect(real_db_path)
            cursor = conn.cursor()
            column_to_update = target_column if target_column else "galyndy"

            for item in current_cart:
                product_id = item["id"]
                sold_qty = int(item["qty"])
                cursor.execute(
                    f"UPDATE {target_table} SET {column_to_update} = {column_to_update} - ? WHERE id = ?",
                    (sold_qty, product_id)
                )
            conn.commit()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Katastrofa!", f"Baza ýazylmady: {e}")
            return

        # Вывод логов в терминал (сохранение структуры в памяти для будущей аналитики)
        print("\n=== 🧾 TRANSACTION LOG (MEMORY STASH) ===")
        print(f"Total Bill:     {self.total:.2f} TMT")
        print(f"Cash Received:  {self.paid_amount:.2f} TMT")
        print(f"Debt Stored:    {debt_amount:.2f} TMT")
        print("=========================================\n")

        QMessageBox.information(
            self,
            "Töleg Üstünlikli!",
            f"Söwda tamamlandy! 🧾\n\nJemi: {self.total:.2f} TMT\nNagt: {self.paid_amount:.2f} TMT\nNesiýe: {debt_amount:.2f}"
        )

        save_sold_items_history(
            cart_items=current_cart,
            client_name=client_name,
            payment_type='NAGYT',

            sale_total=self.total,
            debt_amount=debt_amount
        )
        self.load_product_tiles()
        self.refresh_cart_table()
        self.update()

        try:
            import json
            import os
            from datetime import datetime

            analytics_file = "analytics_data.json"
            today_str = datetime.now().strftime("%Y-%m-%d")

            # 1. READ EXISTING JSON FILE (So past sales are NEVER lost!)
            all_records = {}
            if os.path.exists(analytics_file):
                try:
                    with open(analytics_file, "r", encoding="utf-8") as f:
                        all_records = json.load(f)
                except Exception:
                    all_records = {}

            # Ensure today's record exists in dictionary
            if today_str not in all_records:
                all_records[today_str] = {
                    "total": 0.0,
                    "sold_items": 0,
                    "debt_amount": 0.0,
                    "sale_count": 0,
                    "client_debts": {}
                }

            # 2. CALCULATE CURRENT SALE VALUES
            sale_total = float(getattr(self, "total", 0.0))
            cash_paid = float(getattr(self, "paid_amount", sale_total))
            sale_debt = max(0.0, sale_total - cash_paid)



            # 6. TRIGGER ANALYTICS UI REFRESH
            main_window = self.window() if hasattr(self, 'window') else getattr(self, 'main_window', None)
            if main_window:
                from PyQt6.QtWidgets import QWidget
                for child in main_window.findChildren(QWidget):
                    if hasattr(child, "refresh_analytics"):
                        child.refresh_analytics()

        except Exception as e:
            print(f"❌ Checkout save error: {e}")

    def refresh_cart_table(self):
        current_tab_index = self.tabs.currentIndex()
        if current_tab_index == -1 or current_tab_index >= len(self.tables): return

        table = self.tables[current_tab_index]
        current_cart = self.carts[current_tab_index]

        table.setRowCount(0)
        for row_idx, item in enumerate(current_cart):
            table.insertRow(row_idx)
            total_item_price = item["price"] * item["qty"]

            table.setItem(row_idx, 0, QTableWidgetItem(str(item["name"])))
            table.setItem(row_idx, 1, QTableWidgetItem(f"{item['price']:.2f} TMT"))
            table.setItem(row_idx, 2, QTableWidgetItem(str(item["qty"])))
            table.setItem(row_idx, 3, QTableWidgetItem(f"{total_item_price}:.2f TMT"))

            # ➕ / ➖ СОЗДАНИЕ УПРАВЛЯЮЩИХ КНОПОК В СТРОКЕ ЧЕКА
            actions_container = QWidget()
            actions_layout = QHBoxLayout(actions_container)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            actions_layout.setSpacing(4)

            btn_minus = QPushButton("-")
            btn_minus.setStyleSheet(
                "background-color: #bf616a; color: white; border-radius: 4px; font-weight: bold; min-width: 25px;")
            btn_minus.clicked.connect(lambda checked, name=item["name"]: self.change_item_qty_by_name(name, -1))

            btn_plus = QPushButton("+")
            btn_plus.setStyleSheet(
                "background-color: #a3be8c; color: #2e3440; border-radius: 4px; font-weight: bold; min-width: 25px;")
            btn_plus.clicked.connect(lambda checked, name=item["name"]: self.change_item_qty_by_name(name, 1))

            actions_layout.addWidget(btn_minus)
            actions_layout.addWidget(btn_plus)

            table.setCellWidget(row_idx, 4, actions_container)

    # =================================================================
    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ И ИНИЦИАЛИЗАЦИЯ ТАБЛИЦЫ
    # =================================================================
    def create_tab_ui(self, tab_title):
        tab_widget = QWidget()
        tab_layout = QVBoxLayout(tab_widget)

        table = QTableWidget()
        table.setColumnCount(5)  # 5 колонок с учетом действий
        table.setHorizontalHeaderLabels(["Haryt", "Bahasy", "Sany", "Jemi", "Hereketler"])
        table.setStyleSheet("background-color: #1a1d24; color: white; border: none;")
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)

        tab_layout.addWidget(table)
        tab_widget.setLayout(tab_layout)

        self.tables.append(table)
        self.tabs.addTab(tab_widget, tab_title)

    def sync_cart_with_database(self):
        from core.database import get_all_products
        warehouse_products = get_all_products()
        existing_names = set()
        for p in warehouse_products:
            name = p.get("name") if isinstance(p, dict) else p[1]
            existing_names.add(name)
        cart_changed = False
        for cart in self.carts:
            original_len = len(cart)
            cart[:] = [item for item in cart if item["name"] in existing_names]
            if len(cart) != original_len: cart_changed = True
        if cart_changed:
            self.refresh_cart_table()
            db.update_total_price(self)

    def showEvent(self, event):
        super().showEvent(event)
        self.sync_cart_with_database()
        self.load_product_tiles()

    def go_back_to_menu(self):
        top_window = self.window()
        if top_window and hasattr(top_window, 'switch_page'):
            top_window.switch_page(0)
            return
        current_node = self.parent()
        while current_node:
            if hasattr(current_node, 'switch_page'):
                current_node.switch_page(0)
                return
            current_node = current_node.parent()

    def add_new_tab(self):
        self.carts.append([])
        next_index = self.tabs.count() + 1
        self.create_tab_ui(f"Sebet {next_index}")
        self.tabs.setCurrentIndex(next_index - 1)

    def on_tab_changed(self, index):
        if index == -1: return
        self.refresh_cart_table()
        db.update_total_price(self)

    def close_cart_tab(self, index):
        if self.tabs.count() <= 1: return
        self.tabs.blockSignals(True)
        self.tabs.removeTab(index)
        self.carts.pop(index)
        self.tables.pop(index)
        self.tabs.blockSignals(False)
        self.on_tab_changed(self.tabs.currentIndex())

    def process_full_cash_checkout(self):
        """Проводит продажу со 100% оплатой наличными (без долга)"""

        current_tab_index = self.tabs.currentIndex()
        current_cart = self.carts[current_tab_index]
        if not current_cart:
            from PyQt6.QtWidgets import QMessageBox
            title = "Внимание" if self.lang == "ru" else "Gözegçilik"
            text = "Корзина пуста! Добавьте товар." if self.lang == "ru" else "Sebet boş! Haryt goşuň."
            QMessageBox.warning(self, title, text)
            return

        self.execute_checkout_logic(0, 0)

    def process_debt_checkout(self):
            """Запрашивает сумму долга через всплывающее окно"""
            current_tab_index = self.tabs.currentIndex()
            if current_tab_index == -1: return
            current_cart = self.carts[current_tab_index]

            if not current_cart:
                from PyQt6.QtWidgets import QMessageBox
                title = "Внимание" if self.lang == "ru" else "Gözegçilik"
                text = "Корзина пуста! Добавьте товар." if self.lang == "ru" else "Sebet boş! Haryt goşuň."
                QMessageBox.warning(self, title, text)  # <-- Fixed position arguments
                return

            from PyQt6.QtWidgets import QInputDialog
            total = sum(float(item["price"]) * int(item["qty"]) for item in current_cart)

            # 1. Ask for Debt Amount
            title_debt = "Счет в долг" if self.lang == "ru" else "Nesiýe Hasaby"
            label_debt = (f"Итоговый счет: {total:.2f} TMT\nСумма долга:" if self.lang == "ru"
                          else f"Jemi Hasap: {total:.2f} TMT\nNesiýe ýazylmaly möçberi (Debt):")

            debt_amount, ok = QInputDialog.getDouble(
                self, title_debt, label_debt, 0.0, 0.0, total, 2
            )

            if ok:
                # 2. Ask for Client Name
                title_client = "Имя клиента" if self.lang == "ru" else "Müşderi Ady"
                label_client = "Введите имя клиента:" if self.lang == "ru" else "Müşderiniň adyny giriziň (Client Name):"

                client_name, name_ok = QInputDialog.getText(self, title_client, label_client)

                # 3. Handle default name
                default_name = "Неизвестный" if self.lang == "ru" else "Nätanyş"

                if name_ok and client_name.strip():
                    final_client_name = client_name.strip()
                else:
                    final_client_name = default_name

                # 4. Run your execution logic with the translated client name
                self.execute_checkout_logic(debt_amount=debt_amount, client_name=final_client_name)

                # 4. Reset the name back to default so the next customer doesn't accidentally get this name
                self.client_name = "Nätanyş"

    def send_sms_receipt(self, receipt_text):
        """Отправка чека по SMS через Twilio API"""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox

        # Запрашиваем номер телефона клиента
        phone_number, ok = QInputDialog.getText(
            self,
            "SMS Çek Ugratmak",
            "Müşderiniň telefon belgisi (+993...):",
            text="+993"
        )

        if not ok or not phone_number.strip():
            return

        # ⚠️ ВАЖНО: Вставь сюда свои реальные ключи от аккаунта Twilio
        account_sid = 'ТВОЙ_TWILIO_ACCOUNT_SID'
        auth_token = 'ТВОЙ_TWILIO_AUTH_TOKEN'
        twilio_number = 'ТВОЙ_TWILIO_НОМЕР'

        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=receipt_text,
                from_=twilio_number,
                to=phone_number.strip()
            )
            QMessageBox.information(
                self,
                "SMS Üstünlikli!",
                f"Çek müşderä ugradyldy!\nStatus: {message.status}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "SMS Ýalňyşlyk",
                f"Twilio API hatasy:\n{e}"
            )

    def update_texts(self, lang):
        print(f"lang: {lang}")
        self.lang = lang

        if self.lang == "ru":
            # Update placeholders and static buttons
            self.search_bar.setPlaceholderText("🔍 Поиск товаров... (Введите название для поиска)")
            self.btn_full_checkout.setText("💳 Наличные / Полная оплата")
            self.btn_debt_checkout.setText("📝 В долг")
            self.btn_back_to_menu.setText("⬅️ Главное меню")
            self.btn_add_tab.setText("+ Новая корзина")

            # Safely swap the word "Jemi" for "Итого" without losing the numbers!
            current_total = self.lbl_total.text().split(':')[-1].strip()
            self.lbl_total.setText(f"Итого: {current_total}")

            # Update all open tab titles (Sebet -> Корзина)
            for i in range(self.tabs.count()):
                self.tabs.setTabText(i, f"Корзина {i + 1}")

        else:  # Turkmen fallback
            self.search_bar.setPlaceholderText("🔍 Haryt gözle... (Введите название для поиска)")
            self.btn_full_checkout.setText("💳 Nagt / Doly Töleg")
            self.btn_debt_checkout.setText("📝 Karz Ýazmak")
            self.btn_back_to_menu.setText("⬅️ Esasy Menýu")
            self.btn_add_tab.setText("+ Täze sebet")

            current_total = self.lbl_total.text().split(':')[-1].strip()
            self.lbl_total.setText(f"Jemi: {current_total}")

            for i in range(self.tabs.count()):
                self.tabs.setTabText(i, f"Sebet {i + 1}")


    # =========================================================
# SYSTEM COMPONENT CLASSES
# =========================================================
class NavButton(QPushButton):
    """Zero-risk custom navigation button. Uses safe layouts instead of volatile HTML."""

    def __init__(self, icon_str, parent=None):
        super().__init__(parent)
        self.setFixedHeight(75)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        self.icon_lbl = QLabel(icon_str, self)
        self.icon_lbl.setStyleSheet("font-size: 24px; background: transparent; border: none;")

        text_container = QWidget(self)
        text_container.setStyleSheet("background: transparent; border: none;")
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        self.title_lbl = QLabel(self)
        self.title_lbl.setStyleSheet(
            "color: #FFFFFF; font-size: 13px; font-weight: bold; background: transparent; border: none;")

        self.sub_lbl = QLabel(self)
        self.sub_lbl.setStyleSheet("color: #6C707E; font-size: 10px; background: transparent; border: none;")

        text_layout.addWidget(self.title_lbl)
        text_layout.addWidget(self.sub_lbl)

        layout.addWidget(self.icon_lbl)
        layout.addWidget(text_container, 1)

    def set_content_safe(self, title, subtitle):
        try:
            _ = self.objectName()
            if hasattr(self, "title_lbl") and self.title_lbl is not None:
                self.title_lbl.setText(title)
            if hasattr(self, "sub_lbl") and self.sub_lbl is not None:
                self.sub_lbl.setText(subtitle)
        except RuntimeError:
            pass


class MetricCard(QFrame):
    def __init__(self, icon_str, title_str, value_str, color_hex, parent):
        super().__init__(parent)
        self.setFixedSize(220, 65)
        self.setObjectName("MetricCard")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        self.icon_lbl = QLabel(icon_str, self)
        self.icon_lbl.setStyleSheet(f"font-size: 22px; color: {color_hex}; background: transparent;")

        text_widget = QWidget(self)
        text_widget.setStyleSheet("background: transparent;")
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        self.title_label = QLabel(title_str, text_widget)
        self.title_label.setStyleSheet("color: #8E939E; font-size: 11px;")

        self.val_label = QLabel(value_str, text_widget)
        self.val_label.setStyleSheet(f"color: {color_hex}; font-size: 15px; font-weight: bold;")

        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.val_label)

        layout.addWidget(self.icon_lbl)
        layout.addWidget(text_widget, 1)


class DashboardCard(QPushButton):
    def __init__(self, icon_str, title, subtitle, parent):
        super().__init__(parent)
        self.setFixedSize(245, 185)
        self.setObjectName("DashboardCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.circle_frame = QFrame(self)
        self.circle_frame.setFixedSize(60, 60)
        self.circle_frame.setStyleSheet("""
            QFrame {
                border: 2px solid rgba(0, 204, 102, 0.4);
                border-radius: 30px;
                background-color: rgba(0, 204, 102, 0.05);
            }
        """)
        circle_layout = QVBoxLayout(self.circle_frame)
        circle_layout.setContentsMargins(0, 0, 0, 0)
        circle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.icon_lbl = QLabel(icon_str, self.circle_frame)
        self.icon_lbl.setStyleSheet("font-size: 24px; border: none; background: transparent;")
        circle_layout.addWidget(self.icon_lbl)

        self.title_lbl = QLabel(title, self)
        self.title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_lbl.setStyleSheet(
            "color: #FFFFFF; font-size: 14px; font-weight: bold; border: none; background: transparent;")

        self.sub_lbl = QLabel(subtitle, self)
        self.sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sub_lbl.setWordWrap(True)
        self.sub_lbl.setStyleSheet("color: #6C707E; font-size: 11px; border: none; background: transparent;")

        layout.addWidget(self.circle_frame, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_lbl)
        layout.addWidget(self.sub_lbl)


# =========================================================
# PRODUCT MODAL POPUP
# =========================================================
class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новый товар / Täze Haryt")
        self.setFixedSize(400, 580)
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title_lbl = QLabel("ДОБАВИТЬ ТОВАР", self)
        title_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #00CC66;")
        layout.addWidget(title_lbl)

        self.input_name = QLineEdit(self)
        self.input_name.setPlaceholderText("Наименование товара")
        layout.addWidget(self.input_name)

        self.input_category = QLineEdit(self)
        self.input_category.setPlaceholderText("Категория")
        layout.addWidget(self.input_category)

        self.input_p_price = QLineEdit(self)
        self.input_p_price.setPlaceholderText("Закупочная цена (TMT)")
        layout.addWidget(self.input_p_price)

        self.input_s_price = QLineEdit(self)
        self.input_s_price.setPlaceholderText("Цена продажи (TMT)")
        layout.addWidget(self.input_s_price)

        self.input_stock = QLineEdit(self)
        self.input_stock.setPlaceholderText("Количество (шт)")
        layout.addWidget(self.input_stock)

        self.input_min_stock = QLineEdit(self)
        self.input_min_stock.setPlaceholderText("Мин. остаток")
        layout.addWidget(self.input_min_stock)

        self.input_debt = QLineEdit(self)
        self.input_debt.setPlaceholderText("Karhana garzlary")
        layout.addWidget(self.input_debt)

        self.lbl_error = QLabel("", self)
        self.lbl_error.setStyleSheet("color: #FF453A;")
        layout.addWidget(self.lbl_error)

        btn_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Отмена", self)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_save = QPushButton("Сохранить", self)
        self.btn_save.setObjectName("SaveBtn")
        self.btn_save.clicked.connect(self.validate_and_save)
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog { background-color: #0F1013; }
            QLineEdit { 
                background-color: #15171E; 
                color: #FFFFFF; 
                padding: 12px; 
                border-radius: 6px; 
                border: 1px solid #22252D;
                font-size: 13px;
            }
            QLineEdit:focus { border: 1px solid #00CC66; }
            QPushButton { 
                background-color: #1E222B; 
                color: #FFFFFF; 
                padding: 12px; 
                border-radius: 6px; 
                font-weight: bold;
                border: none;
            }
            QPushButton#SaveBtn { background-color: #00CC66; color: #000000; }
            QPushButton#SaveBtn:hover { background-color: #00E676; }
        """)

    def validate_and_save(self):
        name = self.input_name.text().strip()
        category = self.input_category.text().strip()
        if not name or not category:
            self.lbl_error.setText("⚠️ Заполните обязательные поля!")
            return
        try:
            p_price = float(self.input_p_price.text() or 0.0)
            s_price = float(self.input_s_price.text() or 0.0)
            stock = int(self.input_stock.text() or 0)
            min_stock = int(self.input_min_stock.text() or 0)

            add_product(name, category, p_price, s_price, stock, min_stock)
            self.accept()
            if hasattr(self, 'analytics_widget'):
                self.analytics_widget.refresh_analytics()
            elif hasattr(self, 'refresh_analytics'):
                self.refresh_analytics()
        except ValueError:
            self.lbl_error.setText("⚠️ Цены и количество должны быть числами!")


def save_store_debt_to_json(debt_amount, product_name="Nätanyş Haryt"):
    if debt_amount <= 0:
        return

    # Use exact absolute path
    today_str = datetime.now().strftime("%Y-%m-%d")

    records = {}
    if os.path.exists(ANALYTICS_FILE):
        try:
            with open(ANALYTICS_FILE, "r", encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            records = {}

    if today_str not in records:
        records[today_str] = {
            "total": 0.0,
            "sold_items": 0,
            "debt_amount": 0.0,
            "store_debt": 0.0,
            "store_debt_history": [],  # 🆕 Our new list for the pie chart!
            "sale_count": 0
        }

    # 1. Update the total store_debt float (for the top cards)
    records[today_str]["store_debt"] = float(records[today_str].get("store_debt", 0.0)) + debt_amount

    # 2. Ensure the history list exists (in case it's an old day in the JSON)
    if "store_debt_history" not in records[today_str]:
        records[today_str]["store_debt_history"] = []

    # 3. Append the specific product and debt amount (Just like you designed!)
    records[today_str]["store_debt_history"].append({
        "prod_name": product_name,
        "debt_amount": debt_amount
    })

    with open(ANALYTICS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4)

    print(f"✅ Saved {debt_amount} TMT for {product_name} to: {ANALYTICS_FILE}")


# =========================================================
# MAIN APP WINDOW
# =========================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BUILD STORE PRO")
        self.resize(1380, 920)
        self.current_lang = "tm"

        self.init_ui()
        self.apply_styles()
        self.update_texts()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)
        self.update_datetime()

        self.load_products_from_db()
        self.stackedWidget = QStackedWidget()
        self.stackedWidget.setCurrentIndex(0)
        self.btn_sklad.clicked.connect(lambda: self.switch_page(1))
        self.btn_sales.clicked.connect(lambda: self.switch_page(2))

        self.sales_widget = SalesWidget(2)

        self.sales_page_index = self.page_stack.addWidget(self.sales_widget)

        self.sales_widget.btn_back_to_menu.clicked.connect(lambda: self.switch_page(0))

    def update_top_header_cards(self):
        from PyQt6.QtCore import QFileSystemWatcher
        if not hasattr(self, "watcher"):
            self.watcher = QFileSystemWatcher(self)
            self.watcher.addPath(ANALYTICS_FILE)
            self.watcher.fileChanged.connect(self.update_top_header_cards)
            print("Watcher started!")

        """Updates top header MetricCard values from JSON & DB"""
        import json
        import os

        from datetime import datetime

        today_sales = 0.0
        total_customer_debt = 0.0
        total_store_debt = 0.0

        # 1. READ VALUES FROM JSON
        if os.path.exists(ANALYTICS_FILE):
            try:
                with open(ANALYTICS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)

                today_str = datetime.now().strftime("%Y-%m-%d")

                if today_str in data and isinstance(data[today_str], dict):
                    today_sales = float(data[today_str].get("total", 0.0))

                for date_key, stats in data.items():
                    if isinstance(stats, dict):
                        total_store_debt += float(stats.get("store_debt", 0.0))
                        total_customer_debt += float(stats.get("debt_amount", 0.0))

            except Exception as e:
                print(f"❌ JSON Header read error: {e}")
        str_today_sales = f"{today_sales:,.0f} m".replace(",", " ")
        str_cust_debt = f"{total_customer_debt:,.0f} m".replace(",", " ")
        str_store_debt = f"{total_store_debt:,.0f} m".replace(",", " ")

        # 3. OVERWRITE THE MetricCard LABELS DIRECTLY
        if hasattr(self, "metric_sales") and hasattr(self.metric_sales, "val_label"):
            self.metric_sales.val_label.setText(str_today_sales)

        if hasattr(self, "metric_client") and hasattr(self.metric_client, "val_label"):
            self.metric_client.val_label.setText(str_cust_debt)

        if hasattr(self, "metric_supplier") and hasattr(self.metric_supplier, "val_label"):
            self.metric_supplier.val_label.setText(str_store_debt)

        print(
            f"✅ TOP CARDS UPDATED: Sales={str_today_sales} | Client Debt={str_cust_debt} | Supplier Debt={str_store_debt}")

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # =========================================================
        # 1. SIDEBAR (Premium Glow Left-Nav)
        # =========================================================
        sidebar = QFrame(central_widget)
        sidebar.setFixedWidth(280)
        sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 25, 20, 25)
        sidebar_layout.setSpacing(15)

        # Brand Header (Stacked Vertically to avoid truncation)
        brand_container = QWidget(sidebar)
        brand_container.setStyleSheet("background: transparent;")
        brand_layout = QVBoxLayout(brand_container)
        brand_layout.setContentsMargins(0, 0, 0, 0)
        brand_layout.setSpacing(6)

        self.lbl_logo = QLabel("BUILD STORE PRO", brand_container)
        self.lbl_logo.setMinimumWidth(240)
        self.lbl_logo.setStyleSheet(
            "color: #FFFFFF; font-weight: 900; font-size: 20px; letter-spacing: 0.5px; background: transparent;")

        self.lbl_version = QLabel("V15 PRO", brand_container)
        self.lbl_version.setFixedSize(65, 20)
        self.lbl_version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_version.setStyleSheet("""
            background-color: rgba(0, 204, 102, 0.15);
            color: #00CC66;
            border-radius: 4px;
            font-size: 10px;
            font-weight: bold;
        """)

        brand_layout.addWidget(self.lbl_logo)
        brand_layout.addWidget(self.lbl_version)
        sidebar_layout.addWidget(brand_container)

        spacer = QWidget(sidebar)
        spacer.setFixedHeight(15)
        sidebar_layout.addWidget(spacer)

        # Custom buttons (Exclusive toggle logic)
        self.btn_sklad = NavButton("📦", sidebar)
        self.btn_sklad.setChecked(True)
        self.btn_sklad.setAutoExclusive(True)
        self.btn_sklad.clicked.connect(lambda: self.switch_page(1))

        self.btn_sales = NavButton("🛒", sidebar)
        self.btn_sales.setAutoExclusive(True)
        self.btn_sales.clicked.connect(lambda: self.switch_page(2))

        self.btn_analytics = NavButton("📊", sidebar)
        self.btn_analytics.setAutoExclusive(True)

        sidebar_layout.addWidget(self.btn_sklad)
        sidebar_layout.addWidget(self.btn_sales)
        sidebar_layout.addWidget(self.btn_analytics)
        sidebar_layout.addStretch()

        # Sidebar footer controls
        self.btn_lang = QPushButton(sidebar)
        self.btn_lang.setObjectName("SidebarFooterBtn")
        self.btn_lang.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_lang.clicked.connect(self.toggle_language)

        self.btn_settings = QPushButton("⚙️ Настройки", sidebar)
        self.btn_settings.setObjectName("SidebarFooterBtn")
        self.btn_settings.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_settings.clicked.connect(lambda: self.switch_page(3))

        sidebar_layout.addWidget(self.btn_lang)
        sidebar_layout.addWidget(self.btn_settings)
        main_layout.addWidget(sidebar)

        # =========================================================
        # 2. MAIN HUB WORKSPACE
        # =========================================================
        right_container = QWidget(central_widget)
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(25, 25, 25, 25)
        right_layout.setSpacing(20)

        # TOP NAVIGATION BAR (Header Indicators)
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 10)

        self.metric_sales = MetricCard("📈", "", "15 450 ₼", "#00CC66", right_container)
        self.metric_stock = MetricCard("📦", "", "3 560", "#00CC66", right_container)
        self.metric_client = MetricCard("👤", "", "1 250 ₼", "#FF9F0A", right_container)
        self.metric_supplier = MetricCard("🚚", "", "840 ₼", "#FF3B30", right_container)

        top_bar.addWidget(self.metric_sales)
        top_bar.addWidget(self.metric_stock)
        top_bar.addWidget(self.metric_client)
        top_bar.addWidget(self.metric_supplier)
        top_bar.addStretch()

        self.user_panel = QFrame(right_container)
        self.user_panel.setObjectName("UserPanel")
        self.user_panel.setFixedSize(190, 65)
        user_layout = QHBoxLayout(self.user_panel)
        user_layout.setContentsMargins(10, 8, 10, 8)

        user_details = QVBoxLayout()
        user_details.setSpacing(1)
        self.lbl_user_title = QLabel("Пользователь:", self.user_panel)
        self.lbl_user_title.setStyleSheet("color: #8E939E; font-size: 11px;")
        self.lbl_username = QLabel("Администратор", self.user_panel)
        self.lbl_username.setStyleSheet("color: #00CC66; font-size: 13px; font-weight: bold;")
        user_details.addWidget(self.lbl_user_title)
        user_details.addWidget(self.lbl_username)

        self.lbl_user_time = QLabel(self.user_panel)
        self.lbl_user_time.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_user_time.setStyleSheet("color: #FFFFFF; font-size: 13px; font-weight: bold;")

        user_layout.addLayout(user_details)
        user_layout.addWidget(self.lbl_user_time)
        top_bar.addWidget(self.user_panel)

        right_layout.addLayout(top_bar)

        self.page_stack = QStackedWidget(right_container)

        # --- PAGE 0: MAIN DASHBOARD ---
        self.dash_page = QWidget(self.page_stack)
        dash_layout = QVBoxLayout(self.dash_page)
        dash_layout.setContentsMargins(0, 0, 0, 0)
        dash_layout.setSpacing(15)

        self.lbl_welcome = QLabel(self.dash_page)
        self.lbl_welcome.setStyleSheet("color: #FFFFFF; font-size: 26px; font-weight: bold; letter-spacing: 0.5px;")
        self.lbl_subtitle = QLabel(self.dash_page)
        self.lbl_subtitle.setStyleSheet("color: #8E939E; font-size: 13px;")

        dash_layout.addWidget(self.lbl_welcome)
        dash_layout.addWidget(self.lbl_subtitle)

        dash_spacer = QWidget(self.dash_page)
        dash_spacer.setFixedHeight(10)
        dash_layout.addWidget(dash_spacer)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        self.dash_cards_title = []
        self.dash_cards_sub = []

        icons = ["🛒", "🚚", "📋", "👥", "📊", "⚠️", "🖨️", "⚙️"]
        for i in range(8):
            card = DashboardCard(icons[i], "", "", self.dash_page)
            self.dash_cards_title.append(card.title_lbl)
            self.dash_cards_sub.append(card.sub_lbl)
            if i == 0:

                card.clicked.connect(lambda: self.switch_page(2))
            elif i == 1:
                card.clicked.connect(self.open_add_product_modal)
            elif i == 2:
                card.clicked.connect(lambda: self.switch_page(1))
            elif i == 3:
                card.clicked.connect(lambda: self.switch_page(3))
            row, col = divmod(i, 4)
            grid_layout.addWidget(card, row, col)

        dash_layout.addLayout(grid_layout)
        dash_layout.addStretch()

        self.backup_panel = QFrame(self.dash_page)
        self.backup_panel.setObjectName("BackupPanel")
        self.backup_panel.setFixedHeight(85)
        backup_layout = QHBoxLayout(self.backup_panel)
        backup_layout.setContentsMargins(20, 15, 20, 15)

        shield_icon = QLabel("🛡️", self.backup_panel)
        shield_icon.setStyleSheet("font-size: 26px; background: transparent;")

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        self.lbl_backup_title = QLabel(self.backup_panel)
        self.lbl_backup_title.setStyleSheet(
            "color: #FFFFFF; font-size: 14px; font-weight: bold; background: transparent;")
        self.lbl_backup_sub = QLabel(self.backup_panel)
        self.lbl_backup_sub.setStyleSheet("color: #8E939E; font-size: 12px; background: transparent;")
        text_col.addWidget(self.lbl_backup_title)
        text_col.addWidget(self.lbl_backup_sub)

        self.lbl_backup_last = QLabel(self.backup_panel)
        self.lbl_backup_last.setStyleSheet("color: #8E939E; font-size: 12px; background: transparent;")
        self.lbl_backup_date = QLabel("21.06.2025 20:15", self.backup_panel)
        self.lbl_backup_date.setStyleSheet(
            "color: #00CC66; font-size: 12px; font-weight: bold; background: transparent;")

        self.btn_backup_action = QPushButton(self.backup_panel)
        self.btn_backup_action.setObjectName("BackupBtn")
        self.btn_backup_action.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_backup_action.setFixedSize(140, 36)

        backup_layout.addWidget(shield_icon)
        backup_layout.addLayout(text_col, 1)
        backup_layout.addWidget(self.lbl_backup_last)
        backup_layout.addWidget(self.lbl_backup_date)
        backup_layout.addWidget(self.btn_backup_action)
        dash_layout.addWidget(self.backup_panel)

        # --- PAGE 1: DETAILED STORAGE OVERVIEW (Sklad) ---
        self.sklad_page = QWidget(self.page_stack)
        sklad_layout = QVBoxLayout(self.sklad_page)
        sklad_layout.setContentsMargins(0, 0, 0, 0)
        sklad_layout.setSpacing(15)

        self.lbl_sklad_title = QLabel(self.sklad_page)
        self.lbl_sklad_title.setStyleSheet("color: #FFFFFF; font-size: 26px; font-weight: bold;")
        self.lbl_sklad_subtitle = QLabel(self.sklad_page)
        self.lbl_sklad_subtitle.setStyleSheet("color: #8E939E; font-size: 13px;")

        sklad_layout.addWidget(self.lbl_sklad_title)
        sklad_layout.addWidget(self.lbl_sklad_subtitle)

        controls_layout = QHBoxLayout()
        self.sklad_search = QLineEdit(self.sklad_page)
        self.sklad_search.setFixedHeight(45)
        self.sklad_search.setMinimumWidth(380)
        self.sklad_search.setObjectName("SearchField")
        self.sklad_search.textChanged.connect(self.search_filter_table)

        self.btn_sklad_back = QPushButton(self.sklad_page)
        self.btn_sklad_back.setObjectName("SkladBackBtn")
        self.btn_sklad_back.setFixedHeight(45)
        self.btn_sklad_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_sklad_back.clicked.connect(lambda: self.switch_page(0))

        self.btn_add_product = QPushButton(self.sklad_page)
        self.btn_add_product.setObjectName("SkladAddBtn")
        self.btn_add_product.setFixedHeight(45)
        self.btn_add_product.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_product.clicked.connect(self.open_add_product_modal)

        controls_layout.addWidget(self.sklad_search)
        controls_layout.addStretch()
        controls_layout.addWidget(self.btn_sklad_back)
        controls_layout.addWidget(self.btn_add_product)
        sklad_layout.addLayout(controls_layout)

        # HIGH CONTRAST SKLAD GRID WITH ALL 7 REAL COLUMNS
        self.sklad_table = QTableWidget(self.sklad_page)
        self.sklad_table.setColumnCount(7)
        self.sklad_table.setShowGrid(False)
        self.sklad_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.sklad_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.sklad_table.verticalHeader().setVisible(False)

        header = self.sklad_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Sklad name column auto-stretches

        self.sklad_table.setColumnWidth(0, 50)  # ID
        self.sklad_table.setColumnWidth(2, 140)  # Category
        self.sklad_table.setColumnWidth(3, 110)  # Purchase Price
        self.sklad_table.setColumnWidth(4, 110)  # Selling Price
        self.sklad_table.setColumnWidth(5, 100)  # Current Stock
        self.sklad_table.setColumnWidth(6, 110)  # Minimum Stock

        sklad_layout.addWidget(self.sklad_table)

        self.page_stack.addWidget(self.dash_page)
        self.page_stack.addWidget(self.sklad_page)
        right_layout.addWidget(self.page_stack)
        main_layout.addWidget(right_container)

        # THIS IS THE PART YOU ARE ADDING
        self.settings_page = self.create_settings_page()

        # 2. Add them to the stack IN EXACT ORDER
        self.page_stack.addWidget(self.dash_page)  # Becomes Index 0
        self.page_stack.addWidget(self.sklad_page)  # Becomes Index 1
        self.sales_page = SalesWidget(self)
        self.page_stack.addWidget(self.sales_page)  # Becomes Index 2

        # ---> PUT YOUR SETTINGS WIDGET ADDITION HERE <---
        self.page_stack.addWidget(self.settings_page)  # Becomes Index 3
        # In MainWindow settings setup:
        self.toggle_print = AnimatedToggle()
        self.toggle_sms_imo = AnimatedToggle()
        self.toggle_qr = AnimatedToggle()

        # Store state flags on MainWindow
        self.config_auto_print = True  # Default ON
        self.config_sms_imo = False
        self.config_qr_code = False

        # Connect toggle state changes
        self.toggle_print.stateChanged.connect(
            lambda state: setattr(self, 'config_auto_print', bool(state))
        )
        self.toggle_sms_imo.stateChanged.connect(
            lambda state: setattr(self, 'config_sms_imo', bool(state))
        )
        self.toggle_qr.stateChanged.connect(
            lambda state: setattr(self, 'config_qr_code', bool(state))
        )
        # 1. Instantiate the Analytics widget
        self.analytics_page = AnalyticsWidget(
            main_window=self
        )

        # 2. Add it to the stack (This becomes Index 4)
        self.analytics_page_index = self.page_stack.addWidget(self.analytics_page)

        # 3. Connect your sidebar Analytics button to switch to index 4
        self.btn_analytics.clicked.connect(lambda: self.switch_page(4))

    def showEvent(self, event):
        super().showEvent(event)
        # update data when window becomes visible
        self.load_products_from_db()

        if hasattr(self, "analytics_widget"):
            self.analytics_widget.refresh_analytics()

        # 🚀 ADD THIS LINE TO UPDATE TOP METRIC CARDS ON LOAD!
        self.update_top_header_cards()

    # =========================================================
    # LOGICAL ACTIONS
    # =========================================================
    def update_datetime(self):
        current_time = QDateTime.currentDateTime().toString("HH:mm")
        current_date = QDateTime.currentDateTime().toString("dd.MM.yyyy")
        safe_set_text(self.lbl_user_time, f"{current_time}\n{current_date}")

    def open_add_product_modal(self):
        dialog = AddProductDialog(self)

        # When user clicks save/accepted
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 1. 💳 READ & SAVE MAGAZINE DEBT (Kärhana bergisi)
            if hasattr(dialog, "input_debt"):
                try:
                    debt_val = float(dialog.input_debt.text().strip() or 0.0)
                    if debt_val > 0:
                        # 1. Grab the product name from the dialog!
                        p_name = dialog.input_name.text().strip() or "Nätanyş Haryt"

                        # 2. Send both the debt AND the name to the save function
                        save_store_debt_to_json(debt_val, p_name)
                except ValueError:
                    pass

            # 2. 📦 RELOAD PRODUCTS TABLE (Your existing code)
            self.load_products_from_db()

            # 3. 📊 REFRESH ANALYTICS CARDS AUTOMATICALLY
            if hasattr(self, "analytics_widget"):
                self.analytics_widget.refresh_analytics()

            elif hasattr(self, "analytics_tab"):
                self.analytics_tab.refresh_analytics()
            self.update_top_header_cards()

    def search_filter_table(self, query):
        query = query.strip().lower()
        for row in range(self.sklad_table.rowCount()):
            name_item = self.sklad_table.item(row, 1)
            id_item = self.sklad_table.item(row, 0)

            name_match = query in name_item.text().lower() if name_item else False
            id_match = query in id_item.text().lower() if id_item else False

            self.sklad_table.setRowHidden(row, not (name_match or id_match))

    def handle_delete_product(self, prod_id):
        from core.database import delete_product

        # 1. Удаляем из базы данных
        delete_product(prod_id)

        # 2. Перезапускаем функцию загрузки таблицы, чтобы старая строка исчезла!
        self.load_products_from_db()

    def load_products_from_db(self, rows=None):
        try:

            total_stock = 0
            if rows is None:
                rows = get_all_products() or []
                self.sklad_table.setRowCount(len(rows))
                self.sklad_table.setColumnCount(8)
            for row_idx, row_data in enumerate(rows):
                total_stock += int(row_data[5]) if str(row_data[5]).isdigit() else 0

                # Col 0: ID
                item_id = QTableWidgetItem(f" {row_data[0]}")
                item_id.setForeground(QColor("#8E939E"))
                item_id.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))

                # Col 1: Name
                item_name = QTableWidgetItem(str(row_data[1]))
                item_name.setForeground(QColor("#FFFFFF"))
                item_name.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))

                # Col 2: Category
                item_cat = QTableWidgetItem(str(row_data[2]))
                item_cat.setForeground(QColor("#8E939E"))
                item_cat.setFont(QFont("Segoe UI", 10, QFont.Weight.Normal))

                # Col 3: Purchase Price
                item_p_price = QTableWidgetItem(f"{float(row_data[3]):.2f} TMT")
                item_p_price.setForeground(QColor("#FF9F0A"))  # Orange tint
                item_p_price.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))

                # Col 4: Selling Price
                item_s_price = QTableWidgetItem(f"{float(row_data[4]):.2f} TMT")
                item_s_price.setForeground(QColor("#00CC66"))  # Emerald tint
                item_s_price.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))

                # Col 5: Current Stock
                item_qty = QTableWidgetItem(f"   {row_data[5]}")
                item_qty.setForeground(QColor("#FFFFFF"))
                item_qty.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))

                # Col 6: Minimum Stock Alert
                item_min = QTableWidgetItem(f"   {row_data[6]}")
                item_min.setForeground(QColor("#FF3B30"))  # Soft red warning
                item_min.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))

                # Col 7: Button delete ␥
                btn_delete = QPushButton("❌")
                btn_delete.setStyleSheet(
                    """
                    QPushButton{
                        background-color: transparent;
                        color: #F38BA8
                        font-size: 14px;
                        border: none ;
                        
                    }
                    
                    QPushButton:hover {
                        background-color: #313244;
                        border-radius: 4px;
                    }
                    """
                )
                prod_id = row_data[0]

                btn_delete.clicked.connect(lambda checked, p_id=prod_id: self.handle_delete_product(p_id))
                self.sklad_table.setItem(row_idx, 0, item_id)
                self.sklad_table.setItem(row_idx, 1, item_name)
                self.sklad_table.setItem(row_idx, 2, item_cat)
                self.sklad_table.setItem(row_idx, 3, item_p_price)
                self.sklad_table.setItem(row_idx, 4, item_s_price)
                self.sklad_table.setItem(row_idx, 5, item_qty)
                self.sklad_table.setItem(row_idx, 6, item_min)
                self.sklad_table.setCellWidget(row_idx, 7, btn_delete)

                self.sklad_table.setRowHeight(row_idx, 50)

            if hasattr(self, "metric_stock") and hasattr(self.metric_stock, "val_label"):
                safe_set_text(self.metric_stock.val_label, f"{total_stock}")

        except Exception as e:
            print(f"Db Error: {e}")

    def go_back_to_main_menu(self):
        self.switch_page(0)

        self.load_products_from_db()

    def switch_page(self, index):
        print(f"ПРОГРАММА ПЫТАЕТСЯ ПЕРЕКЛЮЧИТЬ НА ИНДЕКС: {index}")  # 👈 Для проверки

        # Сбрасываем визуальное нажатие со всех кнопок
        self.btn_sklad.setChecked(False)
        self.btn_sales.setChecked(False)
        self.btn_settings.setChecked(False)
        # Логика переключения
        if index == 1:
            self.page_stack.setCurrentIndex(1)  # Индекс склада из Qt Designer
            self.btn_sklad.setChecked(True)
            self.load_products_from_db()
            print("Переключено на СКЛАД")

        elif index == 2:
            # 🔴 ВАЖНО: Переключаем не на цифру 2, а на реальный индекс нашего виджета!
            self.page_stack.setCurrentIndex(self.sales_page_index)
            self.btn_sales.setChecked(True)
            print("Переключено на ПРОДАЖИ (Кастомный виджет)")

        elif index == 0:
            self.page_stack.setCurrentIndex(0)  # Главное меню
            print("Переключено на ГЛАВНОЕ МЕНЮ")
        elif index == 3:
            self.page_stack.setCurrentIndex(3)

            self.btn_settings.setChecked(True)
            print("program is tryin to switch on page SETTINGS")
        elif index == 4:
            self.page_stack.setCurrentIndex(4)
            self.btn_analytics.setChecked(True)
            print("program is tryin to switch on page ANALYSIS")

    def toggle_language(self):
        self.current_lang = "tm" if self.current_lang == "ru" else "ru"
        self.update_texts()

    def update_texts(self):
        t = LANGUAGES[self.current_lang]

        # Uniquely update custom button text labels to prevent wrapper crashes
        self.btn_sklad.set_content_safe(t["sidebar_sklad_title"], t["sidebar_sklad_sub"])
        self.btn_sales.set_content_safe(t["sidebar_sales_title"], t["sidebar_sales_sub"])
        self.btn_analytics.set_content_safe(t["sidebar_analytics_title"], t["sidebar_analytics_sub"])

        safe_set_text(self.btn_settings, t["sidebar_settings"])
        safe_set_text(self.btn_lang, t["sidebar_lang"])

        safe_set_text(self.metric_sales.title_label, t["top_sales"])
        safe_set_text(self.metric_stock.title_label, t["top_stock"])
        safe_set_text(self.metric_client.title_label, t["top_debt_client"])
        safe_set_text(self.metric_supplier.title_label, t["top_debt_supplier"])

        safe_set_text(self.lbl_user_title, t["top_user"])
        safe_set_text(self.lbl_username, t["top_role"])

        safe_set_text(self.lbl_welcome, t["dash_title"])
        safe_set_text(self.lbl_subtitle, t["dash_subtitle"])

        if hasattr(self, 'analytics_page'):
            self.analytics_page.update_texts(self.current_lang)
        if hasattr(self, 'sales_page'):
            self.sales_page.update_texts(self.current_lang)

        try:
            visible_widget = self.page_stack.currentWidget()
            if hasattr(visible_widget, 'update_texts'):
                visible_widget.update_texts(self.current_lang)
        except Exception:
            pass

        for i in range(8):
            if i < len(self.dash_cards_title):
                safe_set_text(self.dash_cards_title[i], t[f"card_{i + 1}"])
            if i < len(self.dash_cards_sub):
                safe_set_text(self.dash_cards_sub[i], t[f"card_{i + 1}_sub"])

        safe_set_text(self.lbl_sklad_title, t["sklad_title"])
        safe_set_text(self.lbl_sklad_subtitle, t["sklad_subtitle"])
        safe_set_text(self.btn_add_product, t["sklad_add_btn"])
        safe_set_text(self.btn_sklad_back, t["sklad_back_btn"])

        safe_set_text(self.lbl_backup_title, t["backup_title"])
        safe_set_text(self.lbl_backup_sub, t["backup_sub"])
        safe_set_text(self.lbl_backup_last, t["backup_last"])
        safe_set_text(self.btn_backup_action, t["backup_btn"])

        try:
            if hasattr(self, "sklad_search") and self.sklad_search is not None:
                self.sklad_search.setPlaceholderText(t["sklad_search"])
            if hasattr(self, "sklad_table") and self.sklad_table is not None:
                self.sklad_table.setHorizontalHeaderLabels([
                    t["sklad_th_id"], t["sklad_th_name"], t["sklad_th_category"],
                    t["sklad_th_p_price"], t["sklad_th_s_price"], t["sklad_th_qty"], t["sklad_th_min_qty"]
                ])
                self.sklad_table.horizontalHeader().setStyleSheet("""
                    QHeaderView::section {
                        background-color: #15171E;
                        color: #8E939E;
                        font-weight: bold;
                        font-size: 11px;
                        border: none;
                        padding-left: 15px;
                        height: 45px;
                    }
                """)
        except RuntimeError:
            pass

    def create_settings_page(self):
        settings_widget = QWidget()
        layout = QVBoxLayout(settings_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        btn_erase = QPushButton("🚨 EXTREME ERASE (Clear All Data)")
        btn_erase.setStyleSheet("""
            QPushButton {
                background-color: #FF3B30; /* Emergency Red */
                color: white; 
                font-weight: bold; 
                font-size: 15px; 
                padding: 15px; 
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        # Connect it to our new function
        btn_erase.clicked.connect(self.extreme_erase_data)

        layout.addWidget(btn_erase)


        # Заголовок
        lbl_title = QLabel("⚙ Настройки выдачи чеков")
        lbl_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #eceff4;")
        layout.addWidget(lbl_title)

        # Список настроек с тумблерами
        options = [
            ("🖨️ Автоматическая печать чека на принтере", "print_enabled"),
            ("📱 Отправка чека по SMS / WhatsApp", "sms_enabled"),
            ("📲 Генерация QR-кода на экране для сканирования", "qr_enabled")
        ]

        for title, key in options:
            row = QFrame()
            row.setStyleSheet("""
                QFrame {
                    background-color: #12161f;
                    border-radius: 12px;
                    padding: 12px 18px;
                }
            """)
            row_layout = QHBoxLayout(row)

            lbl = QLabel(title)
            lbl.setStyleSheet("font-size: 15px; color: #eceff4; font-weight: 500;")

            toggle = AnimatedToggle()
            toggle.setChecked(True if key == "print_enabled" else False)

            row_layout.addWidget(lbl)
            row_layout.addStretch()
            row_layout.addWidget(toggle)

            layout.addWidget(row)

        layout.addStretch()
        return settings_widget

    def extreme_erase_data(self):
        from PyQt6.QtWidgets import QMessageBox
        import os
        import json

        # 1. Double-check with the user so they don't click it by mistake!
        reply = QMessageBox.warning(
            self,
            'Diňläň! (Warning)',
            'Are you 100% sure you want to erase ALL data in the app?\n\nThis will wipe the database and analytics. This CANNOT be undone!',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Set up the paths based on your project structure
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

                # Database is inside the 'data' folder
                db_path = os.path.join(BASE_DIR, "data", "store_database.db")

                # FIX: JSON is in the root BASE_DIR directory, NOT inside 'ui'
                json_path = os.path.join(BASE_DIR, "analytics_data.json")

                # 2. Wipe the Analytics JSON
                if os.path.exists(json_path):
                    with open(json_path, "w", encoding="utf-8") as f:
                        json.dump({}, f)  # Overwrite with empty data
                else:
                    print(f"Could not find JSON at: {json_path}")  # Helpful debug print

                # 3. Wipe the Database
                if os.path.exists(db_path):
                    os.remove(db_path)  # Deletes the file entirely

                # 4. Success Message
                QMessageBox.information(
                    self,
                    "Üstünlikli (Success)",
                    "The mind of the app has been completely wiped clean! 🫧✨\n\nPlease restart the application for changes to take effect."
                )

            except Exception as e:
                QMessageBox.critical(self, "Ýalňyşlyk (Error)", f"Could not erase data:\n{str(e)}")

    # =========================================================
    # PREMIUM NEO-GLOW STYLES
    # =========================================================
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow, QWidget { 
                background-color: #0D0E12; 
                color: #FFFFFF; 
                font-family: 'Segoe UI', Arial, sans-serif;
            }

            /* Sidebar Base Frame */
            QFrame#Sidebar { 
                background-color: #121419; 
                border-right: 1px solid #1C1E26;
            }
            QPushButton#SidebarFooterBtn {
                background: transparent;
                border: 1px solid #22252D;
                border-radius: 6px;
                color: #8E939E;
                padding: 10px;
                font-size: 11px;
                text-align: left;
            }
            QPushButton#SidebarFooterBtn:hover {
                color: #FFFFFF;
                border: 1px solid #00CC66;
            }

            /* Neo-Glow Hover and Selection Border Radius on Sidebar Navigation */
            NavButton {
                background-color: transparent;
                border: 1.5px solid transparent;
                border-radius: 12px;
            }
            NavButton:hover {
                background-color: rgba(0, 204, 102, 0.05);
                border: 1.5px solid rgba(0, 204, 102, 0.25);  /* Barely visible glowing transparent green line */
            }
            NavButton:checked {
                background-color: rgba(0, 204, 102, 0.12);
                border: 1.5px solid rgba(0, 204, 102, 0.85);  /* Full active glow */
            }

            /* Metrics Bar */
            QFrame#MetricCard {
                background-color: #121419;
                border-radius: 8px;
                border: 1px solid #1C1E26;
            }
QFrame#UserPanel {
    background-color: #121419;
    border-radius: 8px;
    border: 1px solid #1C1E26;
}

/* Grid Dashboard Cards */
QPushButton#DashboardCard {
    background-color: #121419;
    border-radius: 12px;
    border: 1px solid #1C1E26;
}
QPushButton#DashboardCard:hover {
    border: 1px solid #00CC66;
    background-color: #171A21;
}

/* Backup Bar Panel */
QFrame#BackupPanel {
    background-color: #121419;
    border-radius: 10px;
    border: 1px solid #1C1E26;
}
QPushButton#BackupBtn {
    background-color: transparent;
    color: #00CC66;
    border: 1px solid #00CC66;
    border-radius: 6px;
    font-weight: bold;
    font-size: 11px;
}
QPushButton#BackupBtn:hover {
    background-color: rgba(0, 204, 102, 0.1);
}

/* Search Filters & Layout Buttons */
QLineEdit#SearchField {
    background-color: #121419;
    border: 1px solid #1C1E26;
    border-radius: 6px;
    padding-left: 15px;
    color: #FFFFFF;
    font-size: 12px;
}
    QLineEdit#SearchField:focus {
        border: 1px solid #00CC66;
    }
    QPushButton#SkladBackBtn {
        background-color: transparent;
        border: 1px solid #00CC66;
        border-radius: 6px;
        color: #00CC66;
        padding: 10px 20px;
        font-weight: bold;
    }
    QPushButton#SkladBackBtn:hover {
        background-color: rgba(0, 204, 102, 0.1);
    }
    QPushButton#SkladAddBtn {
        background-color: #00CC66;
        border-radius: 6px;
        color: #000000;
        padding: 10px 20px;
        font-weight: bold;
    }
    QPushButton#SkladAddBtn:hover {
        background-color: #00E676;
    }

    /* Premium Inventory Table Styling */
    QTableWidget {
        background-color: #121419;
        border: 1px solid #1C1E26;
        border-radius: 8px;
        outline: 0;
    }
    QTableWidget::item {
        border-bottom: 1px solid #1C1E26;
        padding-left: 15px;
    }
    QTableWidget::item:selected {
        background-color: #0076FF;  /* Radiant row highlight from your screenshots */
        color: #FFFFFF;
    }
""")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
