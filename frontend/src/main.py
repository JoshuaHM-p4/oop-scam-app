import tkinter as tk
import sys
import os

# Widgets
from auth import LoginFrame
from notes import NotesFrame
from home import HomeFrame

# Append the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import APP_NAME, BACKGROUND_COLOR

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(APP_NAME)
        self.attributes('-fullscreen', True)
        self.configure(bg=BACKGROUND_COLOR)
        self.feature_frames = (HomeFrame, NotesFrame)
        self.frames = {}

        self.create_widgets()
        self.init_frames()

    def create_widgets(self):
        # Main Container Frame for SCAM App Features
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dashboard Buttons
        for F in self.feature_frames:
            frame_name = F.__name__
            button = tk.Button(self, text=frame_name, command=lambda frame_name=frame_name: self.show_frame(frame_name))
            button.pack()

    def init_frames(self):
        # Initialize frames
        self.frames = {}
        for F in self.feature_frames:
            frame_name = F.__name__
            print(frame_name)
            frame_object = F(self.container, self)
            self.frames[frame_name] = frame_object
            frame_object.grid(row=0, column=0, sticky="nsew")

        # Add the Login Frame
        login_frame = LoginFrame(self.container, self)
        self.frames["LoginFrame"] = login_frame
        login_frame.grid(row=0, column=0, sticky="nsew")

        # Show the initial frame
        self.show_frame("LoginFrame")

    def show_frame(self, frame_class):
        """Show a frame for the given class."""
        frame = self.frames[frame_class]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
