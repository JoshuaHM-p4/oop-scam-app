from tkinter import messagebox # remove this once complete front-end is implemented
import customtkinter as ctk
from PIL import Image
import tkinter as tk
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from signup import SignupFrame

from typing import Tuple
import requests

LOGIN_ENDPOINT = "http://localhost:5000/auth/login"

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.configure(fg_color='#222B36', bg_color='#222B36')
        self.callback = callback

        # Container
        self.container_frame = ctk.CTkFrame(self, fg_color='#141A1F', corner_radius=22)
        self.container_frame.pack(fill='both', side='left', expand=True, padx=20, pady=20)

        # Login Frame
        self.login_frame = ctk.CTkFrame(self.container_frame, fg_color='#222B36', corner_radius=22)
        self.login_frame.pack(side='left', fill='both', padx=40, pady=20)

        # Google signup frame
        self.google_signup_frame = ctk.CTkFrame(self.container_frame, fg_color='#222B36', corner_radius=22)
        self.google_signup_frame.pack(side='right', fill='both', padx=(0,40), pady=20, expand=True)

        # Signup frame
        self.signup_frame = SignupFrame(self.container_frame, controller=self)
        self.signup_frame.pack_forget()

        self.setup_ui()

    def setup_ui(self):
        self.pack(fill='both')

        # Set Profile Button
        self.default_profile = ctk.CTkImage(Image.open("assets/images/default_profile_picture.png"), size=(80, 80))

        self.profile_button = ctk.CTkButton(self.login_frame, width=80, height=80, image=self.default_profile, text='',
                                            fg_color='#222B36', hover_color='#D9D9D9', command=self.change_profile)
        self.profile_button.pack(padx=10, pady=20)

        self.welcome_label = ctk.CTkLabel(self.login_frame, text='Welcome Back!', font=("Arial", 25))
        self.welcome_label.pack(padx=10, pady=5)

        # Entries
        self.email_entry = ctk.CTkEntry(self.login_frame, placeholder_text='E-mail',
                                             placeholder_text_color='#141A1F', corner_radius=22, border_color='white',
                                           fg_color='white', width=300, height=35, text_color='#141A1F')
        self.email_entry.pack(padx=20, pady=10)

        self.password_entry = ctk.CTkEntry(self.login_frame, show="*", placeholder_text='Password',
                                           placeholder_text_color='#141A1F', corner_radius=22, border_color='white',
                                           fg_color='white', width=300, height=35, text_color='#141A1F')
        self.password_entry.pack(padx=20, pady=10)

        # Forgot password and sign up container
        self.button_container_frame = ctk.CTkFrame(self.login_frame, fg_color='#222B36')
        self.button_container_frame.pack(pady=5)

        # Forgot Password
        self.forgot_password_button = ctk.CTkButton(self.button_container_frame, text='Forgot Password?',
                                                    fg_color='#222B36', command=self.forgot_password)
        self.forgot_password_button.pack(side='left', padx=5)

        # Signup button
        self.signup_button = ctk.CTkButton(self.button_container_frame, text='Sign-Up', fg_color='#222B36',
                                           command=self.signup)
        self.signup_button.pack(side='right', padx=5)

        # Login Button
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login, corner_radius=24,
                                          width=120, height=45, fg_color='white', text_color='#141A1F')
        self.login_button.pack(padx=10, pady=20)

        self.login_button.bind("<Return>", self.login)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create a canvas to draw the lines and "or" text
        self.upper_line_canvas = tk.Canvas(self.google_signup_frame, width=400, height=40, bg='#222B36', highlightthickness=0)
        self.upper_line_canvas.pack(pady=70)

        # Draw the left line
        self.upper_line_canvas.create_line(0, 20, 170, 20, fill='white', width=2)

        # Draw the right line
        self.upper_line_canvas.create_line(220, 20, 400, 20, fill='white', width=2)

        # Add "or" text
        self.upper_line_canvas.create_text(195, 20, text="or", fill='white', font=("Arial", 22))

        # Signup Widgets
        self.google_logo = ctk.CTkImage(Image.open("assets/images/google_logo.png"), size=(130, 130))

        self.google_signup_button = ctk.CTkButton(self.google_signup_frame, image=self.google_logo, text='', corner_radius=100,
                                           fg_color='#222B36', command=self.google_signup)
        self.google_signup_button.pack(anchor='center')

        self.signup_label = ctk.CTkLabel(self.google_signup_frame, text='No account? Sign-Up', text_color='white')
        self.signup_label.pack()

        # Create a canvas to draw the lower line
        self.lower_line_canvas = tk.Canvas(self.google_signup_frame, width=400, height=40, bg='#222B36', highlightthickness=0)
        self.lower_line_canvas.pack(pady=70)

        self.lower_line_canvas.create_line(0, 20, 400, 20, fill='white', width=2)


    def change_profile(self):
        print('change profile clicked!')


    def forgot_password(self):
        print('Forgot password clicked!')


    def signup(self):
        print('Sign up button clicked')

        self.login_frame.pack_forget()
        self.google_signup_frame.pack_forget()

        self.signup_frame.configure(corner_radius=22)
        self.signup_frame.pack(fill='both', expand=True, padx=20, pady=20)

        self.signup_frame.back_button.configure(command=self.return_to_login)


    def return_to_login(self):
        self.signup_frame.pack_forget()
        self.login_frame.pack(side='left', fill='both', padx=40, pady=20)
        self.google_signup_frame.pack(side='right', fill='both', padx=(0, 40), pady=20, expand=True)


    def google_signup(self):
        print('Google sign up button clicked!')


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
