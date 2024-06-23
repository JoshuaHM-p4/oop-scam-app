import tkinter as tk
import sys
import os

from dashboard import DashboardFrame

# Module Frames for SCAM App Features
from auth import LoginFrame
from notes import NotesFrame
from home import HomeFrame
from templates import TemplatesFrame
from event_calendar import CalendarFrame
from tasks import TasksFrame
from flashcards import FlashcardsFrame
from progress import ProgressFrame
from collaboration import CollaborationFrame

# Append the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import APP_NAME, BACKGROUND_COLOR

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(APP_NAME)
        self.attributes('-fullscreen', True)
        self.configure(bg=BACKGROUND_COLOR)

        # Session Attributes
        self.__user_id = ""
        self.__username = ""
        self.__email = ""
        self.__access_token = ""

        # Main Screen Widgets
        self.module_frames = (
            HomeFrame,
            NotesFrame,
            TemplatesFrame,
            CalendarFrame,
            TasksFrame,
            FlashcardsFrame,
            ProgressFrame,
            CollaborationFrame
        )
        self.main_screen_frames = {}
        self.container = self.dashboard_frame = None

        self.init_loginFrame()

    def create_mainScreen(self):
        # Dashboarad Frme
        self.dashboard_frame = DashboardFrame(self)
        self.dashboard_frame.create_widgets()
        self.dashboard_frame.pack(side='left', expand=True, fill='both')

        # Main Container Frame for SCAM App Features
        self.container = tk.Frame(self)
        self.container.pack(side='left', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def init_loginFrame(self) -> None:
        # Add the Login Frame
        self.login_frame = LoginFrame(self.container, callback=self.set_session_data)
        self.login_frame.pack(expand=True)

    def on_login_success(self) -> None:
        print(f'Login Successful!, Welcome {self.__username}')
        self.login_frame.destroy()

        self.create_mainScreen()
        self.init_moduleFrames()
        self.show_frame("HomeFrame")

    def set_session_data(self, data) -> None:
        self.__user_id = data['user_id']
        self.__username = data['username']
        self.__email = data['email']
        self.__access_token = data['access_token']
        self.on_login_success()

    def init_moduleFrames(self) -> None:
        # Initialize frames for each modules
        for frame in self.module_frames:
            frame_name = frame.__name__

            frame_object = frame(self.container, self)

            self.main_screen_frames[frame_name] = frame_object

            frame_object.grid(row=0, column=0, sticky="nsew")

            print(f"{frame_name} loaded successfully!")

    def show_frame(self, frame_name: str):
        """Show a frame for the given module class to the container."""
        frame = self.main_screen_frames[frame_name]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
