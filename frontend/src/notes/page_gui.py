import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image
import sys
import os
import json
import requests
import socketio
import threading

# Append paths to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # frontend/

# Import necessary modules
from config import APP_NAME, BACKGROUND_COLOR, NOTES_ENDPOINT, API_BASE_URL

class NotebookPageFrame(ctk.CTkFrame):
    def __init__(self, master, index, notebook, *args, **kwargs):
        super().__init__(master,*args,**kwargs)
        self.master = master
        self.index = index
        self.notebook = notebook

        self.add_lock = threading.Lock()
        self.share_lock = threading.Lock()
        self.fetch_lock = threading.Lock()
        self.update_title_lock = threading.Lock()
        self.update_content_lock = threading.Lock()

        self.notebook_title = self.notebook.title
        self.content_dict = {}
        self.current_page = 1  # Start with page 1
        self.total_pages = 0
        self.create_widgets()

        # self.fetch_notes()
        # self.total_pages = len(self.content_dict)
        # print(self.content_dict)
        # self.master.join_room(f"note-{self.content_dict[self.current_page]['note_id']}")

        # self.update_content()
        # self.update_button_states()

    def create_widgets(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack(fill="both", expand=True, padx=2, pady=2)

        self.return_img = ctk.CTkImage(Image.open("assets/images/back_arrow.png"), size=(25, 25))
        self.add_img = ctk.CTkImage(Image.open("assets/images/plus.png"), size=(25, 25))
        self.save_img = ctk.CTkImage(Image.open("assets/images/save.png"), size=(25, 25))

        self.notebook_title = ctk.CTkEntry(self, fg_color=BACKGROUND_COLOR, height=1, font=("Arial", 20), placeholder_text="Title:", width=200)
        self.notebook_title.pack( padx=10, pady=10, anchor="center")
        self.notebook_title.insert(0, self.notebook.title)

        self.top_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        self.top_frame.pack(fill="x", pady=(10,0))

        self.back_button = ctk.CTkButton(self.top_frame, text="", command= self.master.back_to_notebooks,
                                         image=self.return_img, width=25, height=25, corner_radius=20,
                                         fg_color=BACKGROUND_COLOR, hover_color="#222B36", border_width=0)
        self.back_button.pack(side="left", padx=10, expand=True, anchor="w")

        # self.label_notebook_title = ctk.CTkLabel(self.top_frame, text="Notebook Page", font=("Arial", 20), fg_color="red")
        # self.label_notebook_title.pack(side="left", padx=10, pady=10, expand=True, anchor="center")

        self.right_frame = ctk.CTkFrame(self.top_frame, fg_color=BACKGROUND_COLOR)
        self.right_frame.pack(side="left", padx=10,  expand=True, anchor="e")

        self.share_img = ctk.CTkImage(Image.open("assets/images/share.png"), size=(25, 25))
        self.share_button = ctk.CTkButton(self.right_frame, text="", image=self.share_img,
                                            width=25, height=25, corner_radius=20,
                                            fg_color=BACKGROUND_COLOR, hover_color="#222B36", border_width=0,
                                            command=self.share_notebook)
        self.share_button.pack(side="left", anchor="e")

        self.add_page_button = ctk.CTkButton(self.right_frame, text="", command= self.add_page,
                                             image=self.add_img, width=25, height=25, corner_radius=20,
                                             fg_color=BACKGROUND_COLOR, hover_color="#222B36", border_width=0)
        self.add_page_button.pack(side="left", anchor="e")

        self.save_button = ctk.CTkButton(self.right_frame, text="", command= self.save_page,
                                         image=self.save_img, width=25, height=25, corner_radius=20,
                                         fg_color=BACKGROUND_COLOR, hover_color="#222B36", border_width=0)
        self.save_button.pack(side="left",  anchor="e")

        # Title textbox
        self.title_entry = ctk.CTkEntry(self, fg_color=BACKGROUND_COLOR, height=1, font=("Arial", 20), placeholder_text="Title:",
                                          border_width=0, corner_radius=0)
        self.title_entry.pack(fill="x", padx=10, pady=10)

        # self.title_entry.insert(0, self.content_dict[self.current_page]['title'])

        # Content textbox
        self.content_textbox = ctk.CTkTextbox(self, fg_color="white", height=1, text_color="black", border_width=0, corner_radius=0)
        self.content_textbox.pack(fill="both", expand=True, padx=10)
        # self.content_textbox.insert("0.0", "Some example text!\n" * 50)

        self.content_textbox.bind("<KeyRelease>", lambda event: self.master.send_note_update(self.content_textbox.get("1.0", "end-1c")))

        self.lower_frame = ctk.CTkFrame(self, height=20, fg_color=BACKGROUND_COLOR)
        self.lower_frame.pack(fill="x", padx=10, pady=10)

        self.previous_img_active = ctk.CTkImage(Image.open("assets/images/left_arrow.png"), size=(25, 25))
        self.next_img_active = ctk.CTkImage(Image.open("assets/images/right_arrow.png"), size=(25, 25))

        self.previous_img_disabled = ctk.CTkImage(Image.open("assets/images/left_arrow_disabled.png"), size=(25, 25))
        self.next_img_disabled = ctk.CTkImage(Image.open("assets/images/right_arrow_disabled.png"), size=(25, 25))


        self.left_button = ctk.CTkButton(self.lower_frame, text="",
                                         fg_color=BACKGROUND_COLOR,
                                         image=self.previous_img_disabled,
                                         width=25,
                                         height=25,
                                         command = self.previous_page,
                                        )
        self.left_button.pack(side="left", padx=10, expand=True)

        self.page_container = ctk.CTkFrame(self.lower_frame, fg_color=BACKGROUND_COLOR, corner_radius=20, border_width=1)
        self.page_container.pack(side="left", padx=10, expand=True)

        self.page_number = ctk.CTkLabel(self.page_container, text=f"Page {self.current_page} of {self.total_pages}", font=("Arial", 18), fg_color=BACKGROUND_COLOR)
        self.page_number.pack(fill="both", expand=True, padx=10, pady=5)

        self.page_number.bind("<Button-1>", lambda event: self.create_jump_to_page_popup())

        self.right_button = ctk.CTkButton(self.lower_frame, text="",
                                          fg_color=BACKGROUND_COLOR,
                                          image=self.next_img_active,
                                          width=25,
                                          height=25,
                                          command=self.next_page)
        self.right_button.pack(side="left", padx=10, expand=True)

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_content()
            self.update_button_states()
            self.master.join_room(f"note-{self.content_dict[self.current_page]['note_id']}")

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_content()
            self.update_button_states()
            self.master.join_room(f"note-{self.content_dict[self.current_page]['note_id']}")

    def update_button_states(self):
    # Enable or disable buttons based on the current page
        if self.current_page > 1:
            self.left_button.configure(state="normal", image=self.previous_img_active)
        else:
            self.left_button.configure(state="disabled", image=self.previous_img_disabled)

        if self.current_page < self.total_pages:
            self.right_button.configure(state="normal", image=self.next_img_active)
        else:
            self.right_button.configure(state="disabled", image=self.next_img_disabled)

            # Update the page number label
            self.page_number.configure(text=f"Page {self.current_page}")

    def update_content(self):
        # Fetch and display content for the current page
        note = self.content_dict[self.current_page]
        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, note['title'])
        self.content_textbox.delete("1.0", "end")
        self.content_textbox.insert("1.0", note['content'])
        # Update the page number label
        self.page_number.configure(text=f"Page {self.current_page} of {self.total_pages}")
        for item in self.content_dict:
            print(item, self.content_dict[item])

    def add_page(self):
        notebook_id = self.notebook.id
        response = requests.post(
            url=NOTES_ENDPOINT + f"/note/{notebook_id}",
            headers={"Authorization": f"Bearer {self.master.controller.access_token}"}
        )
        if response.status_code != 201:
            messagebox.showerror("Error", response.json()['message'])
            return
        note = response.json()['note']
        self.total_pages += 1
        self.content_dict[self.total_pages] = {'note_id': note['note_id'], 'content': note['content'], 'title': note['title']}
        self.current_page = self.total_pages
        self.update_content()
        self.update_button_states()
        self.master.join_room(f"note-{note['note_id']}")

    def create_jump_to_page_popup(self):
        dialog = ctk.CTkInputDialog(title="Jump to:", text="Enter the page number:")
        title = dialog.get_input()
        if title:
            self.jump_to_page(title)

    def share_notebook(self):
        dialog = ctk.CTkInputDialog(title="Share Notebook", text="Enter the email of the user you want to share the notebook with:")
        email = dialog.get_input()
        if email:
            response = requests.post(
                url=NOTES_ENDPOINT + f"/notebook/share/{self.notebook.id}",
                headers={"Authorization": f"Bearer {self.master.controller.access_token}"},
                json={"email": email}
            )
            if response.status_code != 200:
                messagebox.showerror("Error", response.json()['message'])
                return
            messagebox.showinfo("Success", f"Notebook shared with {email}")
            user_to_share_with_id = response.json()['user_id']
            # self.master.send_notebook_update({"notebook_id": self.notebook_id, "user_id": user_to_share_with_id})
            self.master.send_notebook_update({"notebook_id": self.notebook.id, "user_id": user_to_share_with_id})

    def jump_to_page(self, page_number_str):
        try:
            page_number = int(page_number_str)
            if 1 <= page_number <= self.total_pages:
                self.current_page = page_number
                self.update_content()  # Assuming this method updates the content for the current page
                self.update_button_states()  # Update the state of navigation buttons
                self.master.join_room(f"note-{self.content_dict[self.current_page]['note_id']}")
            else:
                messagebox.showerror("Error", "Page number out of range.")
        except ValueError:
            messagebox.showerror("Error", "Invalid page number.")

    def save_page(self):
        if self.notebook_title.get() != self.notebook.title:
            self.update_notebook_title()
        note_id = self.content_dict[self.current_page]['note_id']
        if self.title_entry.get() != self.content_dict[self.current_page]['title'] or self.content_textbox.get("1.0", "end-1c") != self.content_dict[self.current_page]['content']:
            response = requests.put(
                url=NOTES_ENDPOINT + f"/note/{note_id}",
                headers={"Authorization": f"Bearer {self.master.controller.access_token}"},
                json={
                    "title": self.title_entry.get(),
                    "content": self.content_textbox.get("1.0", "end-1c")
                }
            )
            if response.status_code != 200:
                messagebox.showerror("Error", response.json()['message'])
                return
            messagebox.showinfo("Save", "Note saved successfully.")
            self.content_dict[self.current_page]['title'] = self.title_entry.get()
            self.content_dict[self.current_page]['content'] = self.content_textbox.get("1.0", "end-1c")

    def update_notebook_title(self):
        print('update_notebook_title')
        notebook_id = self.notebook.id
        response = requests.put(
            url=NOTES_ENDPOINT + f"/notebook-title/{notebook_id}",
            headers={"Authorization": f"Bearer {self.master.controller.access_token}"},
            json={"title": self.notebook_title.get()}
        )
        if response.status_code != 200:
            messagebox.showerror("Error", response.json()['message'])
            return
        self.notebook.title = self.notebook_title.get()
        self.master.notebooks[self.index].title = self.notebook_title.get()
        messagebox.showinfo("Success", "Notebook title updated successfully")

    def fetch_notes(self):

        def fetch_request():
            if not self.fetch_lock.acquire(blocking=False):
                print("Fetch request already in progress.")
                return

            lock_acquired = True
            try:
                notebook_id = self.notebook.id
                response = requests.get(
                    url=NOTES_ENDPOINT + f"/notes/{notebook_id}",
                    headers={"Authorization": f"Bearer {self.master.controller.access_token}"},
                    timeout=10
                )
                if response.status_code != 200:
                    messagebox.showerror("Error", response.json()['message'])
                    return

                page_number = 1
                for note in response.json():
                    self.content_dict[page_number] = note # {'content': note['content'], 'title': note['title']}
                    page_number += 1

                self.total_pages = len(self.content_dict)
                self.after(0, self.master.join_room, f"note-{self.content_dict[self.current_page]['note_id']}")
                self.after(0, self.update_content)
                self.after(0, self.update_button_states)

            except ConnectionError as e:
                messagebox.showerror("Error", "Failed to connect to the server.")
            finally:
                if lock_acquired:
                    self.fetch_lock.release()

        threading.Thread(target=fetch_request).start()


# self.fetch_notes()
# self.total_pages = len(self.content_dict)
# print(self.content_dict)
# self.master.join_room(f"note-{self.content_dict[self.current_page]['note_id']}")

# self.setup_ui()
# self.update_content()
# self.update_button_states()