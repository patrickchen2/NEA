from othello import Othello
from player import Player

if __name__ == "__main__":
    
    game = Othello(Player("Player1"), Player("Player2"), 1)
    game.startGame()