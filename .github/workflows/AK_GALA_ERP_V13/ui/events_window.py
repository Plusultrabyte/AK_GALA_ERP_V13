import tkinter as tk
from tkinter import ttk
from core.database import get_connection


class EventsWindow:
    def __init__(self, parent):
        # Toplevel для безопасности
        self.win = tk.Toplevel(parent)
        self.win.title("System Events Log")
        self.win.geometry("700x400")
        self.win.configure(bg="#ECF0F1")

        ttk.Label(self.win, text="📜 System Logs", font=("Segoe UI", 16, "bold"), background="#ECF0F1").pack(pady=10)

        cols = ("ID", "Type", "Message", "Timestamp")
        self.tree = ttk.Treeview(self.win, columns=cols, show="headings")

        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=50, anchor="center")

        self.tree.heading("Type", text="Event Type")
        self.tree.column("Type", width=150, anchor="w")

        self.tree.heading("Message", text="Message")
        self.tree.column("Message", width=300, anchor="w")

        self.tree.heading("Timestamp", text="Timestamp")
        self.tree.column("Timestamp", width=150, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.show_events()

    def show_events(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM events ORDER BY id DESC")

        for row in cur.fetchall():
            self.tree.insert("", tk.END, values=row)

        conn.close()