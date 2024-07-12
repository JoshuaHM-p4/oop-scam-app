import customtkinter as ctk
import os, sys
from tkinter.simpledialog import askstring
import tkinter.messagebox as messagebox
from tkinter import simpledialog, messagebox
from PIL import Image

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

        self.notes_frame = self.create_button_frame(self.frame_top, "Notes", self.notes_button_click)
        self.event_calendar_frame = self.create_button_frame(self.frame_top, "Event Calendar", self.event_calender_click)

        self.frame_bottom = ctk.CTkFrame(self.main_frame, fg_color = second_main_bg_color)
        self.frame_bottom.pack(side="top", fill="both", expand=True)

        self.templates = self.create_button_frame(self.frame_bottom, "Templates", self.templates_button_click)

        self.task_scheduler = self.create_button_frame(self.frame_bottom, "Task Scheduler", self.task_scheduler_button_click)
        self.progress_tracker = self.create_button_frame(self.frame_bottom, "Progress Tracker", self.progress_tracker_button_click)

        # Edit button
        self.edit_img = ctk.CTkImage(Image.open("assets/images/edit.png").resize((40, 40)))
        self.edit_button = ctk.CTkButton(self.frame_top_top, text="", font=("Arial", 20), command=self.edit_button_click, fg_color = bg_color,
                                         image=self.edit_img, width=40, height=40, corner_radius=20)
        self.edit_button.pack(side="right", pady=10, padx = 10)
        self.add_button_img = ctk.CTkImage(Image.open("assets/images/plus.png").resize((40, 40)))
        self.add_button = ctk.CTkButton(self.frame_top_top, text="", font=("Arial", 20), command=self.add_button_click, fg_color = bg_color, 
                                        image=self.add_button_img, width=40, height=40, corner_radius=100)
        self.add_button.pack(side="right", pady=10, padx = 10)

        self.delete_img = ctk.CTkImage(Image.open("assets/images/trash_white.png").resize((40, 40)))
        self.delete_button = ctk.CTkButton(self.frame_top_top, text="", font=("Arial", 20), command=self.delete_button_click, fg_color = bg_color,
                                           image=self.delete_img, width=40, height=40, corner_radius=20)
        self.delete_button.pack(side="right", pady=10, padx = 10)

        self.button_labels = ["Note", "Event Calendar", "Template", "Task Scheduler", "Progress Tracker"]
        self.all_buttons_labels = ["Note", "Event Calendar", "Template", "Task Scheduler", "Progress Tracker", "Flashcard", "Collaboration"]

    def delete_button_click(self):
        target_button = askstring("Delete Button", "Enter button you want to delete:")
        if target_button in self.button_labels:
            for i in self.button_labels:
                if target_button == i:
                    self.button_labels.remove(i)
                    if target_button == "Note":
                        self.notes_frame.pack_forget()
                        self.notes_frame.destroy()
                    elif target_button == "Event Calendar":
                        self.event_calendar_frame.pack_forget()
                        self.event_calendar_frame.destroy()
                    elif target_button == "Template":
                        self.templates.pack_forget()
                        self.templates.destroy()
                    elif target_button == "Task Scheduler":
                        self.task_scheduler.pack_forget()
                        self.task_scheduler.destroy()
                    elif target_button == "Progress Tracker":
                        self.progress_tracker.pack_forget()
                        self.progress_tracker.destroy()
                    elif target_button == "Flashcard":
                        self.flashcard.pack_forget()
                        self.flashcard.destroy()
                    elif target_button == "Collaboration":
                        self.collaboration.pack_forget()
                        self.collaboration.destroy()
        else:
            messagebox.showerror("Error", "Button not found")

    def add_button_click(self):
        if len(self.button_labels) == 7:
            messagebox.showerror("Error", "Cannot add more than 7 buttons")
            return
        while True:
            text = askstring("Add Button", "Enter new button label:")
            if text in self.all_buttons_labels:
                if text in self.button_labels:
                    messagebox.showerror("Error", "Button already exists")
                    continue
                new_text = text
                new_command = self.choose_new_command(new_text)
                self.button_labels.append(new_text)
                if new_command:
                    if new_text == "Note":
                        self.notes_frame = self.create_button_frame(self.higher_number_of_widgets_in_frame(), new_text, new_command)
                        break
                    if new_text == "Event Calendar":
                        self.event_calendar_frame = self.create_button_frame(self.higher_number_of_widgets_in_frame(), new_text, new_command)
                        break
                    if new_text == "Template":
                        self.templates = self.create_button_frame(self.higher_number_of_widgets_in_frame(), new_text, new_command)
                        break
                    if new_text == "Task Scheduler":
                        self.task_scheduler = self.create_button_frame(self.higher_number_of_widgets_in_frame(), new_text, new_command)
                        break
                    if new_text == "Progress Tracker":
                        self.progress_tracker = self.create_button_frame(self.higher_number_of_widgets_in_frame(), new_text, new_command)
                        break
                    if new_text == "Flashcard":
                        self.flashcard = self.create_button_frame(self.higher_number_of_widgets_in_frame(), new_text, new_command)
                        break
                    if new_text == "Collaboration":
                        self.collaboration = self.create_button_frame(self.higher_number_of_widgets_in_frame(), new_text, new_command)
                        break
            else:
                messagebox.showerror("Error", "Function not defined")
                break


    def create_button_frame(self, parent, text, command):
        frame = ctk.CTkFrame(parent, fg_color=bg_color, border_width=10, border_color=second_main_bg_color, corner_radius=40)
        frame.pack(side="left", fill="both", expand=True, padx=10)
        button = ctk.CTkButton(frame, text=text, font=("Arial", 30), fg_color=bg_color, hover_color=hovering_color, corner_radius=100)
        button.pack(side="top", fill="both", expand=True, pady=20, padx=20)
        button.bind("<Button-1>", lambda event: command())
        return frame

    def notes_button_click(self):
        self.controller.app_frame.show_frame("NotebookFrame")

    def event_calender_click(self):
        self.controller.app_frame.show_frame("CalendarFrame")

    def templates_button_click(self):
        self.controller.app_frame.show_frame("TemplatesFrame")

    def task_scheduler_button_click(self):
        self.controller.app_frame.show_frame("TasksFrame")

    def progress_tracker_button_click(self):
        self.controller.app_frame.show_frame("ProgressFrame")

    def flashcard_button_click(self):
        self.controller.app_frame.show_frame("FlashcardsFrame")

    def collaboration_button_click(self):
        self.controller.app_frame.show_frame("CollaborationFrame")

    def edit_button_click(self):
        self.target_button_askstring = askstring("Edit Button", "Enter button you want to edit:")
        if self.target_button_askstring in self.button_labels:
            target_button = self.target_button_askstring
            for i in self.button_labels:
                if target_button == i:
                    self.button_labels.remove(i)
                    if target_button == "Note":
                        self.notes_frame.pack_forget()
                        self.notes_frame.destroy()
                        self.new_text(target_button)
                    elif target_button == "Event Calendar":
                        self.event_calendar_frame.pack_forget()
                        self.event_calendar_frame.destroy()
                        self.new_text(target_button)
                    elif target_button == "Template":
                        self.templates.pack_forget()
                        self.templates.destroy()
                        self.new_text(target_button)
                    elif target_button == "Task Scheduler":
                        self.task_scheduler.pack_forget()
                        self.task_scheduler.destroy()
                        self.new_text(target_button)
                    elif target_button == "Progress Tracker":
                        self.progress_tracker.pack_forget()
                        self.progress_tracker.destroy()
                        self.new_text(target_button)
                    elif target_button == "Flashcard":
                        self.flashcard.pack_forget()
                        self.flashcard.destroy()
                        self.new_text(target_button)
                    elif target_button == "Collaboration":
                        self.collaboration.pack_forget()
                        self.collaboration.destroy()
                        self.new_text(target_button)
        else:
            messagebox.showerror("Error", "Button not found")

    def new_text(self, target_button):
        while True:
            text = askstring("Edit Button", "Enter new button label:")
            if text in self.all_buttons_labels:
                new_text = text
                new_command = self.choose_new_command(new_text)
                self.button_labels.append(new_text)
                if new_command:
                    if new_text == "Note":
                        self.notes_frame = self.create_button_frame(self.higher_number_of_widgets_in_frame(), new_text, new_command)
                        break

                    if new_text == "Event Calendar":
                        self.event_calendar_frame = self.create_button_frame(self.higher_number_of_widgets_in_frame(), new_text, new_command)
                        break

                    if new_text == "Template":
                        self.templates = self.create_button_frame(self.higher_number_of_widgets_in_frame(), new_text, new_command)
                        break

                    if new_text == "Task Scheduler":
                        self.task_scheduler = self.create_button_frame(self.higher_number_of_widgets_in_frame(), new_text, new_command)
                        break

                    if new_text == "Progress Tracker":
                        self.progress_tracker = self.create_button_frame(self.higher_number_of_widgets_in_frame(), new_text, new_command)
                        break

                    if new_text == "Flashcard":
                        self.flashcard = self.create_button_frame(self.higher_number_of_widgets_in_frame(), new_text, new_command)
                        break

                    if new_text == "Collaboration":
                        self.collaboration = self.create_button_frame(self.higher_number_of_widgets_in_frame(), new_text, new_command)
                        break
            else:
                messagebox.showerror("Error", "Function not defined")
                break
    def higher_number_of_widgets_in_frame(self):
        if len(self.frame_top.winfo_children()) >= len(self.frame_bottom.winfo_children()):
            return self.frame_bottom
        else:
            return self.frame_top


    def choose_new_command(self, target_button):
        commands = {
            "note": self.notes_button_click,
            "calendar": self.event_calender_click,
            "template": self.templates_button_click,
            "task scheduler": self.task_scheduler_button_click,
            "progress tracker": self.progress_tracker_button_click,
            "flashcard": self.flashcard_button_click,
            "collaboration": self.collaboration_button_click,
        }
        return commands.get(target_button.lower(), lambda: print(f"{target_button} function not defined"))


