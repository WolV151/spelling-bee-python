class Submission:  # this is basically the class that contains the word that the client provides and server checks it
                    # think of it as the Visit class from the darts application
    def __init__(self):
        self.word = None
        self.player = None # added a player for this one
    
    def get_player():
        return self.player

    def set_player(self, player):
        self.player = player


    def get_word():
        return self.word

    
    def set_word(self, word):
        self.word = word


    def get_length():
        return len(self.word)