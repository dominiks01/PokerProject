from tkinter import ttk
import tkinter as tk
import customtkinter as ctk


class LoginView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None

        # Create new frame for register details
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(expand=True, pady=40, padx=40, fill='both')

        # header
        self.label = ctk.CTkLabel(self.login_frame, text='Login', font=('Times New Roman', 20, "bold"))
        self.label.grid(row=0, column=1, pady=15, padx=25)

        # Username entry
        self.username_var = tk.StringVar()
        self.username_entry = ctk.CTkEntry(self.login_frame, font=('Courier New', 15),
                                           width=250, placeholder_text="Username")
        self.username_entry.grid(row=1, column=1, sticky=tk.NSEW, padx=25, pady=10, ipady=5)

        # password entry
        self.password_var = tk.StringVar()
        self.password_entry = ctk.CTkEntry(self.login_frame, font=('Courier New', 15),
                                           width=250, placeholder_text="Password", show="*")
        self.password_entry.grid(row=3, column=1, sticky=tk.NSEW, padx=25, pady=10, ipady=5)

        # register button
        self.signup_button = ctk.CTkButton(self.login_frame, text='Signup', command=self.login_button_clicked,
                                           height=40)
        self.signup_button.grid(row=7, column=1, columnspan=2, sticky=tk.NSEW, padx=25, pady=10)

        # register button
        self.login_button = ctk.CTkLabel(self.login_frame, text='Do not have an account? Register', height=40)
        self.login_button.grid(row=8, column=1, columnspan=2, sticky=tk.NSEW, padx=25, pady=0)
        self.login_button.bind("<Button-1>", lambda e: self.register_button_clicked())

        # message
        self.message_label = ctk.CTkLabel(self.login_frame, text='')
        self.message_label.grid(row=9, column=1, columnspan=1, sticky=tk.W + tk.E)
        self.message_label.configure(anchor="center")

    def set_controller(self, controller):
        self.controller = controller

    def show_error(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)

    def register_button_clicked(self):
        if self.controller:
            self.controller.register()

    def login_button_clicked(self):
        if self.controller:
            self.controller.login(self.username_entry.get(), self.password_entry.get())

    def show_success(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000, self.hide_message)

    def hide_message(self):
        self.message_label['text'] = ''

    def delete(self):
        self.pack_forget()
        self.grid_forget()