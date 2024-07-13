from tkinter import StringVar
import customtkinter as ctk
from PIL import Image
from tkcalendar import DateEntry
from datetime import datetime
from .tasks_model import TasksModel


class TasksFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # self.filter_window = None
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
        # self.filter_icon = ctk.CTkImage(Image.open("assets/images/filter_icon.png"), size=(25, 25))

        # # Filter button
        # self.filter_button = ctk.CTkButton(self.top_frame, text='+ Filter', hover_color='gray', width=80, height=30,
        #                                    font=('Montserrat', 30), corner_radius=10, image=self.filter_icon,
        #                                    text_color='black', fg_color='white', command=self.show_filter_window)
        # self.filter_button.pack(side='left')

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

    def load_tasks(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        if self.tasks_list:
            # Upper frame for header labels
            upper_frame = ctk.CTkFrame(self.tasks_frame, fg_color='#141A1F', height=50)
            name_label = ctk.CTkLabel(upper_frame, text="Name")
            deadline_label = ctk.CTkLabel(upper_frame, text="Deadline")
            status_label = ctk.CTkLabel(upper_frame, text="Status")
            type_label = ctk.CTkLabel(upper_frame, text="Type")
            priority_label = ctk.CTkLabel(upper_frame, text="Priority")
            done_label = ctk.CTkLabel(upper_frame, text="Done")

            upper_frame.pack(fill='x', padx=30, pady=(10, 0), side='top')
            name_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)
            deadline_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)
            status_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)
            type_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)
            priority_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)
            done_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)

            # Lower frame for task entries
            lower_frame = ctk.CTkScrollableFrame(self.tasks_frame, fg_color='#222B36', corner_radius=10)
            lower_frame.pack(fill='both', expand=True, padx=20, pady=(0, 10), side='top')

            for i in range(len(self.tasks_list)):
                format_frame = ctk.CTkFrame(lower_frame, fg_color='#141A1F', corner_radius=0)

                # Widget frames to hold each widget
                widget_frame_name = ctk.CTkFrame(format_frame, fg_color='#141A1F', corner_radius=0, width=50)
                widget_frame_deadline = ctk.CTkFrame(format_frame, fg_color='#141A1F', corner_radius=0, width=50)
                widget_frame_status = ctk.CTkFrame(format_frame, fg_color='#141A1F', corner_radius=0, width=50)
                widget_frame_type = ctk.CTkFrame(format_frame, fg_color='#141A1F', corner_radius=0, width=50)
                widget_frame_priority = ctk.CTkFrame(format_frame, fg_color='#141A1F', corner_radius=0, width=50)
                widget_frame_check = ctk.CTkFrame(format_frame, fg_color='#141A1F', corner_radius=0, width=50)

                task_name = ctk.CTkLabel(widget_frame_name, text=self.tasks_list[i], justify='left')
                task_deadline = ctk.CTkLabel(widget_frame_deadline, text=self.task_deadline[i])

                # Create a StringVar for task status
                task_status_var = StringVar(value=self.task_status[i])
                task_status = ctk.CTkOptionMenu(widget_frame_status, variable=task_status_var,
                                                values=["Not Started", "Completed", "In Progress"], width=20,
                                                command=lambda value, var=task_status_var: self.update_status_color(var,
                                                                                                                    task_status))
                task_status.set(self.task_status[i])

                task_type = ctk.CTkLabel(widget_frame_type, text=self.task_type[i])
                task_priority = ctk.CTkLabel(widget_frame_priority, text=self.task_priority[i])

                # Create a checkbox for deleting the task
                task_check = ctk.CTkCheckBox(widget_frame_check, text="", corner_radius=20, checkbox_height=15,
                                             checkbox_width=15, command=lambda idx=i: self.delete_task(idx))

                widget_frame_name.pack(side="left", fill='x', expand=True, pady=5, padx=5)
                widget_frame_deadline.pack(side="left", fill='x', expand=True, pady=5, padx=5)
                widget_frame_status.pack(side="left", fill='x', expand=True, pady=5, padx=5)
                widget_frame_type.pack(side="left", fill='x', expand=True, pady=5, padx=5)
                widget_frame_priority.pack(side="left", fill='x', expand=True, pady=5, padx=5)
                widget_frame_check.pack(side="right", fill='x', expand=True, pady=5, padx=5, anchor='e')

                task_name.pack()
                task_deadline.pack()
                task_status.pack()
                task_type.pack()
                task_priority.pack()
                task_check.pack(anchor='e')

                format_frame.pack(fill='x', expand=True, side='top', pady=5)

                self.update_status_color(task_status_var, task_status)

        else:
            # Display no tasks message
            self.no_tasks_frame = ctk.CTkFrame(self.tasks_frame, fg_color='#222B36')
            self.no_tasks_frame.pack(anchor='center', expand=True)

            self.no_tasks_icon = ctk.CTkImage(Image.open("assets/images/no_task_icon.png"), size=(150, 150))
            self.no_tasks = ctk.CTkLabel(self.no_tasks_frame, image=self.no_tasks_icon, text='')
            self.no_tasks.pack(padx=20, pady=(20, 10))

            self.no_tasks_label = ctk.CTkLabel(self.no_tasks_frame, text='Tasks are displayed here.',
                                               text_color='white',
                                               font=('Montserrat', 15))
            self.no_tasks_label.pack(padx=20, pady=(10, 20))

    def update_status_color(self, var, widget):
        status = var.get()
        if status == "Completed":
            widget.configure(fg_color="#318555", button_color='#293340')
        elif status == "In Progress":
            widget.configure(fg_color="#315585", button_color='#293340')
        elif status == "Not Started":
            widget.configure(fg_color="#cc2742", button_color='#293340')

    def delete_task(self, idx):
        del self.tasks_list[idx]
        del self.task_deadline[idx]
        del self.task_status[idx]
        del self.task_type[idx]
        del self.task_priority[idx]
        self.load_tasks()

    # def show_filter_window(self):
    #     if not self.filter_window or not self.filter_window.winfo_exists():
    #         self.filter_window = ctk.CTkToplevel(self)
    #         self.filter_window.title("Filter Options")
    #         self.filter_window.geometry(f"1000x350+{self.tasks_frame.winfo_rootx()}+{self.tasks_frame.winfo_rooty()}")
    #         self.filter_window.configure(fg_color='#141A1F', bg='#141A1F')
    #         self.filter_window.resizable(False, False)
    #         self.filter_window.attributes('-topmost', 1)

    #         # Create variables to store selected options
    #         name_var = StringVar()
    #         date_var = StringVar()
    #         status_var = StringVar()
    #         type_var = StringVar()
    #         priority_var = StringVar()

    #         # Create a main frame for filter options
    #         main_frame = ctk.CTkFrame(self.filter_window, fg_color='#141A1F')
    #         main_frame.pack(fill='both', expand=True, padx=10, pady=(10,0))
    #         bottom_frame = ctk.CTkFrame(self.filter_window, fg_color='#141A1F')
    #         bottom_frame.pack(fill='both', expand=True, padx=10, pady=(10,10))

    #         # Categories and their options
    #         categories = {
    #             "Name": ["A-Z", "Z-A"],
    #             "Date": ["Closest to deadline first", "Farthest to deadline first"],
    #             "Status": ["Completed", "In Progress", "Not Started"],
    #             "Type": ["Tasks", "Review", "Assignment", "Exam"],
    #             "Priority": ["Low", "Mid", "High"]
    #         }

    #         # Create frames to organize the layout
    #         name_frame = ctk.CTkFrame(main_frame, fg_color='#222B36')
    #         name_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)

    #         date_frame = ctk.CTkFrame(main_frame, fg_color='#222B36')
    #         date_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)

    #         status_frame = ctk.CTkFrame(main_frame, fg_color='#222B36')
    #         status_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)

    #         type_frame = ctk.CTkFrame(main_frame, fg_color='#222B36')
    #         type_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)

    #         priority_frame = ctk.CTkFrame(main_frame, fg_color='#222B36')
    #         priority_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)

    #         frames = {
    #             "Name": name_frame,
    #             "Date": date_frame,
    #             "Status": status_frame,
    #             "Type": type_frame,
    #             "Priority": priority_frame
    #         }

    #         for category, options in categories.items():
    #             category_frame = frames.get(category, None)
    #             if category_frame:
    #                 category_label = ctk.CTkLabel(category_frame, text=category, text_color='white',
    #                                               font=('Montserrat', 15))
    #                 category_label.pack(anchor='w', padx=10, pady=10)

    #                 for option in options:
    #                     radio_button = ctk.CTkRadioButton(category_frame, text=option, text_color='white',
    #                                                       font=('Montserrat', 12), value=option)
    #                     radio_button.pack(anchor='w', padx=10, pady=10)

    #         # Apply button
    #         apply_button = ctk.CTkButton(bottom_frame, text="Apply", fg_color='#222B36',
    #                                      command=lambda: self.apply_filter(name_var.get(), date_var.get(),
    #                                                                        status_var.get(),
    #                                                                        type_var.get(), priority_var.get()))
    #         apply_button.pack(pady=(0,10), padx=10, fill='both', expand=True)

    #     else:
    #         self.filter_window.lift()

    def show_new_task_window(self):
        if not self.new_task_window or not self.new_task_window.winfo_exists():
            self.new_task_window = ctk.CTkToplevel(self)
            self.new_task_window.title("New Task")

            new_task_button_right_x = self.new_task_button.winfo_rootx() + self.new_task_button.winfo_width()
            new_task_window_width = 650
            new_task_button_bottom_y = self.new_task_button.winfo_rooty() + self.new_task_button.winfo_height() + 10

            new_task_window_pos_x = new_task_button_right_x - new_task_window_width

            new_task_window_pos_y = new_task_button_bottom_y

            self.new_task_window.geometry(
                f"{new_task_window_width}x350+{new_task_window_pos_x}+{new_task_window_pos_y}")
            self.new_task_window.configure(fg_color='#141A1F', bg='#141A1F')
            self.new_task_window.resizable(False, False)
            self.new_task_window.attributes('-topmost', 5)

            # Create variables to store task details
            task_name_var = StringVar()
            deadline_date_var = StringVar()
            deadline_time_var = StringVar()
            status_var = StringVar()
            type_var = StringVar()
            priority_var = StringVar()

            # Create a main frame for new task options
            main_frame = ctk.CTkFrame(self.new_task_window, fg_color='#141A1F')
            main_frame.pack(fill='both', expand=True, padx=10, pady=10)

            # Task name entry
            task_name_label = ctk.CTkLabel(main_frame, text="Name:", text_color='white', font=('Montserrat', 15))
            task_name_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
            task_name_entry = ctk.CTkEntry(main_frame, textvariable=task_name_var, width=150, fg_color='white',
                                           bg_color='#141A1F', text_color='black')
            task_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

            # Deadline date entry
            deadline_date_label = ctk.CTkLabel(main_frame, text="Date:", text_color='white', font=('Montserrat', 15))
            deadline_date_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')
            deadline_date_entry = DateEntry(main_frame, textvariable=deadline_date_var, width=17, background='dark blue',
                                            fg_color='white', borderwidth=2)
            deadline_date_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

            # Deadline time entry
            deadline_time_label = ctk.CTkLabel(main_frame, text="Time:", text_color='white', font=('Montserrat', 15))
            deadline_time_label.grid(row=1, column=2, padx=20, pady=10, sticky='w')
            deadline_time_entry = ctk.CTkEntry(main_frame, textvariable=deadline_time_var, width=150, fg_color='white',
                                               bg_color='#141A1F', text_color='black')
            deadline_time_entry.grid(row=1, column=3, padx=15, pady=10, sticky='w')

            # Status options
            status_label = ctk.CTkLabel(main_frame, text="Status:", text_color='white', font=('Montserrat', 15))
            status_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')
            status_options = ["Completed", "In Progress", "Not Started"]
            for i, option in enumerate(status_options):
                radio_button = ctk.CTkRadioButton(main_frame, text=option, text_color='white',
                                                  font=('Montserrat', 12), value=option, variable=status_var)
                radio_button.grid(row=3 + i, column=0, padx=20, pady=5, sticky='w')

            # Type options
            type_label = ctk.CTkLabel(main_frame, text="Type:", text_color='white', font=('Montserrat', 15))
            type_label.grid(row=2, column=1, padx=20, pady=10, sticky='w')
            type_options = ["Tasks", "Review", "Assignment", "Exam"]
            for i, option in enumerate(type_options):
                radio_button = ctk.CTkRadioButton(main_frame, text=option, text_color='white',
                                                  font=('Montserrat', 12), value=option, variable=type_var)
                radio_button.grid(row=3 + i, column=1, padx=20, pady=5, sticky='w')

            # Priority options
            priority_label = ctk.CTkLabel(main_frame, text="Priority:", text_color='white', font=('Montserrat', 15))
            priority_label.grid(row=2, column=2, padx=20, pady=10, sticky='w')
            priority_options = ["Low", "Mid", "High"]
            for i, option in enumerate(priority_options):
                radio_button = ctk.CTkRadioButton(main_frame, text=option, text_color='white',
                                                  font=('Montserrat', 12), value=option, variable=priority_var)
                radio_button.grid(row=3 + i, column=2, padx=20, pady=5, sticky='w')

            # Save button
            save_button = ctk.CTkButton(main_frame, text="Save", command=lambda: self.save_new_task(
                task_name_var.get(),
                deadline_date_var.get(),
                deadline_time_var.get(),
                status_var.get(),
                type_var.get(),
                priority_var.get()))
            save_button.grid(row=8, column=0, columnspan=8, pady=(20, 10), padx=15, sticky='we')


        else:
            self.new_task_window.lift()

    def apply_filter(self, name, date, status, type, priority):
        print(f"Filter applied: Name-{name}, Date-{date}, Status-{status}, Type-{type}, Priority-{priority}")
        # Implement filter logic here

    def save_new_task(self, name, deadline_date, deadline_time, status, type, priority):
        deadline_str = f"{deadline_date} - {deadline_time}"

        print(
            f"New Task saved: Name-{name}, Deadline-{deadline_str}, Status-{status}, Type-{type}, Priority-{priority}")

        # Add your logic to save the new task here
        if name:
            self.tasks_list.append(name)
            self.task_deadline.append(deadline_str)
            self.task_status.append(status)
            self.task_type.append(type)
            self.task_priority.append(priority)
            self.load_tasks()
