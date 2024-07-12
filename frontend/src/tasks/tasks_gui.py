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
        self.tasks_list = []
        self.task_deadline = []
        self.task_status = []
        self.task_type = []
        self.task_priority = []

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
        
        self.tasks_frame = ctk.CTkFrame(self, fg_color='#222B36')
        self.tasks_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
            
        self.load_tasks()

        # Load tasks
    def load_tasks(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        if self.tasks_list:
            upper_frame = ctk.CTkFrame(self.tasks_frame, fg_color='#141A1F', height=50)

            name_label = ctk.CTkLabel(upper_frame, text="Aa Name")
            date_label = ctk.CTkLabel(upper_frame, text="📅Date")
            status_label = ctk.CTkLabel(upper_frame, text="↻Status")
            type_label = ctk.CTkLabel(upper_frame, text="▼Type")
            priority_label = ctk.CTkLabel(upper_frame, text="▼Priority")
            done_label = ctk.CTkLabel(upper_frame, text="✓Done")

            lower_frame = ctk.CTkScrollableFrame(self.tasks_frame, fg_color='#222B36', corner_radius=10)
            for task in range(len(self.tasks_list)):
                format_frame = ctk.CTkFrame(lower_frame, fg_color='#141A1F', corner_radius=0)
                task_name = ctk.CTkLabel(format_frame, text=self.tasks_list[task])
                task_deadline = ctk.CTkLabel(format_frame, text=self.task_deadline[task])
                task_status = ctk.CTkOptionMenu(format_frame, values=["Not Started", "Completed", "In Progress"])
                task_type = ctk.CTkLabel(format_frame, text=self.task_type[task])
                task_priority = ctk.CTkLabel(format_frame, text=self.task_priority[task])
                task_check = ctk.CTkCheckBox(format_frame, text="", corner_radius=20, checkbox_height=15, checkbox_width=15)

                format_frame.pack(fill='x', expand=True, side='top',pady=1)
                task_name.pack(side="left", fill='x', expand=True, pady=5, padx=5)
                task_deadline.pack(side="left", fill='x', expand=True, pady=5, padx=5)
                task_status.pack(side="left", fill='x', expand=True, pady=5, padx=5)
                task_type.pack(side="left", fill='x', expand=True, pady=5, padx=5)
                task_priority.pack(side="left", fill='x', expand=True, pady=5, padx=5)
                task_check.pack(side="right", fill='x', expand=True, pady=5, padx=5)

                self.task_name_var.set("")
                self.deadline_var.set("")
                self.status_var.set("")
                self.type_var.set("")
                self.priority_var.set("")

            upper_frame.pack(fill='x', padx=30, pady=(10,0), side='top')
                
            name_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)
            date_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)
            status_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)
            type_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)
            priority_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)
            done_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)
                
            lower_frame.pack(fill='both', expand=True, padx=20, pady=(0,10), side='top')

        else:
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
            self.filter_window.geometry(f"1000x350+{self.tasks_frame.winfo_rootx()}+{self.tasks_frame.winfo_rooty()}")
            self.filter_window.configure(fg_color='#141A1F', bg='#141A1F')
            self.filter_window.resizable(False, False)
            self.filter_window.attributes('-topmost', 1)

            # Create variables to store selected options
            name_var = StringVar()
            date_var = StringVar()
            status_var = StringVar()
            type_var = StringVar()
            priority_var = StringVar()

            # Create a main frame for filter options
            main_frame = ctk.CTkFrame(self.filter_window, fg_color='#141A1F')
            main_frame.pack(fill='both', expand=True, padx=10, pady=(10,0))
            bottom_frame = ctk.CTkFrame(self.filter_window, fg_color='#141A1F')
            bottom_frame.pack(fill='both', expand=True, padx=10, pady=(10,10))

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
            apply_button = ctk.CTkButton(bottom_frame, text="Apply", fg_color='#222B36', 
                                         command=lambda: self.apply_filter(name_var.get(), date_var.get(),
                                                                           status_var.get(),
                                                                           type_var.get(), priority_var.get()))
            apply_button.pack(pady=(0,10), padx=10, fill='both', expand=True)

        else:
            self.filter_window.lift()

    def show_new_task_window(self):
        if not self.new_task_window or not self.new_task_window.winfo_exists():
            self.new_task_window = ctk.CTkToplevel(self)
            self.new_task_window.title("New Task")
            self.new_task_window.geometry(f"300x400+{self.winfo_width()-(self.new_task_window.winfo_width()//4)}+{self.tasks_frame.winfo_rooty()}")
            self.new_task_window.configure(fg_color='#141A1F', bg='#141A1F')
            self.new_task_window.attributes('-topmost', 1)

            # Create variables to store task details
            self.task_name_var = StringVar()
            self.deadline_var = StringVar()
            self.status_var = StringVar()
            self.type_var = StringVar()
            self.priority_var = StringVar()

            # Create a main frame for new task options
            main_frame = ctk.CTkScrollableFrame(self.new_task_window, fg_color='#141A1F')
            main_frame.pack(fill='both', expand=True, padx=10, pady=10)

            # Task name entry
            task_name_label = ctk.CTkLabel(main_frame, text="Task Name:", text_color='white', font=('Montserrat', 15))
            task_name_label.pack(anchor='w', padx=10, pady=10)
            task_name_entry = ctk.CTkEntry(main_frame, textvariable=self.task_name_var, width=250, placeholder_text="Title")
            task_name_entry.pack(anchor='w', padx=(10,23), pady=10)

            # Deadline entry
            deadline_label = ctk.CTkLabel(main_frame, text="Deadline:", text_color='white', font=('Montserrat', 15))
            deadline_label.pack(anchor='w', padx=10, pady=10)
            deadline_entry = ctk.CTkEntry(main_frame, textvariable=self.deadline_var, width=250, placeholder_text="Due Date")
            deadline_entry.pack(anchor='w', padx=(10,23), pady=10)

            # Status options
            status_label = ctk.CTkLabel(main_frame, text="Status:", text_color='white', font=('Montserrat', 15))
            status_label.pack(anchor='w', padx=10, pady=10)
            status_options = ["Completed", "In Progress", "Not Started"]
            for option in status_options:
                radio_button = ctk.CTkRadioButton(main_frame, text=option, text_color='white',
                                                  font=('Montserrat', 12), value=option, variable=self.status_var)
                radio_button.pack(anchor='w', padx=10, pady=5)

            # Type options
            type_label = ctk.CTkLabel(main_frame, text="Type:", text_color='white', font=('Montserrat', 15))
            type_label.pack(anchor='w', padx=10, pady=10)
            type_options = ["Tasks", "Review", "Assignment", "Exam"]
            for option in type_options:
                radio_button = ctk.CTkRadioButton(main_frame, text=option, text_color='white',
                                                  font=('Montserrat', 12), value=option, variable=self.type_var)
                radio_button.pack(anchor='w', padx=10, pady=5)

            # Priority options
            priority_label = ctk.CTkLabel(main_frame, text="Priority:", text_color='white', font=('Montserrat', 15))
            priority_label.pack(anchor='w', padx=10, pady=10)
            priority_options = ["Low", "Mid", "High"]
            for option in priority_options:
                radio_button = ctk.CTkRadioButton(main_frame, text=option, text_color='white',
                                                  font=('Montserrat', 12), value=option, variable=self.priority_var)
                radio_button.pack(anchor='w', padx=10, pady=5)

            # Save button
            save_button = ctk.CTkButton(main_frame, text="Save", fg_color='#222B36', command=lambda: self.save_new_task(self.task_name_var.get(),
                                                                                                  self.deadline_var.get(),
                                                                                                  self.status_var.get(),
                                                                                                  self.type_var.get(),
                                                                                                  self.priority_var.get()))
            save_button.pack(pady=(20,10), padx=(10,23), fill='both', expand=True)

        else:
            self.new_task_window.lift()


    def apply_filter(self, name, date, status, type, priority):
        print(f"Filter applied: Name-{name}, Date-{date}, Status-{status}, Type-{type}, Priority-{priority}")
        # Apply the filter logic here


    def save_new_task(self, name, deadline, status, type, priority):
        print(f"New Task saved: Name-{name}, Deadline-{deadline}, Status-{status}, Type-{type}, Priority-{priority}")
        # Add your logic to save the new task here
        if name:
            self.tasks_list.append(name)
            self.task_deadline.append(deadline)
            self.task_status.append(status)
            self.task_type.append(type)
            self.task_priority.append(priority)
            self.load_tasks()
