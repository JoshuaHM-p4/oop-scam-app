import customtkinter as ctk
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common', 'searchbar')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # frontend/

from searchbar import SearchBar
from config import BACKGROUND_COLOR

bg_color = "#222B36"
main_bg_color = "#333333"
second_main_bg_color = "#141a1f"
hovering_color = "#525AAA"

class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)

        self.main_frame = ctk.CTkFrame(self, fg_color = second_main_bg_color)
        self.main_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.frame_top_top = ctk.CTkFrame(self.main_frame, fg_color = second_main_bg_color, corner_radius = 100)
        self.frame_top_top.pack(side="top", fill="x")

        self.label = ctk.CTkLabel(self.frame_top_top, text="WHAT WILL YOU DO TODAY?", font=("Arial", 40))
        self.label.pack(side="left", fill="x", pady=10, padx=20)

        self.searchbar = SearchBar(self.main_frame)
        self.searchbar.pack(side="top", fill="x", pady=1)


        self.frame_top = ctk.CTkFrame(self.main_frame, fg_color = second_main_bg_color)
        self.frame_top.pack(side="top", fill="both", expand=True)

        self.notes_frame = ctk.CTkFrame(self.frame_top, fg_color = bg_color, border_width = 10, border_color = second_main_bg_color, corner_radius = 40)
        self.notes_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
        self.notes_label = ctk.CTkButton(self.notes_frame, text="Notes", font=("Arial", 30), fg_color = bg_color, hover_color = hovering_color, corner_radius = 100)
        self.notes_label.pack(side="top", fill="both", expand=True, pady=(20), padx=(20, 20))
        self.notes_label.bind("<Button-1>", lambda event: self.notes_button_click())
        self.notes_frame.bind("<Button-1>", lambda event: self.notes_button_click())

        self.event_calendar_frame = ctk.CTkFrame(self.frame_top, fg_color = bg_color, border_width = 10, border_color = second_main_bg_color, corner_radius = 40)
        self.event_calendar_frame.pack(side="left", fill="both", expand=True, padx = (0,10))
        self.event_calendar_label = ctk.CTkButton(self.event_calendar_frame, text="Event Calendar", font=("Arial", 30), fg_color = bg_color, hover_color = hovering_color, corner_radius = 100)
        self.event_calendar_label.pack(side="top", fill="both", expand=True, pady=(20), padx=(20, 20))
        self.event_calendar_frame.bind("<Button-1>", lambda event: self.event_calender_click())
        self.event_calendar_label.bind("<Button-1>", lambda event: self.event_calender_click())

        self.frame_bottom = ctk.CTkFrame(self.main_frame, fg_color = second_main_bg_color)
        self.frame_bottom.pack(side="top", fill="both", expand=True)

        self.templates = ctk.CTkFrame(self.frame_bottom, fg_color = bg_color, border_width = 10, border_color = second_main_bg_color, corner_radius = 40)
        self.templates.pack(side="left", fill="both", expand=True, padx=(10,0))
        self.templates_label = ctk.CTkButton(self.templates, text="Templates", font=("Arial", 30), fg_color = bg_color, hover_color = hovering_color, corner_radius = 100)
        self.templates_label.pack(side="top", fill="both", expand=True, pady=(20), padx=(20))
        self.templates_label.bind("<Button-1>", lambda event: self.templates_button_click())
        self.templates.bind("<Button-1>", lambda event: self.templates_button_click())

        self.frame_bottom_right = ctk.CTkFrame(self.frame_bottom, fg_color = second_main_bg_color)
        self.frame_bottom_right.pack(side="left", fill="both", expand=True)

        self.task_scheduler = ctk.CTkFrame(self.frame_bottom_right, fg_color = bg_color, border_width = 10, border_color = second_main_bg_color, corner_radius = 40)
        self.task_scheduler.pack(side="top", fill="both", expand=True, padx=(0,10))
        self.task_scheduler_label = ctk.CTkButton(self.task_scheduler, text="Task Scheduler", font=("Arial", 30), fg_color = bg_color, hover_color = hovering_color, corner_radius = 100)
        self.task_scheduler_label.pack(side="top", fill="both", expand=True, pady=20, padx=(20))
        self.task_scheduler_label.bind("<Button-1>", lambda event: self.task_scheduler_button_click())
        self.task_scheduler.bind("<Button-1>", lambda event: self.task_scheduler_button_click())

        self.progress_tracker = ctk.CTkFrame(self.frame_bottom_right, fg_color = bg_color, border_width = 10, border_color = second_main_bg_color, corner_radius = 40)
        self.progress_tracker.pack(side="top", fill="both", expand=True, padx=(0,10))
        self.progress_tracker_label = ctk.CTkButton(self.progress_tracker, text="Progress Tracker", font=("Arial", 30), fg_color = bg_color, hover_color = hovering_color, corner_radius = 100)
        self.progress_tracker_label.pack(side="top", fill="both", expand=True, pady=(20), padx=(20))
        self.progress_tracker_label.bind("<Button-1>", lambda event: self.progress_tracker_button_click())
        self.progress_tracker.bind("<Button-1>", lambda event: self.progress_tracker_button_click())

    def notes_button_click(self):
        print("geraldo")

    def event_calender_click(self):
        print("event calender")
    
    def templates_button_click(self):
        print("templates")

    def task_scheduler_button_click(self):
        print("task scheduler")
    
    def progress_tracker_button_click(self):
        print("progress tracker")

