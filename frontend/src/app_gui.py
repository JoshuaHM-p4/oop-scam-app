import customtkinter as ctk

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


# Refactor for MainApp class separating self.container frame from the MainApp
class AppFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

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

        for frame in self.module_frames:
            frame_name = frame.__name__
            frame_object = frame(self, self.master)
            self.main_screen_frames[frame_name] = frame_object
            frame_object.grid(row=0, column=0, sticky="nsew")

            print(f"{frame_name} loaded successfully!")

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show_frame(self, frame_name: str):
        """Show a frame for the given module class to the container."""
        frame = self.main_screen_frames[frame_name]
        frame.tkraise()