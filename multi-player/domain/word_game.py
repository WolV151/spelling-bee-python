from datatype.enums import GameStatus

class WordGame:  # a common class for a word game
    # think of it as the Darts match class from the dart application
    def __init__(self):
        self.player_one = None
        self.player_two = None
        self.status = GameStatus.WAITING

    def register_player(self, username):
        if self.player_one is None:
            self.player_one = username
            return username

        elif self.player_two is None:
            self.player_two = username
            return username

        else:
            print("Error: Game is full.")
            return ""
