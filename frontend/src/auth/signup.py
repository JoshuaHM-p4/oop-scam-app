import customtkinter as ctk
from tkinter import messagebox
import requests
import threading
from PIL import Image

SIGNUP_ENDPOINT = "http://localhost:5000/auth/register"


class SignupFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color='#141A1F')
        self.controller = controller
        self.request_lock = threading.Lock()

        self.setup_ui()

    def setup_ui(self):
        # Back button
        self.back_button_logo = ctk.CTkImage(Image.open("assets/images/left_arrow.png"), size=(25, 25))
        self.back_button = ctk.CTkButton(self, text='Login page', text_color='white', fg_color='#141A1F',
                                         hover_color='gray',
                                         command=self.return_login, corner_radius=10, image=self.back_button_logo,
                                         width=50, height=25)
        self.back_button.pack(side='top', anchor='nw', padx=15, pady=(15, 0))

        # Frame for logo and title
        self.logo_frame = ctk.CTkFrame(self, fg_color='#141A1F')
        self.logo_frame.pack(pady=5, padx=10)

        self.app_logo = ctk.CTkImage(Image.open("assets/images/app_logo.png"), size=(200, 200))
        self.app_label = ctk.CTkLabel(self.logo_frame, image=self.app_logo, text='')
        self.app_label.pack(side='left', padx=(0, 10))

        self.title_label = ctk.CTkLabel(self.logo_frame, text="S.C.A.M", text_color='white', font=('Montserrat', 50))
        self.title_label.pack(side='left', padx=(10, 0))

        # Create a container frame for labels, entries, and button
        self.container_frame = ctk.CTkFrame(self, fg_color='#141A1F')
        self.container_frame.pack(pady=(90, 10), padx=10)

        # Email Label and Entry
        self.email_label_frame = ctk.CTkFrame(self.container_frame, fg_color='#141A1F')
        self.email_label_frame.pack(anchor='w')
        self.email_label = ctk.CTkLabel(self.email_label_frame, text="   Email:", text_color='white')
        self.email_label.pack(side='left')
        self.email_error_label = ctk.CTkLabel(self.email_label_frame, text='', font=("Arial", 12), text_color="red")
        self.email_error_label.pack(side='left', padx=10)
        self.email_entry = ctk.CTkEntry(self.container_frame, placeholder_text='Email', corner_radius=10, width=300,
                                        height=40, text_color='#141A1F', fg_color='white', border_color='#141A1F')
        self.email_entry.pack(anchor='w', pady=10)

        # Username Label and Entry
        self.username_label_frame = ctk.CTkFrame(self.container_frame, fg_color='#141A1F')
        self.username_label_frame.pack(anchor='w')
        self.username_label = ctk.CTkLabel(self.username_label_frame, text="   Username:", text_color='white')
        self.username_label.pack(side='left')
        self.username_error_label = ctk.CTkLabel(self.username_label_frame, text='', font=("Arial", 12), text_color="red")
        self.username_error_label.pack(side='left', padx=10)
        self.username_entry = ctk.CTkEntry(self.container_frame, placeholder_text='Username', corner_radius=10,
                                           width=300, height=40, text_color='#141A1F', fg_color='white',
                                           border_color='#141A1F')
        self.username_entry.pack(anchor='w', pady=10)

        # Password Label and Entry
        self.password_label_frame = ctk.CTkFrame(self.container_frame, fg_color='#141A1F')
        self.password_label_frame.pack(anchor='w')
        self.password_label = ctk.CTkLabel(self.password_label_frame, text="   Password:", text_color='white')
        self.password_label.pack(side='left')
        self.password_error_label = ctk.CTkLabel(self.password_label_frame, text='', font=("Arial", 12), text_color="red")
        self.password_error_label.pack(side='left', padx=10)

        self.password_frame = ctk.CTkFrame(self.container_frame, fg_color='white', corner_radius=10,
                                           height=40, width=300)
        self.password_frame.pack(anchor='w', pady=10)

        self.password_entry = ctk.CTkEntry(self.password_frame, placeholder_text='Password', show="*", corner_radius=10,
                                           width=220, height=20, text_color='#141A1F', fg_color='white',
                                           border_color='white')
        self.password_entry.pack(anchor='w', pady=7, padx=7, side='left', fill='y')

        # Hide Icon
        self.hide_password_icon = ctk.CTkImage(Image.open("assets/images/hide_password.png"), size=(20, 20))

        # Hide and Show Icon
        self.show_password_button = ctk.CTkButton(self.password_frame, text='', width=60, height=25,
                                                  text_color='black', hover_color='gray', fg_color='white',
                                                  command=self.toggle_password_visibility, corner_radius=22,
                                                  image=self.hide_password_icon)
        self.show_password_button.pack(side="right", padx=(0, 5))

        # Signup Button
        self.signup_button = ctk.CTkButton(self.container_frame, text="Signup", command=self.signup_button_click,
                                           hover_color='navy blue',
                                           width=120, height=40, corner_radius=10)
        self.signup_button.pack(pady=30)

    def toggle_password_visibility(self):
        if self.password_entry.cget('show') == '*':
            self.password_entry.configure(show='')
            self.show_password_icon = ctk.CTkImage(Image.open("assets/images/show_password.png"), size=(20, 20))
        else:
            self.password_entry.configure(show='*')
            self.show_password_icon = ctk.CTkImage(Image.open("assets/images/hide_password.png"), size=(20, 20))
        self.show_password_button.configure(image=self.show_password_icon)

    def return_login(self):
        self.controller.return_to_login()

    def signup_button_click(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()

        # Clear previous error messages
        self.username_error_label.configure(text='')
        self.password_error_label.configure(text='')
        self.email_error_label.configure(text='')

        # Validation
        if not email or not password or not username:
            if not email:
                self.email_error_label.configure(text="Please enter your email.")
            if not username:
                self.username_error_label.configure(text="Please enter your username.")
            if not password:
                self.password_error_label.configure(text="Please enter your password.")
            return

        # Email domain validation
        valid_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        domain = email.split('@')[-1]
        if domain not in valid_domains:
            self.email_error_label.configure(text="Please enter a valid email domain.")
            return

        # Start a new thread to make the request
        signup_thread = threading.Thread(target=self.signup, args=(username, password, email))
        signup_thread.start()

    def signup(self, username, password, email):
        if not self.request_lock.acquire(blocking=False):
            print("SIGNUP GUI: Signup Request Prevented. A signup request is already being processed.")
            return

        try:
            signup_data = {'username': username, 'password': password, 'email': email}
            response = requests.post(SIGNUP_ENDPOINT, json=signup_data, timeout=10)
            message = response.json()['message']
            if response.status_code == 201:
                self.master.after(0, lambda: self.display_success(message))
            else:
                self.master.after(0, lambda: self.display_error(message))
        except ConnectionError:
            self.master.after(0, lambda: self.display_error("Could not connect to server"))
        finally:
            self.request_lock.release()  # Release the lock

    def display_error(self, message):
        if "password" in message.lower():
            self.password_error_label.configure(text=message)
        elif "email" in message.lower():
            self.email_error_label.configure(text=message)
        elif "username" in message.lower():
            self.username_error_label.configure(text=message)
        else:
            self.password_error_label.configure(text=message)
            self.email_error_label.configure(text=message)
            self.username_error_label.configure(text=message)

    def display_success(self, message):
        messagebox.showinfo("Signup Successful", message)
        self.return_login()
