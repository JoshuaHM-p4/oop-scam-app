import customtkinter as ctk
from config import BACKGROUND_COLOR, FONT_FAMILY
from PIL import Image
import sys,os

class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.main_app: ctk.CTk = master.main_app
        self.user: str = ""
        self.__user_id: int = 0
        self.username: str = ""
        self.email: str = ""

        # Initialize the username variable | self.username
        self.username_var = ctk.StringVar(value=self.username) # dummy username

        # Initialize the email variable | self.email
        self.email_var = ctk.StringVar(value=self.email) # dummy email

        self.default_profile = ctk.CTkImage(Image.open("assets/images/default_profile_picture.png"), size=(40, 40))
        self.dp_label = ctk.CTkLabel(self, image=self.default_profile, text=" ")

        self.user_email_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        self.username_label = ctk.CTkLabel(self.user_email_frame, textvariable=self.username_var, 
                                           height=2, font=(FONT_FAMILY, 21, 'bold'))
        self.email_label = ctk.CTkLabel(self.user_email_frame, textvariable=self.email_var, 
                                           height=2, font=(FONT_FAMILY, 12))

    def pack(self, *args, **kwargs):
        self.dp_label.pack(side='left', padx=5, pady=[20, 15])
        self.user_email_frame.pack(side='top', padx=[8, 0], pady=20, anchor=ctk.W)
        self.username_label.pack(anchor=ctk.W)
        self.email_label.pack(anchor=ctk.W)

        super().pack(*args, **kwargs)

    def set_user(self, username, email, user_id):
        self.username_var.set(username)
        self.email_var.set(email)
        self.__user_id = user_id

class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, master, command, frames):
        super().__init__(master)
        self.module_frames = frames
        self.features = []  # Initialize features list here
        show_frame = command

        self.buttons_container = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)  # Frame for the other buttons
        self.buttons_container.pack(side='top', fill='both')

        self.settings_container = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)  # Frame for the settings button
        self.settings_container.pack(side='top', fill='both', expand=True)

        for i, feature in enumerate(self.module_frames):
            frame_name = feature.__name__

            print(f"Frame Name: {frame_name}")
            
            if frame_name != 'ExitFrame':
                button = ctk.CTkButton(
                    self.buttons_container,
                    text=frame_name[:-5].upper(),
                    width=200,
                    height=40,
                    corner_radius=25,
                    anchor='w',
                    font=(FONT_FAMILY, 16),
                    fg_color='transparent',
                    hover_color='#222B36',
                    command=lambda frame_name=frame_name: show_frame(frame_name)
            )

            else:
                button = ctk.CTkButton(
                    self.settings_container,
                    text='X  ' + frame_name[:-5].upper(),
                    width=200,
                    height=40,
                    corner_radius=25,
                    anchor='w',
                    font=(FONT_FAMILY, 16),
                    fg_color='transparent',
                    hover_color='#222B36',
                    command=lambda frame_name=frame_name: show_frame(frame_name)
                 )
            if frame_name != 'ExitFrame':
                button.pack(pady=2, fill='x', expand=True)
            else: # 
                button.pack(pady=(0, 5), fill='x', side='bottom')
            button.bind("<Button-1>", self.create_click_handler(button))
            self.features.append(button)

    def create_click_handler(self, button):
        def select(event=None):
            self.clear_active_button()
            button.configure(fg_color='#222B36')
        return select

    def clear_active_button(self):
        for feature_btn in self.features:
            feature_btn.configure(fg_color='transparent')

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, command, frames: list[ctk.CTkFrame],  *args, **kwargs):
        super().__init__(master, *args, **kwargs) # self: Parent Dashboard Frame
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack_configure(padx=15, pady=15)
        self.main_app = master
        self.profile_frame = ProfileFrame(self) # profile_frame: Profile Frame
        dashboard_image = ctk.CTkImage(Image.open("./assets/images/dashboard_logo.png"), size=(250, 50))
        self.label = ctk.CTkLabel(self, image=dashboard_image, text=" ")
        self.button_container = ButtonsFrame(self, command=command, frames=frames) # button_Continer: Container for Dashboard Buttons

    def pack(self, *args, **kwargs):
        self.profile_frame.pack(padx=25, fill='x')
        self.profile_frame.configure(fg_color=BACKGROUND_COLOR)
        self.label.pack(pady=5)
        self.button_container.pack(padx=8, pady=8, fill='both', expand=True)
        self.button_container.configure(fg_color=BACKGROUND_COLOR)
        super().pack(*args, **kwargs)

    def set_user(self, username, email, user_id):
        self.profile_frame.set_user(username, email, user_id)