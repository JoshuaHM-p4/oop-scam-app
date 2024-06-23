import tkinter as tk

class LoginFrame(tk.Frame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback

        label = tk.Label(self, text="Login Page")
        label.pack(pady=10, padx=10)

        # Example widgets (entry, button) for login
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack()
        self.login_button.bind("<Return>", self.login)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def login(self):
        # Implement login logic here
        print(f"Logging in {self.username_entry.get()}...")

        test_data = {"user_id": "1", "username": "JoshuaHM", "access_token": "123456789", "email": "joshuahm.2004@gmail.com"}
        self.callback(test_data)
