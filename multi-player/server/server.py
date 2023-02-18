import logging
from concurrent import futures

import grpc

from game_logic import spelling_bee

from spelling_bee_pb2 import CreateGameResponse, RegisterPlayerResponse, CheckWordResponse, CheckRankingResponse, ShowSelectedWordResponce, StartGameResponse, GetStatusResponse, GetPlayerWordsResponse
from spelling_bee_pb2_grpc import WordGameServicer, add_WordGameServicer_to_server
from registry.registry import GameRegistry
from domain import submission, word_game
from pattern import object_factory

import json
import os
import sys
import pika


class SpellingBeeServer(WordGameServicer):  # server class

    def __init__(self):
        self.game_type = "Spelling Bee"
        self.factory = object_factory.ObjectFactory()
        self.factory.register_builder(
            'Spelling Bee', spelling_bee.SpellingBeeBuilder())
        self.registry = GameRegistry.get_instance()
        self.game_score = []


    def CreateGame(self, request, context):
        print("In create game")
        new_game = self.factory.create(request.gameType)
        game = word_game.WordGame()
        new_game.set_game(game)
        game_id = self.registry.add_game(new_game)
        print("Created a new Spelling Bee game:" + str(game_id.bytes))
        print(game_id)

        return CreateGameResponse(gameId=game_id.bytes, gameInvite=str(game_id))

    def RegisterPlayer(self, request, context):
        print("Registering player")
        game = self.registry.get_game(request.gameId)
        username = game.game.register_player(request.userName)

        if not username:
            print("No username to register")
            return RegisterPlayerResponse(status="ERROR")

        print("Sucessfully registered player " +
              username + " to game" + str(request.gameId))

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
        my_submission.set_player(request.username)
        game = self.registry.get_game(request.gameId)
        score, message, player, p1_score, p2_score = game.game_process(
            my_submission)
        score = f" Total score is {score}"

        # construct a message, declare a message queue and send it to the client
        self.game_score = ["GameID: " + str(request.gameId), "Player 1:" + game.game.player_one, "Player 2:" + game.game.player_two,
        "Player 1 Score: " + str(p1_score), "Player 2 Score: " + str(p2_score), "Total Score: " + str(score)]
        
        message_pika = self.game_score

        connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
        channel = connection.channel()
        channel.queue_declare(queue='games_stats')
        channel.basic_publish(exchange='', routing_key='games_stats', body=json.dumps(message_pika))
        connection.close()

        return CheckWordResponse(score=str(score), message=message, p1Score=str(p1_score), p2Score=str(p2_score))

    
    def CheckRanking(self, request, context):
        print("Checking ranking")

    
    def GetStatus(self, request, context):
        game = self.registry.get_game(request.gameId)
        status = game.game.status

        if status == 0:
            return GetStatusResponse(status="WAITING")
        elif status == 1:
            return GetStatusResponse(status="IN_PROGRESS")
        else:
            return GetStatusResponse(status="FINISHED")

   
    def StartGame(self, request, context):
        print("Attempting to start game with id: " + str(request.gameId))
        game = self.registry.get_game(request.gameId)

        if (game.game.player_two is None) or (game.game.player_one is None):
            return StartGameResponse(message="Cannot start without player two!")
        else:
            game.start_game()
            return StartGameResponse(message="Game starting")

    
    def GetPlayerWords(self, request, context):
        print("Requested both player's words")
        game = self.registry.get_game(request.gameId)

        return GetPlayerWordsResponse(p1Words=game.cache.words_p1, p2Words=game.cache.words_p2)




def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_WordGameServicer_to_server(SpellingBeeServer(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()





if __name__ == "__main__":
    logging.basicConfig()
    serve()
