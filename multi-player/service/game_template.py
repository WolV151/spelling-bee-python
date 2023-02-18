from abc import ABC, abstractmethod
from cache.cache import GameCache
from datatype.enums import GameStatus

class GameManager(ABC):

    def __init__(self):
        self.game = None
        self.cache = GameCache()

    
    def set_game(self, game):
        self.game = game
    

    def start_game(self):
        self.init_game()


    def end_match(self):
        self.game.status = GameStatus.FINISHED

    
    @abstractmethod
    def init_game(self):
        pass


class GameTemplate:  # the game template

    def game_process(self, submission):  # calls the different methods to create the flow of the game
        status, message = self.validate_submission(submission)

        p1_score = self.score_p1
        p2_score = self.score_p2

        if status is False:
            return self.score, message, "0", p1_score, p2_score

        score, player = self.check_submission(submission)
        score = self.record_score(score, player)

        p1_score = self.score_p1
        p2_score = self.score_p2

        return score, message, player, p1_score, p2_score

    
    @abstractmethod
    def validate_submission(self, submission): # check wether or not a word is valid
        pass


    @abstractmethod
    def check_submission(self, submission): # check what score the word should bring
        pass


    @abstractmethod
    def record_score(self, score): # record current score to total score
        pass