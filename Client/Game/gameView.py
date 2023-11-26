URL = "http://127.0.0.1:5000"
import pathlib
import tkinter as tk
import pygubu
import os
from PIL import Image, ImageTk
import customtkinter as ctk

PROJECT_PATH = pathlib.Path(__file__).parent.parent
PROJECT_UI_6 = os.path.join(PROJECT_PATH, "UI/game_window.ui")
CARDS_SOURCE = os.path.join(PROJECT_PATH, "Resources/cards")
IMAGES_SOURCE = os.path.join(PROJECT_PATH, "Resources/images")

class GameView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None
        self.game_frame = pygubu.Builder()
        self.game_frame.add_resource_path(PROJECT_PATH)
        self.game_frame.add_from_file(PROJECT_UI_6)

        self.main_window = self.game_frame.get_object('game_window', None)
        self.game_frame.connect_callbacks(self)
        
        self.shifted_players = None
        self.seats = None
        
        self.stakes_data = None
        self.pot_value = 0
        self.nick = {}
        self.shift = None
        self.raise_value = None
        self.all_cards = None

        self.player_nick = {}
        
        self.players_labels = {}
        self.board_labels = {}
        self.buttons = {}
        self.stakes = {}
        self.notes = {}
        self.act = {}
        self.pot = None
        self.raise_bet_slider = None
        # self.root.protocol("WM_DELETE_WINDOW", self.on_quit_button_click)
        
        for i in range(6):
            self.players_labels["table0" + str(i) + "card01"] = self.game_frame.get_object("table0" + str(i) + "card01", None)
            self.players_labels["table0" + str(i) + "card02"] = self.game_frame.get_object("table0" + str(i) + "card02", None)
            self.stakes[i] = self.game_frame.get_object("table0" + str(i) + "stake", None)
            self.notes[i] = self.game_frame.get_object("table0" + str(i) + "note", None)
            self.act[i] = self.game_frame.get_object("table0" + str(i) + "act", None)

        for i in range(5):
            self.board_labels["table07card0" + str(i)] = self.game_frame.get_object("table07card0" + str(i + 1), None)
            self.player_nick["table0" + str(i + 1)] = self.game_frame.get_object("table0" + str(i + 1) + "nick", None)

        self.buttons['move_01'] = self.game_frame.get_object("move_01", None)
        self.buttons['move_02'] = self.game_frame.get_object("move_02", None)
        self.buttons['move_03'] = self.game_frame.get_object("move_03", None)

        self.buttons['move_01'].configure(text="CALL/CHECK")
        self.buttons['move_02'].configure(text="RAISE")
        self.buttons['move_03'].configure(text="FOLD")

        self.buttons['move_01'].bind('<Button-1>', lambda _: self.make_move(1))
        self.buttons['move_02'].bind('<Button-1>', lambda _: self.make_move(2))
        self.buttons['move_03'].bind('<Button-1>', lambda _: self.make_move(3))

        self.pot = self.game_frame.get_object("game_pot", None)
        self.raise_bet_slider = self.game_frame.get_object("raise_bet", None)
        self.game_frame.connect_callbacks(self)
        
    def set_controller(self, controller):
        self.controller = controller

    def clear_board(self):
        for i in range(6):
            self.display_card("table0" + str(i) + "card01", False, True)
            self.display_card("table0" + str(i) + "card02", False, True)

    def on_quit_button_click(self):
        if self.controller:
            self.controller.quit_game()

    def make_move(self, move_id):
        self.controller.make_move(move_id, self.raise_bet_slider.get())
        # self.raise_value = self.raise_bet_slider.get()

        # self.game_socket_handler.move_played(
        #     {'playerId': self.user_id,
        #      'move_id': move_id,
        #      'raise_bet': self.raise_value},
        # )

    def handle_winner(self, cards, seats, stakes):
        self.all_cards = self.game_socket_handler.game_status['all_cards']
        self.seats = self.game_socket_handler.game_status['players_at_table']
        self.stakes_data = self.game_socket_handler.game_status['stakes']

        for uuid, seat_no in self.shifted_players.items():
            if uuid not in self.seats:
                self.display_card("table0" + str(self.shifted_players[uuid]) + "card01", False, True)
                self.display_card("table0" + str(self.shifted_players[uuid]) + "card02", False, True)
            else:
                self.display_card('table0' + str(seat_no) + "card01", False, False, self.all_cards[uuid][0])
                self.display_card('table0' + str(seat_no) + "card02", False, False, self.all_cards[uuid][1])

            self.stakes[seat_no].configure(text="$" + str(self.stakes_data[uuid]))

        self.open_popup()

    def set_up_table_seats(self):
        pass 

    def update(self, actual_player, pot_value, community_cards, seats, stakes_data, game_winner = None):
        actual_player = self.seats[str(self.actual_player_id)]

        for note, stake, actual_player_token in zip(self.notes.values(), self.stakes.values(), self.act.values()):
            note.configure(text="")
            stake.configure(text="")
            actual_player_token.configure(text="")

        self.act[(actual_player - self.shift + len(self.shifted_players)) % len(self.shifted_players)].configure(text="AC")
        self.pot.config(text="POT: $" + str(self.pot_value))
        self.raise_bet_slider.configure(to=self.stakes_data[self.user_id])

        for uuid, seat_no in self.shifted_players.items():
            if uuid not in self.seats:
                self.display_card("table0" + str(self.shifted_players[uuid]) + "card01", False, True)
                self.display_card("table0" + str(self.shifted_players[uuid]) + "card02", False, True)
            elif seat_no != 0:
                self.display_card('table0' + str(seat_no) + "card01", False, False)
                self.display_card('table0' + str(seat_no) + "card02", False, False)
            else:
                self.display_card('table00card01', False, False, self.game_socket_handler.cards[0], )
                self.display_card('table00card02', False, False, self.game_socket_handler.cards[1])

            self.stakes[seat_no].configure(text="$" + str(self.stakes_data[uuid]))

        for i in range(len(self.community_cards)):
            self.display_card('table07card0' + str(i), True, False, self.community_cards[i])

        for i in range(len(self.community_cards), 5, 1):
            self.display_card('table07card0' + str(i), True, True)

    def generate_waiting_room(self, master=None):
        pass

    def open_popup(self):
        self.shift = None
        top = tk.Toplevel(self.main_window)

        def on_submit():
            top.destroy()
            self.start_game()

        top.geometry("600x150")
        top.title("Poker Game")
        text = tk.Label(top, text="Winner is " + str(self.game_socket_handler.game_status['winner']),
                        font=('Mistral 15 bold'))
        text.pack()

        if self.game_socket_handler.owner == self.user_id:
            confirm = tk.Button(top, text="Next round!", font=("Arial", 15), command=on_submit)
            confirm.pack()

    @staticmethod
    def generate_path(card_name):
        return os.path.join(CARDS_SOURCE, card_name)

    def display_card(self, label, board=False, delete_card=True, card_path="card_back.png"):

        if delete_card is True:
            fpath = os.path.join(IMAGES_SOURCE, "p_b.png")
        else:
            fpath = self.generate_path(card_path)

        WIDTH = 115
        HEIGHT = 155

        aux = Image.open(fpath).resize((WIDTH, HEIGHT), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(aux)

        if board:
            self.board_labels[label].configure(image=img, height=HEIGHT, width=WIDTH)
            self.board_labels[label].image = img
        else:
            self.players_labels[label].configure(image=img, height=HEIGHT, width=WIDTH)
            self.players_labels[label].image = img

    def start_game(self):
        self.clear_data()
        self.game_socket_handler.room_start_game()

