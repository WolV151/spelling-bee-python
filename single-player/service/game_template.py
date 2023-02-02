# Marin Donchev SDH3-B R00192936

from abc import ABC, abstractmethod
from cache.cache import GameCache

class GameManager(ABC):

    def __init__(self):
        self.game = None
        self.cache = GameCache()

    
    def set_game(self, game):
        self.game = game
    

    def end_match(self):  # unused for now
        self.game.status = False


class GameTemplate:  # the game template

    def game_process(self, submission):  # calls the different methods to create the flow of the game
        status, message = self.validate_submission(submission)
        if status is False:
            return -1, message

        score = self.check_submission(submission)
        score = self.record_score(score)
 
        return score, message

    
    @abstractmethod
    def validate_submission(self, submission): # check wether or not a word is valid
        pass


    @abstractmethod
    def check_submission(self, submission): # check what score the word should bring
        pass


    @abstractmethod
    def record_score(self, score): # record current score to total score
        pass