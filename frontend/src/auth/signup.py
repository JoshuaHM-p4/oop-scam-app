import customtkinter as ctk
import requests
from tkinter import messagebox # remove this once complete front-end is implemented

SIGNUP_ENDPOINT = "http://localhost:5000/auth/login"
class SignupFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        label = ctk.CTkLabel(self, text="Signup Page")
        label.pack(pady=10, padx=10)

        # Example widgets (entry, button) for signup
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack()

        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.pack()

        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack()

        self.signup_button = ctk.CTkButton(self, text="Signup", command=self.signup)
        self.signup_button.pack()

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()

        signup_data = {
            'username': username,
            'password': password,
            'email': email
        }

        response = requests.post(SIGNUP_ENDPOINT, json=signup_data, timeout=10)

        if response.status_code == 200:
            messagebox.showinfo("Signup Successful", response.json()['message'])
        else:
            print("Signup Error:", response.json()['message'])


