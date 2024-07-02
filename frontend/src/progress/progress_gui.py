import customtkinter as ctk
from tkinter import messagebox, simpledialog
from .progress_model import ProgressModel


back_ground_color = "#222B36"
first_color = "#333333"
second_color = "#141a1f"

class ProgressFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.due_date = "06/19/25"

        self.main_frame = ctk.CTkFrame(self, fg_color = second_color)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.first_frame = ctk.CTkFrame(self.main_frame, fg_color = second_color, corner_radius = 100)
        self.first_frame.pack(side="top", fill="x", expand=False)

        self.first_frame_left = ctk.CTkFrame(self.first_frame, fg_color = second_color)
        self.first_frame_left.pack(side="left", fill="x", expand=True)

        self.label_display_username = ctk.CTkLabel(self.first_frame_left, text="Hi Username! Let's continue your", font=("Times New Roman", 15), anchor = "sw")
        self.label_display_username.pack(side="top", fill="x", pady=(10,0), padx=20)

        self.label_main = ctk.CTkLabel(self.first_frame_left, text="Get To Know Myself", font=("Times New Roman", 30), anchor = "nw")
        self.label_main.pack(side="top", fill="x", pady=(0,10), padx=20)

        self.first_frame_right = ctk.CTkFrame(self.first_frame, fg_color = second_color)
        self.first_frame_right.pack(side="right", fill="x", expand=True)

        self.first_frame_right_leftside = ctk.CTkFrame(self.first_frame_right, fg_color = back_ground_color, corner_radius=100)
        self.first_frame_right_leftside.pack(side="left", fill="x", expand=True, padx = (10))

        self.set_new_goal_button = ctk.CTkButton(self.first_frame_right_leftside, text="Set New Goal", font=("Arial", 20), command=self.set_new_goal, fg_color = back_ground_color)
        self.set_new_goal_button.pack(side="top", fill="x", pady=10, padx=20)

        self.first_frame_right_middle = ctk.CTkFrame(self.first_frame_right, fg_color = back_ground_color, corner_radius=100)
        self.first_frame_right_middle.pack(side="left", fill="x", expand=True, padx = (10))

        self.steps_completed_label = ctk.CTkLabel(self.first_frame_right_middle, text="Steps Completed:", font=("Arial", 20), anchor = "w")
        self.steps_completed_label.pack(side="left", fill="x", pady=10, padx=(20,0))
        self.steps_completed_steps_label = ctk.CTkLabel(self.first_frame_right_middle, text="3", font=("Arial", 20), anchor = "w")
        self.steps_completed_steps_label.pack(side="left", fill="x", pady=10, padx = (0, 20))

        self.first_frame_right_rightside = ctk.CTkFrame(self.first_frame_right, fg_color = back_ground_color, corner_radius=100)
        self.first_frame_right_rightside.pack(side="left", fill="x", expand=True, padx = (10, 20))

        self.goal_due_label = ctk.CTkLabel(self.first_frame_right_rightside, text="Goal Due:", font=("Arial", 20), anchor = "w")
        self.goal_due_label.pack(side="left", fill="none", pady=10, padx=(20,0))
        self.goal_due_date_label = ctk.CTkLabel(self.first_frame_right_rightside, text=self.due_date, font=("Arial", 20), anchor = "w")
        self.goal_due_date_label.pack(side="left", fill="none", pady=10, padx = (0, 20))

        self.second_frame = ctk.CTkFrame(self.main_frame, fg_color = back_ground_color, corner_radius = 40)
        self.second_frame.pack(side="top", fill="both", expand=True, pady = 20, padx = 20)

    def set_new_goal(self):
        self.count = 1
        self.check_var = 1
        messagebox.showinfo("Set New Goal", "Set New Goal Button Clicked")
        self.first_step = ctk.CTkInputDialog(title = "First Step", text = "Enter the First Step:")
        first_step = self.first_step.get_input()
        self.second_frame_step = ctk.CTkFrame(self.second_frame, fg_color = second_color, corner_radius = 40)
        self.second_frame_step.pack(side="top", fill="x", expand=True, pady = 20, padx = 20)

        self.check_var_step_one = ctk.IntVar(value=1)
        self.check_button_step = ctk.CTkCheckBox(self.second_frame_step, text=f"Step 1: {first_step}", font=("Arial", 20), onvalue = 1, offvalue = 0, command=self.check_box_event, variable = self.check_var_step_one, fg_color = "red", bg_color=back_ground_color)
        self.check_button_step.pack(side="top", fill="x", pady = 10, padx = 20)
        self.check_button_step.deselect()

        self.add_step_button = ctk.CTkButton(self.second_frame_step, text="Add Step", font=("Arial", 20), command=self.add_step, fg_color = back_ground_color)
        self.add_step_button.pack(side="top", fill="x", pady=10, padx=20)

    def add_step(self):
        messagebox.showinfo("Add Step", "Add Step Button Clicked")
        self.add_step_button.destroy()
        self.check_var += 1
        self.check_var_each = ctk.IntVar(value = self.check_var)
        self.steps = ctk.CTkInputDialog(title = f"Step {self.count + 1}", text = f"Enter Step {self.count + 1}:")
        steps = self.steps.get_input()
        self.check_button_step = ctk.CTkCheckBox(self.second_frame_step, text=f"Step {self.count + 1}: {steps}", font=("Arial", 20), onvalue = self.check_var + 1, offvalue = self.check_var + 0, command=self.check_box_event, variable=self.check_var_each, fg_color = "red", bg_color=back_ground_color)
        self.check_button_step.pack(side="top", fill="x", pady = 10, padx = 20)

        self.add_step_button = ctk.CTkButton(self.second_frame_step, text="Add Step", font=("Arial", 20), command=self.add_step, fg_color = back_ground_color)
        self.add_step_button.pack(side="top", fill="x", pady = 10, padx = 20)

        self.count += 1

    def check_box_event(self):
        if self.check_var_step_one.get() == 1:
            messagebox.showinfo("Check Box Event", "Check Box Event")
        else:
            pass