import customtkinter as ctk
from config import BACKGROUND_COLOR

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
        show_frame = command
        self.features = []

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
            ) # Lambda function assigns button to show_frame method
            button.pack(side='top', pady=3, fill='x', expand=True)
            button.bind("<Button-1>", self.create_click_handler(button))
            self.features.append(button)
    
    def create_click_handler(self, button):
        def select(event=None):
            for feature_btn in self.features:
                feature_btn.configure(fg_color='transparent')
            button.configure(fg_color='#222B36')
        return select

class SettingsButton(ctk.CTkFrame):
    def __init__(self, master, command):
        super().__init__(master)
        self.button = ctk.CTkButton(
            self,
            text="Settings",
            width=200,
            height=40,
            corner_radius=25,
            fg_color='transparent',
            hover_color='#222B36',
            command=command
        )
        self.button.pack(side='bottom', pady=3, fill='x', expand=True)
        self.button.bind("<Button-1>", self.create_click_handler(self.button))
    
    def create_click_handler(self, button):
        def select(event=None):
            button.configure(fg_color='#222B36')
        return select

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, command, frames: list[ctk.CTkFrame],  *args, **kwargs):
        super().__init__(master, *args, **kwargs) # self: Parent Dashboard Frame
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack_configure(padx=15, pady=15)
        self.profile_frame = ProfileFrame(self) # profile_frame: Profile Frame
        self.label = ctk.CTkLabel(self, text="Dashboard")
        self.button_container = ButtonsFrame(self, command=command, frames=frames) # button_Continer: Container for Dashboard Buttons
        self.settings_button = SettingsButton(self, command=command)

    def pack(self, *args, **kwargs):
        self.profile_frame.pack()
        self.profile_frame.configure(width=200, height=80, fg_color=BACKGROUND_COLOR)
        self.label.pack()
        self.label.configure(width=200, height=50)
        self.button_container.pack(padx=8, pady=8)
        self.button_container.configure(fg_color=BACKGROUND_COLOR)
        self.settings_button.pack(side='bottom', padx=8, pady=8)
        self.settings_button.configure(fg_color=BACKGROUND_COLOR)
        super().pack(*args, **kwargs)