import tkinter as tk
from tkinter import ttk
from core.database import get_connection


class ReportsWindow:
    def __init__(self, parent):
        # ИСПОЛЬЗУЕМ Toplevel вместо Tk() для дочерних окон!
        self.win = tk.Toplevel(parent)
        self.win.title("Sales Reports")
        self.win.geometry("600x400")
        self.win.configure(bg="#ECF0F1")

        ttk.Label(self.win, text="📈 Sales History", font=("Segoe UI", 16, "bold"), background="#ECF0F1").pack(pady=10)

        # Создаём красивую таблицу (Treeview)
        cols = ("ID", "Customer ID", "Total", "Date")
        self.tree = ttk.Treeview(self.win, columns=cols, show="headings")

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.show_sales()

    def show_sales(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales ORDER BY id DESC")

        for row in cur.fetchall():
            # Форматируем деньги красиво
            formatted_row = (row[0], row[1], f"${row[2]:.2f}", row[3])
            self.tree.insert("", tk.END, values=formatted_row)

        conn.close()