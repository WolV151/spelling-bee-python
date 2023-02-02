import logging
from concurrent import futures

import grpc

from game_logic import spelling_bee

from spelling_bee_pb2 import CreateGameResponse, RegisterPlayerResponse, CheckWordResponse, CheckRankingResponse, ShowSelectedWordResponce
from spelling_bee_pb2_grpc import WordGameServicer, add_WordGameServicer_to_server
from registry.registry import GameRegistry
from domain import submission, word_game
from pattern import object_factory

class SpellingBeeServer(WordGameServicer):  # server class

    def __init__(self):
        self.game_type = "Spelling Bee"
        self.factory = object_factory.ObjectFactory()
        self.factory.register_builder('Spelling Bee', spelling_bee.SpellingBeeBuilder())
        self.registry = GameRegistry.get_instance()
    

    def CreateGame(self, request, context):
        print("In create game")
        new_game = self.factory.create(request.gameType)
        game = word_game.WordGame()
        new_game.set_game(game)
        game_id = self.registry.add_game(new_game)
        print("Created a new Spelling Bee game:" + str(game_id.bytes))
        
        return CreateGameResponse(gameId = game_id.bytes)        


    def RegisterPlayer(self, request, context):
        print("Registering player")
        game = self.registry.get_game(request.gameId)
        username = game.game.register_player(request.userName)

        if not username:
            print("No username to register")
            return RegisterPlayerResponse(status="ERROR")

        print("Sucessfully registered player " + username + " to game" + str(request.gameId))

        return RegisterPlayerResponse(status="OK")


    def ShowSelectedWord(self, request, context):
        print("Showing selected word (pangram)")
        game = self.registry.get_game(request.gameId)
        word = game.cache.selected_pangram
        center_letter = game.cache.selected_center_letter
        word = word.replace(center_letter, f"[{center_letter}]")
        return ShowSelectedWordResponce(word=word)

    
    def CheckWord(self, request, context):
        print("Checking word " + request.word)
        my_submission = submission.Submission()
        my_submission.set_word(request.word)
        game = self.registry.get_game(request.gameId)
        score, message = game.game_process(my_submission)
        score = f" Your score is {score}"

        return CheckWordResponse(score=str(score), message=message)


    def CheckRanking(self, request, context):
        print("Checking ranking")
        


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_WordGameServicer_to_server(SpellingBeeServer(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()