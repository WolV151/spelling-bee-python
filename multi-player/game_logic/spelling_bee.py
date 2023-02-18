from service.game_template import GameTemplate, GameManager
from datatype.enums import GameStatus, WordMultiplier
import json

class SpellingBee(GameTemplate, GameManager): # Spelling Bee game, implements a word game Template
    def __init__(self):
        super().__init__()
        self.score = 0
        self.score_p1 = 0  # score for p1
        self.score_p2 = 0  # score for p2


    def init_game(self):
        self.game.status = GameStatus.IN_PROGRESS


    def validate_submission(self, submission):  # check if a word is valid
        flag = True
        message = "Valid word!"

        if len(submission.word) < 4: # less letters than 4
            flag = False
            message = "A word must be at least 4 letters long!"
            return flag, message

        if not (set(submission.word) <= set(self.cache.selected_pangram)): # uses only letters provided
            flag = False
            message = "You must use the letters provided!"
            return flag, message

        if self.cache.selected_center_letter not in submission.word: # has center letter
            flag = False
            message = "You must use the center letter! (the one in [])."
            return flag, message

        if submission.word in self.cache.stored_words: # if the word is already guessed
            flag = False
            message = "This word was already guessed!"
            return flag, message
        
        with open("./data/words_dictionary.json") as readfile:  # check the dictionary to see if it's actually a word
            data = json.load(readfile)

            if submission.word not in data:
                flag = False
                message = "This is not a valid word."
                return flag, message
        
        self.cache.add_word(submission.word)
        
        if self.game.player_one == submission.player:
            self.cache.add_word_p1(submission.word)
        else:
            self.cache.add_word_p2(submission.word)

        return flag, message


    def check_submission(self, submission): # this class checks what score should the word bring to the player 
        score = 0
        player = submission.player
        if len(submission.word) == 4:
            score = 1
        elif len(submission.word) > 4:
            score = len(submission.word)
            with open("./data/pangrams.json") as pangramfile:
                data = json.load(pangramfile)
                if submission.word in data:  # if it is a pangram apply the bonus
                    print("You found a pangram!")
                    score += WordMultiplier.PANGRAM_BONUS
        return score, player
    

    def record_score(self, score, player):  # this adds the current word score to the total score
        if self.game.player_one == player:
            self.score_p1 += score
        else:
            self.score_p2 += score

        self.score += score
        return self.score

    
    def print_score(self):
        print("Your current score is: " + self.score)


class SpellingBeeBuilder():  # this is the builder for this particular word game
    def __init__(self):
        pass

 
    def __call__(self):
        return SpellingBee()

    