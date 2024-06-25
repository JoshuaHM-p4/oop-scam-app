import customtkinter as ctk
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common', 'searchbar')))

from searchbar import SearchBar

bg_color = "#222B36"
main_bg_color = "#333333"
second_main_bg_color = "#141a1f"

class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.main_frame = ctk.CTkFrame(self, fg_color = second_main_bg_color)
        self.main_frame.pack(side="top", fill="both", expand=True)

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
        self.notes_label = ctk.CTkLabel(self.notes_frame, text="Notes", font=("Arial", 30))
        self.notes_label.pack(side="top", fill="both", expand=True, pady=(100), padx=(20,10))

        self.event_calendar_frame = ctk.CTkFrame(self.frame_top, fg_color = bg_color, border_width = 10, border_color = second_main_bg_color, width = 1000, corner_radius = 40)
        self.event_calendar_frame.pack(side="left", fill="both", expand=True, padx = (0,10))
        self.event_calendar_label = ctk.CTkLabel(self.event_calendar_frame, text="Event Calendar", font=("Arial", 30), anchor="w")
        self.event_calendar_label.pack(side="top", fill="both", expand=True, pady=(100), padx=(450, 20))


        self.frame_bottom = ctk.CTkFrame(self.main_frame, fg_color = second_main_bg_color)
        self.frame_bottom.pack(side="top", fill="both", expand=True)

        self.templates = ctk.CTkFrame(self.frame_bottom, fg_color = bg_color, border_width = 10, border_color = second_main_bg_color, corner_radius = 40)
        self.templates.pack(side="left", fill="both", expand=True, padx=(10,0))
        self.templates_label = ctk.CTkLabel(self.templates, text="Templates", font=("Arial", 30))
        self.templates_label.pack(side="top", fill="both", expand=True, pady=(50,50), padx=(50))

        self.frame_bottom_right = ctk.CTkFrame(self.frame_bottom, fg_color = second_main_bg_color)
        self.frame_bottom_right.pack(side="left", fill="both", expand=True)

        self.task_scheduler = ctk.CTkFrame(self.frame_bottom_right, fg_color = bg_color, border_width = 10, border_color = second_main_bg_color, corner_radius = 40)
        self.task_scheduler.pack(side="top", fill="both", expand=True, padx=(0,10))
        self.task_scheduler_label = ctk.CTkLabel(self.task_scheduler, text="Task Scheduler", font=("Arial", 30))
        self.task_scheduler_label.pack(side="top", fill="both", expand=True, pady=50, padx=(50))

        self.progress_tracker = ctk.CTkFrame(self.frame_bottom_right, fg_color = bg_color, border_width = 10, border_color = second_main_bg_color, corner_radius = 40)
        self.progress_tracker.pack(side="top", fill="both", expand=True, padx=(0,10))
        self.progress_tracker_label = ctk.CTkLabel(self.progress_tracker, text="Progress Tracker", font=("Arial", 30))
        self.progress_tracker_label.pack(side="top", fill="both", expand=True, pady=(50), padx=(50))