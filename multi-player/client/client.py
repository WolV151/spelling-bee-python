import logging
import grpc
import spelling_bee_pb2 as spelling_bee_pb2
import spelling_bee_pb2_grpc as spelling_bee_pb2_grpc
from uuid import UUID

def select(): # handle user options
    while 1:
        choice = int(input('1. Create new game\n' + '2.Join game\n' + '>>>>'))
        
        if 0 < choice <= 2:
            return choice
        else:
            print('Error: Invalid input. Please select from the options.')


def handle_user(option): # option 1 to host a game
    if option == 1:

        channel = grpc.insecure_channel('localhost:50055')
        stub = spelling_bee_pb2_grpc.WordGameStub(channel)
        game = stub.CreateGame(spelling_bee_pb2.CreateGameRequest(gameType='Spelling Bee'))
        game1 = game.gameId

        username = input("Enter name: ")
        player_status = stub.RegisterPlayer(spelling_bee_pb2.RegisterPlayerRequest(gameId=game1, userName=username))
        current_word = stub.ShowSelectedWord(spelling_bee_pb2.ShowSelectedWordRequest(gameId=game1)).word

        print("You are now in waiting room.\n")
        print(f"Your game invite ID is {game.gameInvite}. Send it to the other player.")
        while 1:
            start = input("Type !start to start the game.\n")
            if (start == "!start"):
                response = stub.StartGame(spelling_bee_pb2.StartGameRequest(gameId=game1)).message
                if response == "Game starting":
                    status = stub.GetStatus(spelling_bee_pb2.GetStatusRequest(gameId=game1)).status
                    print(status)

                    if status == "IN_PROGRESS":
                        print(status)
                        run(current_word, game1, username)
                else:
                    print(response)
                    continue
            else:
                continue

    if option == 2: # option to to join a game
        gameId = input("Enter a game id: ")
        gameId = UUID(gameId)


        username = input("Enter a name: ")


        channel = grpc.insecure_channel('localhost:50055')
        stub = spelling_bee_pb2_grpc.WordGameStub(channel)
        
        player_status = stub.RegisterPlayer(spelling_bee_pb2.RegisterPlayerRequest(gameId=gameId.bytes, userName=username)).status

        current_word = stub.ShowSelectedWord(spelling_bee_pb2.ShowSelectedWordRequest(gameId=gameId.bytes)).word

        print("Waiting for host to start\n")

        while 1:
            game_status = stub.GetStatus(spelling_bee_pb2.GetStatusRequest(gameId=gameId.bytes)).status
            print(game_status)
            if game_status == "IN_PROGRESS":
                break
        run(current_word, gameId.bytes, username)



def run(current_word, gameId, username):
    while 1:

        channel = grpc.insecure_channel('localhost:50055')
        stub = spelling_bee_pb2_grpc.WordGameStub(channel)

        print("\n" + current_word)
        user_word = input(">>>>")

        response = stub.CheckWord(spelling_bee_pb2.CheckWordRequest(gameId=gameId, word=user_word, username=username))
        print(response.message + response.score)
        print("Player One Score: " + response.p1Score)
        print("Player Two Score: " + response.p2Score)
        word_resp = stub.GetPlayerWords(spelling_bee_pb2.GetPlayerWordsRequest(gameId=gameId))
        print("Player One Words: " + str(word_resp.p1Words))
        print("Player Two Words: " + str(word_resp.p2Words))


if __name__ == "__main__":
    try:
        logging.basicConfig()
        handle_user(select())
    except KeyboardInterrupt:
        print("Thank you for playing!")