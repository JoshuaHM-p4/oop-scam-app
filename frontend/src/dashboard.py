import customtkinter as ctk

class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.username_var = ctk.StringVar(value="Joshua")
        self.email_var = ctk.StringVar(value="joshuahm.2004@gmail.com")
        self.__user_id = 0

        self.username_label = ctk.CTkLabel(self, textvariable=self.username_var)
        self.email_label = ctk.CTkLabel(self, textvariable=self.email_var)

        self.canvas = ctk.CTkCanvas(self, bg='white')

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
    def __init__(self, master, main_app, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.main_app = main_app # main app
        self.feature_frames = main_app.module_frames

    def pack(self, *args, **kwargs):
        # Dashboard Buttons
        for i, feature in enumerate(self.feature_frames):
            frame_name = feature.__name__
            button = ctk.CTkButton(
                self,
                text=frame_name,
                command=lambda frame_name=frame_name: self.main_app.show_frame(frame_name)
            ) # Lambda function assigns button to show_frame method
            button.grid(row=i, column=0, sticky="ew")

        super().pack(*args, **kwargs)

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master) # self: Parent Dashboard Frame

        self.label = ctk.CTkLabel(self, text="Dashboard")
        self.profile_frame = ProfileFrame(self) # profile_frame: Profile Frame
        self.button_container = ButtonsFrame(self, main_app=master) # button_Continer: Container for Dashboard Buttons

    def create_widgets(self):
        self.label.pack()
        self.profile_frame.pack()
        self.button_container.pack()