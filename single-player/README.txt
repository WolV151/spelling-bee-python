Marin Donchev SDH3-B R00192936

The purpose of this file is to explain the patterns I chose and why I chose them.


SINGLETON:
To start with, I created a game registry, which will store all the current games on a server. This allows multiple games to be ran on the same server. I made sure this class to be a singleton class, because we will only ever need one registry per server to store all the games. The registry is present in the registry/registry.py file. It is called inside the server.py

FACTORY:
The next pattern I chose is the Factory pattern. I used this pattern, because in the future we might have to create other similar games to the Spelling Bee, therefore it would be easier to create instances of those games by just passing the required game builder to the Object Factory. The class is present in pattern/object_factory.py, every word game needs to implement it's own builder (For example, game_logic/spelling_bee.py has SpellingBeeBuilder()).

TEMPLATE:
The final pattern to talk about is the Template pattern. I chose this pattern for the same reason as above. I created a template for a word game that checks if a word submission from the client is valid or not, calculates some score based on the submission and records that score to the total score of the player. I believe that other similar word games would act in the same manner, maybe with different rules on checking if a word is valid, maybe a different score system. The template is present in pattern/game_template.py. Every word game needs to inherit this pattern and implement the abstract methods it has in order to implement its logic. Currently there is only a single game, which inherits this template - the Spelling Bee game. This class can be found in game_logic/spelling_bee.py.

One fact to note here is that I put the logic that checks whether or not a word is valid, meaining if it is present in the dictionary, inside the game itself (spelling_bee.py), I am aware there will be code replication when implementing other games, since checking the dictionary, to see if the word is present in it, would use the same method. This could have been done, as you mentioned, inside a dictionary component which would be a singleton.
