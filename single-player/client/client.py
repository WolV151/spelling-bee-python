import logging
import grpc
import spelling_bee_pb2 as spelling_bee_pb2
import spelling_bee_pb2_grpc as spelling_bee_pb2_grpc



def run():
    channel = grpc.insecure_channel('localhost:50055')
    stub = spelling_bee_pb2_grpc.WordGameStub(channel)

    game1 = stub.CreateGame(spelling_bee_pb2.CreateGameRequest(gameType='Spelling Bee')).gameId
    player_status = stub.RegisterPlayer(spelling_bee_pb2.RegisterPlayerRequest(gameId=game1, userName='Marin'))
    player_status1 = stub.RegisterPlayer(spelling_bee_pb2.RegisterPlayerRequest(gameId=game1, userName='John')).status
    current_word = stub.ShowSelectedWord(spelling_bee_pb2.ShowSelectedWordRequest(gameId=game1)).word


    while 1:
        print("\n" + current_word)
        user_word = input(">>>>")

        response = stub.CheckWord(spelling_bee_pb2.CheckWordRequest(gameId=game1, word=user_word))
        print(response.message + response.score)


if __name__ == "__main__":
    try:
        logging.basicConfig()
        run()
    except KeyboardInterrupt:
        print("Thank you for playing!")