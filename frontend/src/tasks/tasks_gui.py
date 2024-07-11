import customtkinter as ctk
from PIL import Image
from tkinter import StringVar  # Import StringVar from tkinter
from .tasks_model import TasksModel

class TasksFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.filter_window = None
        self.new_task_window = None

        self.setup_ui()

    def setup_ui(self):
        # top frame
        self.top_frame = ctk.CTkFrame(self, fg_color='#141A1F')
        self.top_frame.pack(side='top', fill='x', padx=20, pady=20)

        # Open filter image
        self.filter_icon = ctk.CTkImage(Image.open("assets/images/filter_icon.png"), size=(25, 25))

        # Filter button
        self.filter_button = ctk.CTkButton(self.top_frame, text='+ Filter', hover_color='gray', width=80, height=30,
                                           font=('Montserrat', 30), corner_radius=10, image=self.filter_icon,
                                           text_color='black', fg_color='white', command=self.show_filter_window)
        self.filter_button.pack(side='left')

        # Add new icon
        self.add_new_icon = ctk.CTkImage(Image.open("assets/images/arrow_down.png"), size=(25, 25))

        # New task button
        self.new_task_button = ctk.CTkButton(self.top_frame, text='New', hover_color='navy blue', width=80, height=30,
                                             font=('Montserrat', 30), corner_radius=10, image=self.add_new_icon,
                                             text_color='white', fg_color='#2B5EB2', command=self.show_new_task_window)
        self.new_task_button.pack(side='right')

        # task bg
        self.tasks_frame = ctk.CTkFrame(self, fg_color='#222B36')
        self.tasks_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # no task frame
        self.no_tasks_frame = ctk.CTkFrame(self.tasks_frame, fg_color='#222B36')
        self.no_tasks_frame.pack(anchor='center', expand=True)

        # no tasks icon
        self.no_tasks_icon = ctk.CTkImage(Image.open("assets/images/no_task_icon.png"), size=(150, 150))

        # no tasks
        self.no_tasks = ctk.CTkLabel(self.no_tasks_frame, image=self.no_tasks_icon, text='')
        self.no_tasks.pack(padx=20, pady=(20, 10))

        # no task label
        self.no_tasks_label = ctk.CTkLabel(self.no_tasks_frame, text='Tasks are displayed here.', text_color='white',
                                           font=('Montserrat', 15))
        self.no_tasks_label.pack(padx=20, pady=(10, 20))

    def show_filter_window(self):
        if not self.filter_window or not self.filter_window.winfo_exists():
            self.filter_window = ctk.CTkToplevel(self)
            self.filter_window.title("Filter Options")
            self.filter_window.geometry("1000x275")
            self.filter_window.configure(fg_color='#141A1F', bg='#141A1F')
            self.filter_window.resizable(False, False)

            # Create variables to store selected options
            name_var = StringVar()
            date_var = StringVar()
            status_var = StringVar()
            type_var = StringVar()
            priority_var = StringVar()

            # Create a main frame for filter options
            main_frame = ctk.CTkFrame(self.filter_window, fg_color='#141A1F')
            main_frame.pack(fill='both', expand=True, padx=10, pady=10)

            # Categories and their options
            categories = {
                "Name": ["A-Z", "Z-A"],
                "Date": ["Closest to deadline first", "Farthest to deadline first"],
                "Status": ["Completed", "In Progress", "Not Started"],
                "Type": ["Tasks", "Review", "Assignment", "Exam"],
                "Priority": ["Low", "Mid", "High"]
            }

            # Create frames to organize the layout
            name_frame = ctk.CTkFrame(main_frame, fg_color='#222B36')
            name_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)

            date_frame = ctk.CTkFrame(main_frame, fg_color='#222B36')
            date_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)

            status_frame = ctk.CTkFrame(main_frame, fg_color='#222B36')
            status_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)

            type_frame = ctk.CTkFrame(main_frame, fg_color='#222B36')
            type_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)

            priority_frame = ctk.CTkFrame(main_frame, fg_color='#222B36')
            priority_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)

            frames = {
                "Name": name_frame,
                "Date": date_frame,
                "Status": status_frame,
                "Type": type_frame,
                "Priority": priority_frame
            }

            for category, options in categories.items():
                category_frame = frames.get(category, None)
                if category_frame:
                    category_label = ctk.CTkLabel(category_frame, text=category, text_color='white',
                                                  font=('Montserrat', 15))
                    category_label.pack(anchor='w', padx=10, pady=10)

                    for option in options:
                        radio_button = ctk.CTkRadioButton(category_frame, text=option, text_color='white',
                                                          font=('Montserrat', 12), value=option)
                        radio_button.pack(anchor='w', padx=10, pady=10)

            # Apply button
            apply_button = ctk.CTkButton(main_frame, text="Apply",
                                         command=lambda: self.apply_filter(name_var.get(), date_var.get(),
                                                                           status_var.get(),
                                                                           type_var.get(), priority_var.get()))
            apply_button.pack(pady=20, padx=20, fill='both', expand=True)

        else:
            self.filter_window.lift()

    def show_new_task_window(self):
        if not self.new_task_window or not self.new_task_window.winfo_exists():
            self.new_task_window = ctk.CTkToplevel(self)
            self.new_task_window.title("New Task")
            self.new_task_window.geometry("600x400")
            self.new_task_window.configure(fg_color='#141A1F', bg='#141A1F')

            # Create variables to store task details
            task_name_var = StringVar()
            deadline_var = StringVar()
            status_var = StringVar()
            type_var = StringVar()
            priority_var = StringVar()

            # Create a main frame for new task options
            main_frame = ctk.CTkFrame(self.new_task_window, fg_color='#141A1F')
            main_frame.pack(fill='both', expand=True, padx=10, pady=10)

            # Task name entry
            task_name_label = ctk.CTkLabel(main_frame, text="Task Name:", text_color='white', font=('Montserrat', 15))
            task_name_label.pack(anchor='w', padx=10, pady=10)
            task_name_entry = ctk.CTkEntry(main_frame, textvariable=task_name_var, width=50)
            task_name_entry.pack(anchor='w', padx=10, pady=10)

            # Deadline entry
            deadline_label = ctk.CTkLabel(main_frame, text="Deadline:", text_color='white', font=('Montserrat', 15))
            deadline_label.pack(anchor='w', padx=10, pady=10)
            deadline_entry = ctk.CTkEntry(main_frame, textvariable=deadline_var, width=50)
            deadline_entry.pack(anchor='w', padx=10, pady=10)

            # Status options
            status_label = ctk.CTkLabel(main_frame, text="Status:", text_color='white', font=('Montserrat', 15))
            status_label.pack(anchor='w', padx=10, pady=10)
            status_options = ["Completed", "In Progress", "Not Started"]
            for option in status_options:
                radio_button = ctk.CTkRadioButton(main_frame, text=option, text_color='white',
                                                  font=('Montserrat', 12), value=option, variable=status_var)
                radio_button.pack(anchor='w', padx=10, pady=5)

            # Type options
            type_label = ctk.CTkLabel(main_frame, text="Type:", text_color='white', font=('Montserrat', 15))
            type_label.pack(anchor='w', padx=10, pady=10)
            type_options = ["Tasks", "Review", "Assignment", "Exam"]
            for option in type_options:
                radio_button = ctk.CTkRadioButton(main_frame, text=option, text_color='white',
                                                  font=('Montserrat', 12), value=option, variable=type_var)
                radio_button.pack(anchor='w', padx=10, pady=5)

            # Priority options
            priority_label = ctk.CTkLabel(main_frame, text="Priority:", text_color='white', font=('Montserrat', 15))
            priority_label.pack(anchor='w', padx=10, pady=10)
            priority_options = ["Low", "Mid", "High"]
            for option in priority_options:
                radio_button = ctk.CTkRadioButton(main_frame, text=option, text_color='white',
                                                  font=('Montserrat', 12), value=option, variable=priority_var)
                radio_button.pack(anchor='w', padx=10, pady=5)

            # Save button
            save_button = ctk.CTkButton(main_frame, text="Save", command=lambda: self.save_new_task(task_name_var.get(),
                                                                                                  deadline_var.get(),
                                                                                                  status_var.get(),
                                                                                                  type_var.get(),
                                                                                                  priority_var.get()))
            save_button.pack(pady=20, padx=20, fill='both', expand=True)

        else:
            self.new_task_window.lift()


    def apply_filter(self, name, date, status, type, priority):
        print(f"Filter applied: Name-{name}, Date-{date}, Status-{status}, Type-{type}, Priority-{priority}")
        # Apply the filter logic here


    def save_new_task(self, name, deadline, status, type, priority):
        print(f"New Task saved: Name-{name}, Deadline-{deadline}, Status-{status}, Type-{type}, Priority-{priority}")
        # Add your logic to save the new task here
