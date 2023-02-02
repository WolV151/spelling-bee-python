import json
from random import randint

class GameCache: # this class bascially stores any words that are alredy guessed and deals with selecting a pangram
                # and a random center word
    def __init__(self):
        self.stored_words = []
        self.selected_pangram, self.selected_center_letter = self.select_pangram()

    
    def add_word(self, word): # store anything guessed
        self.stored_words.append(word)

    
    def get_selected_pangram(self): # get selected pangram
        return self.select_pangram
               

    def select_pangram(self): # select a new pangram from the pangrams file
        with open("./data/pangrams.json") as readfile:
            data = json.load(readfile)
            rand_num = randint(0, len(data))
            random_pangram = list(data.keys())[rand_num]
            rand_letter_num = randint(0, len(random_pangram) - 1)
            random_center_letter = random_pangram[rand_letter_num] # also select a random center word

            random_pangram = set(random_pangram)
            random_pangram = ''.join(random_pangram)
            
            return random_pangram, random_center_letter

