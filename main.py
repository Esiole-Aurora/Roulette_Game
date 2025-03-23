import random

import termcolor
from termcolor import colored


class Game:
    numbers: list = range(0,37)
    players: list = []
    bets_payouts: dict = {"c":2, "o":2, "h":2, "u":3, "d":3, "s":36}
    current_bets: list = []
    colour_numbers: dict = {"R": [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36],
                            "B": [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]}

    def __init__(self):
        self.numbers = Game.numbers
        self.players = Game.players
        self.bets_payouts = Game.bets_payouts
        self.current_bets = Game.current_bets
        self.colour_numbers = Game.colour_numbers
        self.game_loop()

    def game_loop(self) -> None:
        self.get_players()
        while self.players:
            self.place_bets()
            current_number: int = self.generate_number()
            print("Current number: ", current_number)
            self.resolve_bets(current_number)
            self.eliminate_players()


    def get_players(self) -> None:
        player_count: int = 0
        again: str = "Y"
        while again.upper() == "Y":
            name: str = input("Please enter your name: ")
            new_player: Player = Player(name, player_count)
            self.players.append(new_player)

            player_count += 1
            print("Is there another player? Y/N")
            again = input()

    def eliminate_players(self) -> None:
        for player in self.players:
            if player.chips == 0:
                print(f"{player.name} has no chips!")
                self.players.remove(player)

    def place_bets(self) -> None:
        for player in self.players:
            self.display_board()
            print(f"{player.name}'s chips: {player.chips}")
            print("c: Colour Bet \no: Odd/Even Bet\nh: High/Low Bet\nu: Column Bet \nd: Dozen Bet \ns: Straight Bet")
            valid:bool = False
            while not valid:
                bet_type: str = input("Please enter your bet type: ")
                bet_amount: int = int(input("Please enter your bet amount: "))
                if bet_type in ["c", "o", "h", "u", "d", "s"] and bet_amount <= player.chips:
                    valid = True

            if bet_type == "c":
                colour:str = input("Please enter a Colour R/B: ").upper()
                bet:tuple = (player.player_ref,bet_type,bet_amount,colour)
            elif bet_type == "o":
                odd_even:str = input("Please enter O/E: ").upper()
                bet:tuple = (player.player_ref, bet_type, bet_amount, odd_even)
            elif bet_type == "h":
                high_low:str = input("Please enter H/L: ").upper()
                bet:tuple = (player.player_ref, bet_type, bet_amount, high_low)
            elif bet_type == "u":
                column:str = input("Please enter Column [1/2/3]: ")
                bet:tuple = (player.player_ref, bet_type, bet_amount, column)
            elif bet_type == "d":
                dozen:str = input("Please enter Dozen [1/2/3]: ")
                bet:tuple = (player.player_ref, bet_type, bet_amount, dozen)
            elif bet_type == "s":
                straight:str = input("Please enter Value: ")
                bet:tuple = (player.player_ref, bet_type, bet_amount, straight)

            self.current_bets.append(bet)

    def resolve_bets(self, current_value: int) -> None:
        for bet in self.current_bets:
            for player in self.players:
                if player.player_ref == bet[0]:
                    if bet[1] == "c":
                        if current_value in self.colour_numbers[bet[3].upper()]:
                            player.chips -= bet[2]
                            player.chips += bet[2] * self.bets_payouts[bet[1]]
                        else:
                            player.chips -= bet[2]
                    elif bet[1] == "o":
                        if bet[3] == "e" and current_value % 2 == 0:
                            player.chips -= bet[2]
                            player.chips += bet[2]*self.bets_payouts[bet[1]]

                        elif bet[3] == "o" and current_value % 2 == 1:
                            player.chips -= bet[2]
                            player.chips += bet[2] * self.bets_payouts[bet[1]]
                        else:
                            player.chips -= bet[2]

                    elif bet[1] == "h":
                        if bet[3] == "h" and current_value > 18:
                            player.chips -= bet[2]
                            player.chips += bet[2] * self.bets_payouts[bet[1]]
                        elif bet[3] == "u" and current_value <= 18:
                            player.chips -= bet[2]
                            player.chips += bet[2] * self.bets_payouts[bet[1]]
                        else:
                            player.chips -= bet[2]

                    elif bet[1] == "u":
                        if bet[3] == "1" and current_value % 3 == 1:
                            player.chips -= bet[2]
                            player.chips += bet[2] * self.bets_payouts[bet[1]]
                        elif bet[3] == "2" and current_value % 3 == 2:
                            player.chips -= bet[2]
                            player.chips += bet[2] * self.bets_payouts[bet[1]]
                        elif bet[3] == "3" and current_value % 3 == 0:
                            player.chips -= bet[2]
                            player.chips += bet[2] * self.bets_payouts[bet[1]]
                        else:
                            player.chips -= bet[2]

                    elif bet[1] == "d":
                        if bet[3] == "1" and current_value >= 1 and current_value <= 12:
                            player.chips -= bet[2]
                            player.chips += bet[2] * self.bets_payouts[bet[1]]
                        elif bet[3] == "2" and current_value >= 13 and current_value <= 24:
                            player.chips -= bet[2]
                            player.chips += bet[2] * self.bets_payouts[bet[1]]
                        elif bet[3] == "3" and current_value > 24:
                            player.chips -= bet[2]
                            player.chips += bet[2] * self.bets_payouts[bet[1]]
                        else:
                            player.chips -= bet[2]

                    elif bet[1] == "s":
                            if bet[3] == current_value:
                                player.chips -= bet[2]
                                player.chips += bet[2] * self.bets_payouts[bet[1]]
                            else:
                                player.chips -= bet[2]
        self.current_bets = []

    def display_board(self) -> None:
        print(f"  {self.numbers[0]}   ")
        for i in range(1, 37, 3):
            print(f"{self.numbers[i]}|{self.numbers[i+1]}|{self.numbers[i+2]}")
            self.construct_horizontal()

    def construct_horizontal(self) -> None:
        print("-----")

    def generate_number(self) -> int:
        random_number: int = random.randint(0,37)
        return random_number

class Player:
    player_ref: int
    chips: int = 100
    name: str
    def __init__(self, name, reference):
        self.name = name
        self.chips = Player.chips
        self.player_ref = reference

new_game: Game = Game()