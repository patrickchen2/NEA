from othello import Othello
from player import Player

if __name__ == "__main__":
    
    game = Othello(Player(input("Player 1 enter your name: ")), Player(input("Player 2 enter your name: ")), 180, 1)
    game.playGame()