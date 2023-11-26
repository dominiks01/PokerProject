import tkinter as tk
import customtkinter as ctk

class CreateRoomView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None
        
        self.create_room_frame = ctk.CTkFrame(self,width=500,  height=500)
        self.create_room_frame.pack(expand=True,  pady=40, padx=25, fill='both')

        self.label = ctk.CTkLabel(
            self.create_room_frame, 
            text='Create New Room', 
            font=('Times New Roman', 20, "bold"))
        self.label.pack(padx=25, pady=(20, 0))
        
        self.lobby_name_input = ctk.CTkEntry(
            self.create_room_frame, 
            width=250, 
            font=('Courier New', 15),
            placeholder_text="Lobby Name")
        self.lobby_name_input.pack(padx=25, pady=(30, 20))

        self.big_blind_input = ctk.CTkEntry(
            self.create_room_frame, 
            width=250, 
            font=('Courier New', 15),
            placeholder_text="Big Blind Value")
        self.big_blind_input.pack(padx=25, pady=(0, 20))

        self.money_input = ctk.CTkEntry(
            self.create_room_frame, 
            width=250, 
            font=('Courier New', 15),
            placeholder_text="Starting Money")
        self.money_input.pack(padx=25, pady=(0, 20))

        self.max_players = ctk.CTkEntry(
            self.create_room_frame, 
            width=250, 
            font=('Courier New', 15),
            placeholder_text="Max Players")
        self.max_players.pack(padx=25, pady=(0, 10))

        self.create_room_button = ctk.CTkButton(
            self.create_room_frame,
            text="Create Lobby",
            command=self.create_room,
            height=40, width=50)
        
        self.cancel_button = ctk.CTkButton(
            self.create_room_frame, 
            text="Cancel", 
            command=self.cancel_button, 
            height=40, width=50)

        self.create_room_button.pack(side=ctk.LEFT, padx=(75, 25), pady=(10,10))
        self.cancel_button.pack(side=ctk.RIGHT, padx=(25, 75), pady=(10,10))
        
    def set_controller(self, controller):
        self.controller = controller
        
    def cancel_button(self):
        self.controller.cancel()
        
    def create_room(self):
        if self.controller:
            self.controller.create_room(
                self.lobby_name_input.get(),
                self.big_blind_input.get(),
                self.money_input.get(),
                self.max_players.get()
            )

    def delete(self):
        self.pack_forget()
        self.create_room_frame = None