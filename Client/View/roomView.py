from tkinter import ttk
import tkinter as tk
import re

import customtkinter as ctk
import numpy as np


class RoomView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.room_frame = ctk.CTkFrame(self, width=500, height=500)
        self.room_frame.pack( pady=40, padx=40, fill='both')
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
        
        self.lobby_button = ctk.CTkButton(self.room_frame, text='Go to lobby', command=self.lobby_button_clicked ,height=40, width=300)
        self.lobby_button.grid(column=0, row=0, pady=(10,10))
        
        self.change_state = ctk.CTkButton(self.room_frame, text='Change State' ,height=40, width=300)
        self.change_state.grid(column=1, row=0, pady=(10,10))

        '''
            Treeview will represent interactive lobby. 
            You can join room simply by double clicking on record
        '''
        self.room_treeview = ttk.Treeview(self.room_frame, columns=("","Player", "Ready"), padding=25)
        self.room_treeview.heading("#1", text="Index", anchor="center")
        self.room_treeview.heading("Player", text="Player", anchor="center", command= lambda i =0: self.sort_by("username"))
        self.room_treeview.heading("Ready", text="Ready", anchor="center", command= lambda i =1: self.sort_by("ready"))
        self.room_treeview.column("#0", width=0, anchor="center")
        self.room_treeview.column("#1", width=180, anchor="center")
        self.room_treeview.column("Player", width=250, anchor="center")
        self.room_treeview.column("Ready", width=250, anchor="center")
        self.room_treeview.grid(column=0, row=1, columnspan=4)


    def set_controller(self, controller):
        self.controller = controller
        
    def owner_view(self, is_owner):
        if is_owner:
            self.owner_button = ctk.CTkButton(self.room_frame, text='Start game', command=self.start_game ,height=40, width=300)
            self.owner_button.grid(column=1, row=0, pady=(10,10))
    
    def start_game(self):
        self.controller.start_game()

    def sort_by(self, value):
        self.controller.sort_by(value)
    
    def lobby_button_clicked(self):
        self.controller.join_lobby()

    def draw_room(self, lst):
        for player_index, item in  enumerate(lst):
            values = (item['username'], item['ready'])
            self.room_treeview.insert("", "end", values=(player_index+1, )+values)

    def show_error(self, message):
       return
   
    def remove_room(self):
        for row in self.room_treeview.get_children():
            self.room_treeview.delete(row)
        
    def delete(self):
        self.pack_forget()
        self.grid_forget()
        self.room_frame = None

    