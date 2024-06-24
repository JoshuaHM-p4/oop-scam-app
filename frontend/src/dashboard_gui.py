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
    def __init__(self, master, command, frames):
        super().__init__(master)
        self.module_frames = frames
        show_frame = command

        for i, feature in enumerate(self.module_frames):
            frame_name = feature.__name__
            button = ctk.CTkButton(
                self,
                text=frame_name,
                command=lambda frame_name=frame_name: show_frame(frame_name)
            ) # Lambda function assigns button to show_frame method
            button.pack(side='top', fill='x', expand=True)

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, command, frames: list[ctk.CTkFrame],  *args, **kwargs):
        super().__init__(master, *args, **kwargs) # self: Parent Dashboard Frame
        self.label = ctk.CTkLabel(self, text="Dashboard")
        self.profile_frame = ProfileFrame(self) # profile_frame: Profile Frame
        self.button_container = ButtonsFrame(self, command=command, frames=frames) # button_Continer: Container for Dashboard Buttons

    def pack(self, *args, **kwargs):
        self.label.pack()
        self.profile_frame.pack()
        self.button_container.pack()
        super().pack(*args, **kwargs)

