import customtkinter as ctk
from PIL import Image
import tkinter as tk
import os
import sys
import threading

loading_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common', 'loading'))
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(loading_dir)
sys.path.append(script_dir)

from loading import LoadingFrame
from signup import SignupFrame

from typing import Tuple
import requests

LOGIN_ENDPOINT = "http://localhost:5000/auth/login"

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.master = master
        self.configure(fg_color='#222B36', bg_color='#222B36')

        self.callback = callback
        self.request_lock = threading.Lock()  # Initialize the lock
        self.loading = None

        # Container
        self.container_frame = ctk.CTkFrame(self, fg_color='#141A1F', corner_radius=10)
        self.container_frame.pack(fill='both', side='left', expand=True, padx=20, pady=20)

        # Login Frame

        self.login_frame = ctk.CTkFrame(self.container_frame, fg_color='#222B36', corner_radius=22)
        self.login_frame.pack(side='left', fill='both', padx=40, pady=20, expand=True)

        # Google signup frame
        self.google_signup_frame = ctk.CTkFrame(self.container_frame, fg_color='#222B36', corner_radius=22)
        self.google_signup_frame.pack(side='right', fill='both', padx=(0, 40), pady=20, expand=True)

        # Signup frame
        self.signup_frame = SignupFrame(self.container_frame, controller=self)
        self.signup_frame.pack_forget()

        self.setup_ui()

    def setup_ui(self):
        self.pack(fill='both')

        # Set Profile Button

        self.center_frame_login = ctk.CTkFrame(self.login_frame, fg_color='#222B36')
        self.center_frame_login.pack(expand=True, anchor='center', fill='x', padx=20)

        self.default_profile = ctk.CTkImage(Image.open("assets/images/default_profile_picture.png"), size=(120, 120))

        self.profile_button = ctk.CTkButton(self.center_frame_login , width=120, height=120, image=self.default_profile, text='',
                                            fg_color='#222B36', hover_color='#737373', command=self.change_profile)

        self.welcome_label = ctk.CTkLabel(self.center_frame_login , text='Welcome Back!', font=("Arial", 35))


        # Email Entry
        self.email_entry = ctk.CTkEntry(self.center_frame_login , placeholder_text='E-mail',
                                        placeholder_text_color='#141A1F', corner_radius=22, border_color='white',
                                        fg_color='white', width=315, height=40, text_color='#141A1F')


        # Error label for email
        self.email_error_label = ctk.CTkLabel(self.center_frame_login , text='', font=("Arial", 15), text_color="red")


        # Password Frame
        self.password_frame = ctk.CTkFrame(self.center_frame_login , fg_color='white', corner_radius=22, bg_color='#222B36',
                                           height=35, width=300)


        # Password Entry
        self.password_entry = ctk.CTkEntry(self.password_frame, show="*", placeholder_text='Password',
                                           placeholder_text_color='#141A1F', corner_radius=22, border_color='white',
                                           fg_color='white', width=240, height=25, text_color='#141A1F')
        self.password_entry.pack(side="left", fill="both", expand=True, padx=7, pady=7)

        # Hide Icon
        self.hide_password_icon = ctk.CTkImage(Image.open("assets/images/hide_password.png"), size=(20, 20))

        # Hide and Show button
        self.show_password_button = ctk.CTkButton(self.password_frame, text='', width=60, height= 25,
                                                  text_color='black', hover_color='gray', fg_color='white',
                                                  command=self.toggle_password_visibility, corner_radius=22,
                                                  image=self.hide_password_icon)
        self.show_password_button.pack(side="left", padx=(0,7))

        # Error label for password
        self.password_error_label = ctk.CTkLabel(self.center_frame_login , text='', font=("Arial", 15), text_color="red")


        # Forgot password and sign up container

        # FRAMEEEEEEEEEE
        self.button_container_frame = ctk.CTkFrame(self.center_frame_login , fg_color='#222B36')


        # Forgot Password
        self.forgot_password_button = ctk.CTkButton(self.button_container_frame, text='Forgot Password?',
                                                    fg_color='#222B36', command=self.forgot_password)
        self.forgot_password_button.pack(side='left', padx=5)

        # Signup button
        self.signup_button = ctk.CTkButton(self.button_container_frame, text='Sign-Up', fg_color='#222B36',
                                           command=self.signup)
        self.signup_button.pack(side='right', padx=5)

        # Login Button
        self.login_button = ctk.CTkButton(self.center_frame_login , text="Login", command=self.login_button_click,
                                          corner_radius=24, width=120, height=45, fg_color='white', text_color='#141A1F')

        self.login_button.bind("<Return>", self.login_button_click)

        # Loading Frame
        self.loading = LoadingFrame(self.center_frame_login, fg_color="#222B36")

        # PACKING ALL LOGIN TANGINA
        self.profile_button.pack()
        self.welcome_label.pack(pady=40)
        self.email_entry.pack(fill='x')
        self.email_error_label.pack()
        self.password_frame.pack(fill='x')
        self.password_error_label.pack()
        self.button_container_frame.pack(pady=(0,10))
        self.login_button.pack(pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.center_frame_signup = ctk.CTkFrame(self.google_signup_frame, fg_color='#222B36')
        self.center_frame_signup.pack(expand=True, anchor='center', fill='x', padx=20)

        # Create a canvas to draw the lines and "or" text
        self.upper_line_canvas = tk.Canvas(self.center_frame_signup, width=400, height=40, bg='#222B36',
                                           highlightthickness=0)

        # Draw the left line
        self.upper_line_canvas.create_line(0, 20, 170, 20, fill='white', width=2)

        # Draw the right line
        self.upper_line_canvas.create_line(220, 20, 400, 20, fill='white', width=2)

        # Add "or" text
        self.upper_line_canvas.create_text(195, 20, text="or", fill='white', font=("Arial", 22))

        # Signup Widgets
        self.google_logo = ctk.CTkImage(Image.open("assets/images/google_logo.png"), size=(130, 130))

        self.google_signup_button = ctk.CTkButton(self.center_frame_signup, image=self.google_logo, text='',
                                                  corner_radius=100, fg_color='#222B36', command=self.google_signup)

        self.signup_label = ctk.CTkLabel(self.center_frame_signup, text='No account? Sign-Up', text_color='white')


        # Create a canvas to draw the lower line
        self.lower_line_canvas = tk.Canvas(self.center_frame_signup, width=400, height=40, bg='#222B36',
                                           highlightthickness=0)

        self.lower_line_canvas.create_line(0, 20, 400, 20, fill='white', width=2)

        self.upper_line_canvas.pack(pady=(0, 30))
        self.google_signup_button.pack(pady=(20,0))
        self.signup_label.pack(pady=(0, 20))
        self.lower_line_canvas.pack(pady=(30,0))

    def toggle_password_visibility(self):
        if self.password_entry.cget('show') == '*':
            self.password_entry.configure(show='')
            self.show_password_icon = ctk.CTkImage(Image.open("assets/images/show_password.png"), size=(20, 20))
            self.show_password_button.configure(text='', image=self.show_password_icon)
        else:
            self.password_entry.configure(show='*')
            self.show_password_button.configure(text='', image=self.hide_password_icon)

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
        self.login_frame.pack(side='left', fill='both', padx=40, pady=20, expand=True)
        self.google_signup_frame.pack(side='right', fill='both', padx=(0, 40), pady=20, expand=True)

    def google_signup(self):
        email = 'test1@gmail.com'
        password = 'test1'

        # Email domain validation
        valid_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        if email != "admin":
            domain = email.split('@')[-1]
            if domain not in valid_domains:
                messagebox.showerror("Input Error", "Please enter a valid email domain (gmail, yahoo, hotmail, outlook).")
                return

        # Start a new thread to make the request
        login_thread = threading.Thread(target=self.login, args=(email, password))
        login_thread.start()

    def login_button_click(self, event=None):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Clear previous error messages
        self.email_error_label.configure(text='')
        self.password_error_label.configure(text='')

        # Validation
        if not email or not password:
            if not email:
                self.email_error_label.configure(text="Please enter your email.")
            if not password:
                self.password_error_label.configure(text="Please enter your password.")
            return

        # Email domain validation
        valid_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        if email != "admin":
            domain = email.split('@')[-1]
            if domain not in valid_domains:
                self.email_error_label.configure(text="Please enter a valid email domain.")
                return

        # Start a new thread to make the request
        login_thread = threading.Thread(target=self.login, args=(email, password))
        login_thread.start()

        self.login_button.pack_forget()
        self.loading.pack(expand=True)

    def login(self, email: str, password: str):
        if not self.request_lock.acquire(blocking=False):
            print("LOGIN GUI: Login Request Prevented. A login request is already being processed.")
            return

        lock_acquired = True
        try:
            login_data = {'email': email, 'password': password}
            response = requests.post(LOGIN_ENDPOINT, json=login_data, timeout=10)
            if response.status_code == 200:
                self.master.after(0, self.callback, response.json())
            else:
                message = response.json()['message']
                self.master.after(0, lambda: self.display_error(message))
        except ConnectionError:
            self.master.after(0, lambda: self.display_error("Could not connect to server"))
        finally:

            if lock_acquired:
                self.request_lock.release()  # Release the lock

    def display_error(self, message):
        self.loading.pack_forget()
        self.login_button.pack(pady=10)
        if "password" in message.lower():
            self.password_error_label.configure(text=message)
        elif "email" in message.lower() or "account" in message.lower():
            self.email_error_label.configure(text=message)
        else:
            self.password_error_label.configure(text=message)
            self.email_error_label.configure(text=message)


