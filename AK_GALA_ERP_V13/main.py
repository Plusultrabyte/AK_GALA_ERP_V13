import tkinter as tk
from tkinter import messagebox
from core.database import init_db
from core.auth import login
from ui.main_window import MainWindow
import sys
from PyQt6.QtWidgets import QApplication
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(os.path.dirname(os.executable), relative_path)

def bootstrap():
    init_db()


class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ERP Login")
        self.root.geometry("350x400")
        self.root.configure(bg="#121212")
        self.root.eval('tk::PlaceWindow . center')  # Center on screen

        # Dark theme login
        frame = tk.Frame(self.root, bg="#121212")
        frame.pack(expand=True)

        tk.Label(frame, text="BUILD STORE PRO", font=("Segoe UI", 18, "bold"), bg="#121212", fg="#2ECC71").pack(pady=20)

        tk.Label(frame, text="Username:", bg="#121212", fg="white", font=("Segoe UI", 10)).pack(anchor="w")
        self.u = tk.Entry(frame, font=("Segoe UI", 12), bg="#1A1A1A", fg="white", insertbackground="white",
                          relief="flat")
        self.u.pack(pady=(0, 15), ipady=5, fill="x")

        tk.Label(frame, text="Password:", bg="#121212", fg="white", font=("Segoe UI", 10)).pack(anchor="w")
        self.p = tk.Entry(frame, show="*", font=("Segoe UI", 12), bg="#1A1A1A", fg="white", insertbackground="white",
                          relief="flat")
        self.p.pack(pady=(0, 25), ipady=5, fill="x")

        tk.Button(frame, text="ENTER", font=("Segoe UI", 12, "bold"), bg="#2ECC71", fg="#121212",
                  activebackground="#27AE60", relief="flat", command=self.check).pack(fill="x", ipady=5)

        self.root.mainloop()

    def check(self):
        user = login(self.u.get(), self.p.get())
        if user:
            username = user[1]
            self.root.destroy()
            self.open_app(username)
        else:
            messagebox.showerror("Error", "Wrong credentials! Try admin / admin")

    def open_app(self, username):

        app = QApplication(sys.argv)
        window=MainWindow()
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    bootstrap()
    LoginWindow()