import customtkinter as ctk
from tkinter import messagebox, simpledialog
from .progress_model import ProgressModel

back_ground_color = "#222B36"
first_color = "#141a1f"
font_color_1 = "#515f73"

class ProgressFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.username = "username" # ito yung nakalagay sa Hi username
        self.goal_name = "How Long Can My Goal Be?" # ito yung ididisplay for the goal
        self.due_date = "01/01/0001" # due date na nakadisplay
        self.steps_completed = 0 # steps completed na display
        self.goal_description = ""
        self.purpose_text = ""
        self.value = 0
        
        self.controller = controller
        
        self.main_frame = ctk.CTkFrame(self, fg_color=first_color)
        self.main_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.top_frame = ctk.CTkFrame(self.main_frame, fg_color=first_color)
        self.top_frame.pack(side="top", fill="x")   

        # username label and goal label
        self.top_left_frame = ctk.CTkFrame(self.top_frame, fg_color=first_color)
        self.top_left_frame.pack(side="left", padx=(10,0), pady=10)
        self.top_left_frame.configure(width=700, height=120)
        
        self.username_label = ctk.CTkLabel(self.top_left_frame, text=f"Hi {self.username}! Let's continue your", text_color=font_color_1, font=('arial', 20))
        self.username_label.pack(anchor="w")
        
        # note: gawa ng pang limit sa goal name length
        self.goalname_label = ctk.CTkLabel(self.top_left_frame, text=self.goal_name, text_color="white", font=('arial',35))
        self.goalname_label.pack(anchor="w")
        
        # set goal button, completed steps label, and due date label
        self.top_right_frame = ctk.CTkFrame(self.top_frame, fg_color=first_color)
        self.top_right_frame.pack(side="right", fill="x", padx=10, pady=10)
        self.top_right_frame.configure(height=120)

        self.top_right_goal_due_display = ctk.CTkLabel(self.top_right_frame, text=f"Due Date: {self.due_date}", fg_color=back_ground_color, corner_radius=100)
        self.top_right_goal_due_display.pack(side="right", padx=(10,0))
        self.top_right_goal_due_display.configure(height=30)
        
        self.top_right_completed_steps_display = ctk.CTkLabel(self.top_right_frame, text=f"Steps Completed: {self.steps_completed}", fg_color=back_ground_color, corner_radius=100)
        self.top_right_completed_steps_display.pack(side="right", padx=(10,0))
        self.top_right_completed_steps_display.configure(height=30)
        
        # set new goal button
        self.top_right_new_goal_button = ctk.CTkButton(self.top_right_frame, text="New Goal", fg_color=back_ground_color, corner_radius=100, command=self.set_new_goal)
        self.top_right_new_goal_button.pack(side="right", pady=10)
        self.top_right_new_goal_button.configure(width=100, height=30)
        
        self.middle_frame = ctk.CTkFrame(self.main_frame, fg_color=back_ground_color)
        self.middle_frame.pack(side="top", fill="x", padx=10, pady=10)
        
        # goal description label
        self.middle_left_frame = ctk.CTkFrame(self.middle_frame, fg_color=back_ground_color)
        self.middle_left_frame.pack(side="left", fill="x", expand=True, padx=(5,10))
        
        goal_description_label = ctk.CTkLabel(self.middle_left_frame, fg_color=back_ground_color, text="Goal Description", text_color="white", font=('arial',25))
        goal_description_label.pack(anchor="w", pady=(15,10), padx=(10,0))
        
        # description text
        self.description_textbox = ctk.CTkTextbox(self.middle_left_frame, height=65, fg_color=back_ground_color, activate_scrollbars=False)
        self.description_textbox.pack(side="left", anchor="w", pady=(0,10), padx=(5,0), fill="x", expand=True)
        self.description_textbox.insert("end", self.goal_description)
        self.description_textbox.configure(state="disabled")
        
        # purpose label
        self.middle_right_frame = ctk.CTkFrame(self.middle_frame, fg_color=back_ground_color)
        self.middle_right_frame.pack(side="left", fill="x",expand=True, padx=(10,5))
        self.middle_right_frame.configure(height=100)      
        
        purpose_label = ctk.CTkLabel(self.middle_right_frame, fg_color=back_ground_color, text="Why I Started", text_color="white", font=('arial',25))
        purpose_label.pack(anchor="w", pady=(15,10), padx=(10,0))
        
        # purpose text
        self.purpose_textbox = ctk.CTkTextbox(self.middle_right_frame, height=65, fg_color=back_ground_color, activate_scrollbars=False)
        self.purpose_textbox.pack(side="left", anchor="w", pady=(0,10), padx=(5,0), fill="x", expand=True)
        self.purpose_textbox.insert("end", self.purpose_text)
        self.purpose_textbox.configure(state="disabled")
        
        self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color=first_color)
        self.bottom_frame.pack(side="top", fill="both", expand=True)
        
        # steps progress bar
        self.bottom_inner_frame = ctk.CTkFrame(self.bottom_frame, fg_color=back_ground_color)
        self.bottom_inner_frame.pack(fill="both", expand=True, padx=10, pady=(10,10))
        
        self.progressbar_frame = ctk.CTkFrame(self.bottom_inner_frame, fg_color=back_ground_color)
        self.progressbar_frame.pack(fill="x", side="top", padx=15, pady=(10,10))
        
        self.left_progressbar_frame = ctk.CTkFrame(self.progressbar_frame, fg_color=back_ground_color)
        self.left_progressbar_frame.pack(fill="x", side="left")
        
        self.steps_label = ctk.CTkLabel(self.left_progressbar_frame, text="Steps", text_color="white", font=('arial',25))
        self.steps_label.pack(anchor="w")
        
        # self.progressbar = ctk.CTkProgressBar(self.progressbar_frame, orientation="horizontal", mode="determinate", height=25, width=810)
        
        # steps checklist
        self.checklist_frame = ctk.CTkFrame(self.bottom_inner_frame, fg_color=back_ground_color)
        self.checklist_frame.pack(fill="both", padx=(15), pady=(0,10), expand=True)
        
        # add step button
        self.add_step_button = ctk.CTkButton(self.bottom_frame, text="+ Add Step", command=self.add_step, state="disabled")
        self.add_step_button.pack(side="left", padx=10, pady=(10,10))
        self.add_step_button.configure(height=30, width=100)
        
    def set_new_goal(self):
        
        goal, due_date, description, purpose, new_goal = None, None, None, None, None

        # Show the "New Goal" input dialog
        goal = ctk.CTkInputDialog(title="New Goal", text="Enter your new goal").get_input()

        # Show the "Due Date" input dialog if goal is provided
        if goal:
            due_date = ctk.CTkInputDialog(title="Due Date", text="Enter your due date").get_input()

        # Show the "Goal Description" input dialog if due date is provided
        if due_date:
            description = ctk.CTkInputDialog(title="Goal Description", text="Enter your goal description").get_input()

        # Show the "Purpose" input dialog if description is provided
        if description:
            purpose = ctk.CTkInputDialog(title="Purpose", text="Enter your purpose").get_input()

        # Show the final input dialog if purpose is provided
        if purpose:
            new_goal = ctk.CTkInputDialog(title="New Goal Confirmation", text="Confirm your new goal").get_input()

        # Configure GUI elements only if all inputs are provided
        if new_goal:
            self.goal_name = goal
            self.goalname_label.configure(text=self.goal_name)
            self.due_date = due_date
            self.top_right_goal_due_display.configure(text=f"Due Date: {self.due_date}")

            # Update goal description
            self.description_textbox.configure(state="normal")
            self.description_textbox.delete("1.0", "end")
            self.description_textbox.insert("end", description)
            self.description_textbox.configure(state="disabled")

            # Update purpose text
            self.purpose_textbox.configure(state="normal")
            self.purpose_textbox.delete("1.0", "end")
            self.purpose_textbox.insert("end", purpose)
            self.purpose_textbox.configure(state="disabled")

            
            # self.progressbar.configure(value=0)
            self.new_checklist()
        
    def new_checklist(self):
        self.checklist_new = ctk.CTkCheckBox(self.checklist_frame, fg_color=back_ground_color, corner_radius=10, text=self.goal_name, command=self.plus)
        self.checklist_new.pack(fill="both", pady=5, padx=5)
        self.add_step_button.configure(state="normal")
        
        
    def add_step(self):
        goal = ctk.CTkInputDialog(title="Add Step", text="Enter your step").get_input()
        if goal:
            self.checklist_new = ctk.CTkCheckBox(self.checklist_frame, fg_color=back_ground_color, corner_radius=10, text=goal, command=self.plus)
            self.checklist_new.pack(fill="both", pady=5, padx=5)
            self.steps_completed += 1
            self.top_right_completed_steps_display.configure(text=f"Steps Completed: {self.steps_completed}")
    
    def plus(self):
        self.steps_completed += 1
        self.top_right_completed_steps_display.configure(text=f"Steps Completed: {self.steps_completed}")