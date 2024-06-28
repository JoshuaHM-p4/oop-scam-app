import customtkinter as ctk
from config import BACKGROUND_COLOR
from PIL import Image

class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.username_var = ctk.StringVar(value="Joshua")
        self.email_var = ctk.StringVar(value="joshuahm.2004@gmail.com")
        self.__user_id = 0

        self.username_label = ctk.CTkLabel(self, textvariable=self.username_var)
        self.email_label = ctk.CTkLabel(self, textvariable=self.email_var)

    def pack(self, *args, **kwargs):
        # Profile Image
        # Profile Username
        # Profile Email

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

        for i, feature in enumerate(self.module_frames):
            frame_name = feature.__name__
            button = ctk.CTkButton(
                self,
                text=frame_name[:-5],
                width=200,
                height=40,
                corner_radius=25,
                fg_color='transparent',
                hover_color='#222B36',
                command=lambda frame_name=frame_name: show_frame(frame_name)
            )
            button.pack(side='top', pady=3, fill='x', expand=True)
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

class SettingsButton(ctk.CTkFrame):
    def __init__(self, master, command, buttons_container):
        super().__init__(master)
        self.buttons_container = buttons_container
        settings_button_image = ctk.CTkImage(Image.open("../assets/images/settings_logo.png"), size=(15, 15))
        self.settings_button = ctk.CTkButton(
            self,
            image=settings_button_image,    
            text="Settings",
            width=200,
            height=40,
            corner_radius=25,
            fg_color='transparent',
            hover_color='#222B36',
            command=command
        )
        self.settings_button.pack(side='bottom', pady=3, fill='x', expand=True)
        self.settings_button.bind("<Button-1>", self.create_click_handler(self.settings_button))

    def create_click_handler(self, button):
        self.buttons_container.clear_active_button()
        def select(event=None):
            button.configure(fg_color='#222B36')
        return select

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, command, frames: list[ctk.CTkFrame],  *args, **kwargs):
        super().__init__(master, *args, **kwargs) # self: Parent Dashboard Frame
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack_configure(padx=15, pady=15)
        self.profile_frame = ProfileFrame(self) # profile_frame: Profile Frame
        dashboard_image = ctk.CTkImage(Image.open("../assets/images/dashboard_logo.png"), size=(250, 50))
        self.label = ctk.CTkLabel(self, image=dashboard_image, text=" ")
        self.button_container = ButtonsFrame(self, command=command, frames=frames) # button_Continer: Container for Dashboard Buttons
        self.settings_button = SettingsButton(self, command=command, buttons_container=self.button_container)

    def pack(self, *args, **kwargs):
        self.profile_frame.pack()
        self.profile_frame.configure(width=200, height=80, fg_color=BACKGROUND_COLOR)
        self.label.pack()
        self.button_container.pack(padx=8, pady=8)
        self.button_container.configure(fg_color=BACKGROUND_COLOR)
        self.settings_button.pack(side='bottom', padx=8, pady=8)
        self.settings_button.configure(fg_color=BACKGROUND_COLOR)
        super().pack(*args, **kwargs)