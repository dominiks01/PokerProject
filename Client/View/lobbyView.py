from tkinter import ttk
import tkinter as tk
import re

import customtkinter as ctk
import numpy as np


class LobbyView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.controller = None
        self.clicked = None

        self.lobby_frame = ctk.CTkFrame(self, fg_color="black")
        self.lobby_frame.pack(expand=True, pady=40, padx=40, fill='both')

        style = ttk.Style()
        style.configure("Treeview",
                        background="#333333",
                        foreground="White",
                        fieldbackground="#2b2b2b",
                        borderwidth=0.1)

        style.configure("Treeview.Heading",
                        background="#333333",
                        foreground="White",
                        fieldbackground="#2b2b2b",
                        borderwidth=0.1,
                        font=(12))

        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        style.theme_use('default')
        style.map('Treeview', background=[('selected', "#333333"), ('active', "#333333")])

        self.lobby_treeview = ttk.Treeview(self.lobby_frame, columns=("", "Author", "Description", "Players"), padding=25)
        self.lobby_treeview.heading("#1", text="Lobby ID", anchor="center", command= lambda i =0: self.sort_by(i))
        self.lobby_treeview.heading("Author", text="Author", anchor="center", command=lambda i =1: self.sort_by(i))
        self.lobby_treeview.heading("Description", text="Description", anchor="center", command=lambda i =2: self.sort_by(i))
        self.lobby_treeview.heading("Players", text="Players", anchor="center", command=lambda i =3: self.sort_by(i))
        self.lobby_treeview.column("#0", width=0, anchor="center")
        self.lobby_treeview.column("#1", width=100, anchor="center")
        self.lobby_treeview.column("Author", width=200, anchor="center")
        self.lobby_treeview.column("Description", width=250, anchor="center")
        self.lobby_treeview.column("Players", width=250, anchor="center")
        self.lobby_treeview.bind("<Double-1>", self.join_lobby_)

    def set_controller(self, controller):
        self.controller = controller

    def draw_lobby(self):
        for lobby_id, item in enumerate(self.controller.get_lobbies()):
            self.lobby_treeview.insert("", "end", values=item, tags=(item[0]))

        self.lobby_treeview.pack(expand=True, fill="both")

    def show_error(self, message):
       return
    
    def sort_by(self, value):
        self.controller.sort_by(value)

    def join_lobby_(self, event):
        item = self.lobby_treeview.identify("region", event.x, event.y)

        if item != "cell":
            return

        item = self.lobby_treeview.selection()[0]        
        lobby_index = self.lobby_treeview.item(item, "tags")[0]

        self.controller.join_lobby(lobby_index)
    
    def delete(self):
        self.pack_forget()
        self.grid_forget()
        self.lobby_frame = None

    