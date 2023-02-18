import threading
import uuid


class GameRegistry:  # this is the game registry, it is completely identical to the one in the darts application

    __instance = None

    def __init__(self):
        if GameRegistry.__instance is not None:
            raise Exception("This is a singleton!")
        else:
            GameRegistry.__instance = self
        
        self.lock = threading.Lock()
        self.stored_games = {}
        self.instance = None


    @staticmethod    
    def get_instance():
        if GameRegistry.__instance is None:
            with threading.Lock():
                if GameRegistry().__instance is None:
                    GameRegistry()
        
        return GameRegistry.__instance


    def add_game(self, game):
        self.lock.acquire()
        game_id = uuid.uuid4()
        
        self.lock.release()
        self.stored_games[game_id] = game
        return game_id

    
    def get_game(self, game_id):
        return self.stored_games[uuid.UUID(bytes=game_id)]