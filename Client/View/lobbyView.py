from tkinter import ttk
import tkinter as tk
import re

import customtkinter as ctk
import numpy as np


class LobbyView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.lobby_frame = ctk.CTkFrame(self, fg_color="black")
        self.lobby_frame.pack(expand=True, pady=40, padx=40, fill='both')
        self.controller = None
        self.clicked = None

        style = ttk.Style()
        style.configure("Treeview",
                        background="#333333",
                        foreground="White",
                        fieldbackground="#2b2b2b")

        style.configure("Treeview.Heading",
                        background="#333333",
                        foreground="White",
                        fieldbackground="#2b2b2b")

        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.lobby_treeview = ttk.Treeview(self.lobby_frame, columns=("", "Author", "Description", "Players"))
        self.lobby_treeview.heading("#1", text="Lobby ID", anchor="center")
        self.lobby_treeview.heading("Author", text="Author", anchor="center")
        self.lobby_treeview.heading("Description", text="Description", anchor="center")
        self.lobby_treeview.heading("Players", text="Players", anchor="center")
        self.lobby_treeview.column("#0", width=0, anchor="center")
        self.lobby_treeview.column("#1", width=100, anchor="center")
        self.lobby_treeview.column("Author", width=200, anchor="center")
        self.lobby_treeview.column("Description", width=250, anchor="center")
        self.lobby_treeview.column("Players", width=250, anchor="center")
        self.lobby_treeview.bind("<Double-1>", self.join_lobby)

    def set_controller(self, controller):
        self.controller = controller

    def draw_lobby(self, lst):
        for item in lst:
            self.lobby_treeview.insert("", "end", values=item)

        self.lobby_treeview.pack(expand=True, fill="both")

    def show_error(self, message):
       return
    
    def join_lobby(self):
        item = self.lobby_treeview.selection()[0]
        lobby_index = self.lobby_treeview.item(item, "tags")[0]

        self.controller.join_lobby(lobby_index)
    
    def delete(self):
        self.pack_forget()
        self.grid_forget()
        self.lobby_frame = None

    