class WordGame:  # a common class for a word game
                # think of it as the Darts match class from the dart application
    def __init__(self):
        self.player = None
    
    def register_player(self, username):
        if self.player is None:
            self.player = username

            return username
        else :
            print("Error: A player is already registered to that game.")
            return ""