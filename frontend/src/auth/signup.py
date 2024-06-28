import customtkinter as ctk
from PIL import Image

class SignupFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color='#141A1F')
        self.controller = controller

        self.setup_ui()


    def setup_ui(self):
        # Back button
        self.back_button_logo = ctk.CTkImage(Image.open("assets/images/back_button.png"), size=(25, 25))
        self.back_button = ctk.CTkButton(self, text='Login page', text_color='#141A1F', fg_color='#141A1F', hover_color='gray',
                                         command=self.return_login, corner_radius=10, image=self.back_button_logo,
                                         width=50, height=25)
        self.back_button.pack(side='top', anchor='nw', padx=15, pady=(15, 0))

        # Frame for logo and title
        self.logo_frame = ctk.CTkFrame(self, fg_color='#141A1F')
        self.logo_frame.pack(pady=5, padx=10)

        self.app_logo = ctk.CTkImage(Image.open("assets/images/app_logo.png"), size=(90, 90))
        self.app_label = ctk.CTkLabel(self.logo_frame, image=self.app_logo, text='')
        self.app_label.pack(side='left', padx=(0, 10))

        self.title_label = ctk.CTkLabel(self.logo_frame, text="S.C.A.M", text_color='white', font=('Montserrat', 50))
        self.title_label.pack(side='left', padx=(10, 0))

        # Create a container frame for labels, entries, and button
        self.container_frame = ctk.CTkFrame(self, fg_color='#141A1F')
        self.container_frame.pack(pady=5, padx=10, expand=True)

        # Email Label and Entry
        self.email_label = ctk.CTkLabel(self.container_frame, text="   Email:", text_color='white')
        self.email_label.pack(anchor='w')
        self.email_entry = ctk.CTkEntry(self.container_frame, placeholder_text='Email', corner_radius=10, width=300,
                                        height=30, text_color='#141A1F', fg_color='#D9D9D9', border_color='navy blue')
        self.email_entry.pack(anchor='w')

        # Username Label and Entry
        self.username_label = ctk.CTkLabel(self.container_frame, text="   Username:", text_color='white')
        self.username_label.pack(anchor='w')
        self.username_entry = ctk.CTkEntry(self.container_frame, placeholder_text='Username', corner_radius=10, width=300,
                                           height=30, text_color='#141A1F', fg_color='#D9D9D9', border_color='navy blue')
        self.username_entry.pack(anchor='w')

        # Password Label and Entry
        self.password_label = ctk.CTkLabel(self.container_frame, text="   Password:", text_color='white')
        self.password_label.pack(anchor='w')
        self.password_entry = ctk.CTkEntry(self.container_frame, placeholder_text='Password', show="*", corner_radius=10, width=300,
                                           height=30, text_color='#141A1F', fg_color='#D9D9D9', border_color='navy blue')
        self.password_entry.pack(anchor='w', pady=(0, 5))

        # Signup Button
        self.signup_button = ctk.CTkButton(self.container_frame, text="Signup", command=self.signup, hover_color='navy blue',
                                           width=120, height=40, corner_radius=10)
        self.signup_button.pack(pady=15)

    def return_login(self):
        print('Return to login page')

    def signup(self):
        # Implement signup logic here
        print("Signing up...")
        # Example: validate credentials and switch frame
        self.controller.show_frame("NotesFrame")