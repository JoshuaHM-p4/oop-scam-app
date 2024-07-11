import customtkinter as ctk
from .templates_model import TemplateModel, HomeworkModel, MathModel, LetterModel, EssayModel
import sys, os
from PIL import Image
from CTkListbox import *
import datetime
# import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # frontend/
from config import APP_NAME, BACKGROUND_COLOR

class TemplatesFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
               
        
    def setup_ui(self):
        # Load images
        self.homework_img = ctk.CTkImage(Image.open("assets/images/homework.png"), size=(100, 100))
        self.letter_img = ctk.CTkImage(Image.open("assets/images/letter.png"), size=(100, 100))
        self.essay_img = ctk.CTkImage(Image.open("assets/images/essay.png"), size=(100, 100))
        self.math_img = ctk.CTkImage(Image.open("assets/images/math.png"), size=(100, 100))
        self.back_img = ctk.CTkImage(Image.open("assets/images/back_arrow.png"), size=(30, 30))
        
        self.top_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        
        self.homework_button = ctk.CTkButton(self.top_frame, fg_color="#1C3662", text="Homework", 
                                             corner_radius=20, image=self.homework_img, compound="top",
                                             command=lambda: self.show_frame("HomeworkFrame"))
        
        self.letter_button = ctk.CTkButton(self.top_frame, fg_color="#2B3742", text="Letter", 
                                           corner_radius=20, image=self.letter_img, compound="top",
                                           command=lambda: self.show_frame("LetterFrame"))
        
        self.bottom_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        
        self.essay_button = ctk.CTkButton(self.bottom_frame, fg_color="#2B3742", text="Essay", 
                                          corner_radius=20, image=self.essay_img, compound="top",
                                          command=lambda: self.show_frame("EssayFrame"))
        
        self.math_button = ctk.CTkButton(self.bottom_frame, fg_color="#1C3662", text="Math", 
                                         corner_radius=20, image=self.math_img, compound="top",
                                         command=lambda: self.show_frame("MathFrame"))
        
        self.horizontal_line = ctk.CTkCanvas(self, height=5, bg='#222B36', highlightthickness=0)
        
        self.vertical_line = ctk.CTkCanvas(self, width=5, bg='#222B36', highlightthickness=0)
        self.pack_and_place_widgets()
        
    def pack_and_place_widgets(self):
        # Packing top frame and its buttons
        self.top_frame.pack(side="top", fill="both", expand=True, padx=20, pady=(20,0))
        self.homework_button.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        self.letter_button.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # Packing bottom frame and its buttons
        self.bottom_frame.pack(side="top", fill="both", expand=True, padx=20, pady=(0,20))
        self.essay_button.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        self.math_button.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # Placing horizontal and vertical lines
        self.horizontal_line.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.9)
        self.vertical_line.place(relx=0.5, rely=0.5, anchor='center', relheight=0.9)
        
    def pack_forget_frames(self):
        for widget in self.winfo_children():
            widget.pack_forget()
            widget.place_forget()
    
    def pack_first_page(self):
        self.pack_forget_frames()
        self.pack_and_place_widgets()
    
    def show_frame(self, frame_name):
        self.pack_forget_frames()
        
        if frame_name == "HomeworkFrame":
            name = "Homework Template"
        elif frame_name == "LetterFrame":
            name = "Letter Template"
        elif frame_name == "EssayFrame":
            name = "Essay Template"
        elif frame_name == "MathFrame":
            name = "Math Template"
            
        self.header_frame = TemplateHeaderFrame(self, name)
        self.header_frame.pack(side="top", fill="x", padx=10, pady=(10, 0))
        
        if frame_name == "HomeworkFrame":
            self.homework_frame = HomeworkFrame(self)
            self.homework_frame.pack(side="top", fill="both", expand=True, pady=10, padx=10)
        elif frame_name == "LetterFrame":
            self.letter_frame = LetterFrame(self)
            self.letter_frame.pack(side="top", fill="both", expand=True, pady=10, padx=10)
        elif frame_name == "EssayFrame":
            self.essay_frame = EssayFrame(self)
            self.essay_frame.pack(side="top", fill="both", expand=True, pady=10, padx=10)
        elif frame_name == "MathFrame":
            self.math_frame = MathFrame(self)
            self.math_frame.pack(side="top", fill="both", expand=True, pady=10, padx=10)
            
class TemplateHeaderFrame(ctk.CTkFrame):
    def __init__(self, master, frame_name, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.frame_name = frame_name
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.setup_header_questions()
        
    def header_questions(self):
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        
        self.subject_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Subject:", width=150)
        self.title_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Title:", width=150)
        
        self.frame1 = ctk.CTkFrame(self.header_frame, fg_color=BACKGROUND_COLOR)
        
        self.name_entry = ctk.CTkEntry(self.frame1, placeholder_text="Name", width=150)
        self.name_entry.pack(side="left")
        
        self.date_entry = ctk.CTkEntry(self.frame1, placeholder_text="Date", width=150)
        self.date_entry.insert(0, current_date)
        self.date_entry.pack(side="right")
        
        self.frame2 = ctk.CTkFrame(self.header_frame, fg_color=BACKGROUND_COLOR)
        
        self.professor_entry = ctk.CTkEntry(self.frame2, placeholder_text="Professor", width=150)
        self.professor_entry.pack(side="left")
        
        self.school_entry = ctk.CTkEntry(self.frame2, placeholder_text="School(Optional):", width=150)
        self.school_entry.pack(side="right")
        self.section_entry = ctk.CTkEntry(self.frame2, placeholder_text="Section(Optional)", width=150)
        self.section_entry.pack(side="right")
        self.instructions_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Instructions(Optional):", width=150)
       
    def setup_header_questions(self):
        self.home_work_title = ctk.CTkLabel(self, text=self.frame_name, fg_color=BACKGROUND_COLOR, font=("Arial", 20, "bold"), height=30)
        self.home_work_title.pack(pady=10, fill="x", padx=10)
        
        self.button = ctk.CTkButton(self.home_work_title, text="", fg_color=BACKGROUND_COLOR, corner_radius=20, command=self.master.pack_first_page,
                                         image=self.master.back_img, height=30, width=30)
        self.button.place(anchor="nw", relheight=1, relwidth=0.1)
        
        self.check_var = ctk.StringVar(value="off")
        
        
        self.header_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, corner_radius=20, border_width=1)
        self.header_frame.pack(fill="x", padx=10, pady=10)
        self.header_questions()
        
        
        self.checkbox = ctk.CTkCheckBox(self.header_frame, text="Apply header?", variable=self.check_var, onvalue="on", offvalue="off",
                                           command=self.pack_header_questions)
        
        self.checkbox.pack(padx=5, pady=10)
        
    def pack_header_questions(self):
        if self.check_var.get() == "on":
            self.subject_entry.pack(side="top", padx=20, anchor="w", pady=10)
            self.title_entry.pack(side="top", padx=20, anchor="w", pady=10)
            self.frame1.pack(side="top", fill="x", padx=20)
            self.frame2.pack(side="top", fill="x", padx=20)
            self.instructions_entry.pack(side="top", padx=20, anchor="w", pady=10)
        else:
            self.subject_entry.pack_forget()
            self.title_entry.pack_forget()
            self.frame1.pack_forget()
            self.frame2.pack_forget()
            self.instructions_entry.pack_forget()
    
            
class HomeworkFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.header = self.master.header_frame
        
        self.questions = []  # List to store questions
        self.setup_ui()
        


    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        
        # Entry for question input
        self.question_entry = ctk.CTkEntry(self, placeholder_text="Type your question here", corner_radius=10, border_width=1)
        self.question_entry.pack(pady=5, fill="x", padx=10)
        
        # Button to add question
        self.add_question_btn = ctk.CTkButton(self, text="Add Question", command=self.add_question)
        self.add_question_btn.pack(pady=5)
        
        self.remove_icon = ctk.CTkImage(Image.open("assets/images/trash.png"), size=(20, 20))
        
        # Listbox to display questions
        self.questions_listbox = CTkListbox(self, corner_radius=10, border_width=1, command=self.toggle_remove_button, multiple_selection=True)
        self.questions_listbox.pack(fill="both", expand=True, pady=5, padx=10)
        
        self.lower_frame_buttons = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        self.lower_frame_buttons.pack(fill="both", pady=5, padx=10)
        
        self.save_homework_btn = ctk.CTkButton(self.lower_frame_buttons, text="Save Homework", command= self.save_homework, 
                                               corner_radius=10, state="disabled")
        self.save_homework_btn.pack(side="left", pady=5, padx=5,expand=True, anchor='e')
        
        self.remove_question_btn = ctk.CTkButton(self.lower_frame_buttons, text="Remove Question", command=self.remove_question,
                                                 image=self.remove_icon, compound="left",corner_radius=10, state="disabled")
        self.remove_question_btn.pack(side="right", pady=5, anchor='w', expand=True, padx=5)
        
        self.questions_listbox.bind('<<ListboxSelect>>', self.toggle_remove_button)
        
    def toggle_remove_button(self, event=None):
        selected_indices = self.questions_listbox.curselection()
        if selected_indices:  # If there's at least one item selected
            self.remove_question_btn.configure(state="normal")
        else:
            self.remove_question_btn.configure(state="disabled")
        
    def remove_question(self):
        selected_indices = self.questions_listbox.curselection()
        selected_indices = list(selected_indices)
        print(selected_indices)
        for i in reversed(selected_indices):  # Iterate in reverse order
            print(i)
            self.questions_listbox.delete(i)
            self.questions.pop(i)
        self.remove_question_btn.configure(state="disabled")
        if self.questions_listbox.size() == 0:
            self.save_homework_btn.configure(state="disabled")
        
    def add_question(self):
        question = self.question_entry.get()
        if question:  # Check if the question is not empty
            self.questions.append(question)  # Add question to the list
            self.questions_listbox.insert(ctk.END, question)  # Display question in the listbox
            self.question_entry.delete(0, ctk.END)  # Clear the entry widget
            self.save_homework_btn.configure(state="normal")
            
    def save_homework(self):
        name: str = self.header.name_entry.get()
        title: str = self.header.title_entry.get()
        subject: str = self.header.subject_entry.get()
        professor: str = self.header.professor_entry.get()
        instructions: str = self.header.instructions_entry.get()  # optional
        section: str = self.header.section_entry.get()  # optional
        school: str = self.header.school_entry.get()  # optional
        date: str = self.header.date_entry.get()  # auto    

        questions: list[str] = self.questions
        
        homework_template = HomeworkModel(
            name = name, 
            title = title,
            date = date,
            subject = subject,
            professor = professor,  
            questions = questions,
            section = section, 
            school = school, 
        )
        homework_template.add_instructions(instructions)
        
        try:
            if questions:
                file_path = asksaveasfile(defaultextension=".docx", filetypes=[("Word Documents", "*.docx")]).name
                if file_path:
                    homework_template.create_file(file_path)
                    if self.header.check_var.get() == "on": 
                        homework_template.write_header(file_path)
                    homework_template.write_questions(file_path)
                    self.questions = []
                    self.questions_listbox.delete(0, ctk.END)
                    messagebox.showinfo("Save Success", f"The file was saved successfully")
                    if self.questions_listbox.size() == 0:
                        self.save_homework_btn.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Save Error", f"The file was not saved")       
        
class LetterFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.header = self.master.header_frame
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.setup_ui()
    
    def setup_ui(self):
        # self.letter = LetterModel()
        
        self.frame_container = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, corner_radius=20, border_width=1)
        self.recipient_entry = ctk.CTkEntry(self.frame_container, placeholder_text="Recipient's Name", height=30)
        self.address_entry = ctk.CTkEntry(self.frame_container, placeholder_text="Address", height=30)
        self.save_button = ctk.CTkButton(self, text="Save Letter", fg_color="black", height=30, corner_radius=20, command= self.save_letter)
        
        self.pack_letter()
        
    def pack_letter(self):
        self.frame_container.pack(pady=10, padx=10, fill="both", expand=True)
        self.recipient_entry.pack(padx=10, expand=True, anchor="s", pady=10)
        self.address_entry.pack(padx=10, expand=True, anchor="n", pady=10)
        self.save_button.pack( padx=10)
    
    def save_letter(self):
        name: str = self.header.name_entry.get()
        title: str = self.header.title_entry.get()
        subject: str = self.header.subject_entry.get()
        professor: str = self.header.professor_entry.get()
        instructions: str = self.header.instructions_entry.get()  # optional
        section: str = self.header.section_entry.get()  # optional
        school: str = self.header.school_entry.get()  # optional
        date: str = self.header.date_entry.get()  # auto
        recepient: str = self.recipient_entry.get()
        address: str = self.address_entry.get()
        
        letter_template = LetterModel(
            name = name,
            title = title,
            subject = subject,
            professor = professor,
            section = section,
            school = school,
            date = date,
            recipient = recepient,
            address = address
        )
        
        letter_template.add_instructions(instructions)
        
        try:
            file_path = asksaveasfile(defaultextension=".docx", filetypes=[("Word Documents", "*.docx")]).name
            if file_path:
                letter_template.create_file(file_path)
                if self.header.check_var.get() == "on": 
                    letter_template.write_header(file_path)
                letter_template.write_letter(file_path)
                messagebox.showinfo("Save Success", f"The file was saved successfully")
        except Exception as e:
            messagebox.showerror("Save Error", f"The file was not saved")
        
        
class EssayFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.header = self.master.header_frame
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.setup_ui()
    
    def setup_ui(self):
        
        self.frame_container = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, corner_radius=20, border_width=1)
        self.essay_topic_entry = ctk.CTkEntry(self.frame_container, placeholder_text="Essay Topic", height=30)
        self.save_button = ctk.CTkButton(self, text="Save Essay", fg_color="black", height=30, corner_radius=20, command= self.save_essay)
        self.pack_essay()
        
    def pack_essay(self):
        self.frame_container.pack(pady=10, padx=10, fill="both", expand=True)
        self.essay_topic_entry.pack(expand=True)
        self.save_button.pack(padx=10)
    
    def save_essay(self):
        name: str = self.header.name_entry.get()
        title: str = self.header.title_entry.get()
        subject: str = self.header.subject_entry.get()
        professor: str = self.header.professor_entry.get()
        instructions: str = self.header.instructions_entry.get()  # optional
        section: str = self.header.section_entry.get()  # optional
        school: str = self.header.school_entry.get()  # optional
        date: str = self.header.date_entry.get()  # auto
        essay: str = self.essay_topic_entry.get()
        
        
        essay_template = EssayModel(
            name = name,
            title = title,
            subject = subject,
            professor = professor,
            section = section,
            school = school,
            date = date,
            essay = essay
        )
        
        essay_template.add_instructions(instructions)
        
        try:
            file_path = asksaveasfile(defaultextension=".docx", filetypes=[("Word Documents", "*.docx")]).name
            if file_path:
                essay_template.create_file(file_path)
                if self.header.check_var.get() == "on": 
                    essay_template.write_header(file_path)
                essay_template.write_essay(file_path)
                messagebox.showinfo("Save Success", f"The file was saved successfully")
        except Exception as e:
            messagebox.showerror("Save Error", f"The file was not saved")
        
        
        
        
        
class MathFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.header = self.master.header_frame
        self.math_questions = []
        self.setup_ui()
    
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        
        # Entry for question input
        self.question_entry = ctk.CTkEntry(self, placeholder_text="Type your math question here", corner_radius=10, border_width=1)
        self.question_entry.pack(pady=5, fill="x", padx=10)
        
        # Button to add question
        self.add_question_btn = ctk.CTkButton(self, text="Add Question", command=self.add_question)
        self.add_question_btn.pack(pady=5)
        
        self.remove_icon = ctk.CTkImage(Image.open("assets/images/trash.png"), size=(20, 20))
        
        # Listbox to display questions
        self.questions_listbox = CTkListbox(self, corner_radius=10, border_width=1, command=self.toggle_remove_button, multiple_selection=True)
        self.questions_listbox.pack(fill="both", expand=True, pady=5, padx=10)
        
        self.lower_frame_buttons = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        self.lower_frame_buttons.pack(fill="both", pady=5, padx=10)
        
        self.save_homework_btn = ctk.CTkButton(self.lower_frame_buttons, text="Save Homework", command= self.save_math, 
                                               corner_radius=10)
        self.save_homework_btn.pack(side="left", pady=5, padx=5,expand=True, anchor='e')
        
        self.remove_question_btn = ctk.CTkButton(self.lower_frame_buttons, text="Remove Question", command=self.remove_question,
                                                 image=self.remove_icon, compound="left",corner_radius=10, state="disabled")
        self.remove_question_btn.pack(side="right", pady=5, anchor='w', expand=True, padx=5)
        
        self.questions_listbox.bind('<<ListboxSelect>>', self.toggle_remove_button)
        
    def toggle_remove_button(self, event=None):
        selected_indices = self.questions_listbox.curselection()
        if selected_indices:  # If there's at least one item selected
            self.remove_question_btn.configure(state="normal")
        else:
            self.remove_question_btn.configure(state="disabled")
        
    def remove_question(self):
        selected_indices = self.questions_listbox.curselection()
        selected_indices = list(selected_indices)
        print(selected_indices)
        for i in reversed(selected_indices):  # Iterate in reverse order
            print(i)
            self.questions_listbox.delete(i)
            self.questions.pop(i)
        self.remove_question_btn.configure(state="disabled")
        if self.questions_listbox.size() == 0:
            self.save_homework_btn.configure(state="disabled")
        

    def add_question(self):
        math_question = self.question_entry.get()
        if math_question:  # Check if the question is not empty
            self.math_questions.append(math_question)  # Add question to the list
            self.questions_listbox.insert(ctk.END, math_question)  # Display question in the listbox
            self.question_entry.delete(0, ctk.END)  # Clear the entry widget
            
    def save_math(self):
        name: str = self.header.name_entry.get()
        title: str = self.header.title_entry.get()
        subject: str = self.header.subject_entry.get()
        professor: str = self.header.professor_entry.get()
        instructions: str = self.header.instructions_entry.get()  # optional
        section: str = self.header.section_entry.get()  # optional
        school: str = self.header.school_entry.get()  # optional
        date: str = self.header.date_entry.get()  # auto    

        math_questions: list[str] = self.math_questions
        
        math_template = MathModel(
            name = name, 
            title = title,
            date = date,
            subject = subject,
            professor = professor,  
            problems = math_questions,
            section = section, 
            school = school, 
            
        )
        math_template.add_instructions(instructions)
        
        try:
            if math_questions:
                file_path = asksaveasfile(defaultextension=".docx", filetypes=[("Word Documents", "*.docx")]).name
                if file_path:
                    math_template.create_file(file_path)
                    if self.header.check_var.get() == "on": 
                        math_template.write_header(file_path)
                    math_template.write_problems(file_path)
                    self.math_questions = []
                    self.questions_listbox.delete(0, ctk.END)
                    messagebox.showinfo("Save Success", f"The file was saved successfully")
                    if self.questions_listbox.size() == 0:
                        self.save_homework_btn.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Save Error", f"The file was not saved") 


