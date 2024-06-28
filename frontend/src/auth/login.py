from tkinter import messagebox # remove this once complete front-end is implemented
import customtkinter as ctk
from typing import Tuple
import requests

LOGIN_ENDPOINT = "http://localhost:5000/auth/login"

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback

        label = ctk.CTkLabel(self, text="Login Page")
        label.pack(pady=10, padx=10)

        # Example widgets (entry, button) for login
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.pack()

        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack()

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack()
        self.login_button.bind("<Return>", self.login)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def login(self, event=None): # response.json, response.status_code
        email = self.email_entry.get()
        password = self.password_entry.get()

        print(f"Logging in {email}...")

        login_data = {
            'email': email,
            'password': password,
        }

        try:
            response = requests.post(LOGIN_ENDPOINT, json=login_data, timeout=10)

            if response.status_code == 200:
                self.callback(response.json())
            else:
                messagebox.showerror("Login Error", response.json()['message'])
        except ConnectionError:
            messagebox.showerror("Connection Error", "Could not connect to server")

