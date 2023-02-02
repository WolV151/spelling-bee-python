from enum import IntEnum

class WordMultiplier(IntEnum):  # maybe add more multipliers for different games in the future
    DUMMY = 0  # grpc will not compile if this is not present
    PANGRAM_BONUS = 7


class GameStatus(IntEnum): # unused for now
    IN_PROGRESS = 0
    FINISHED = 1