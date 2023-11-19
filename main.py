from othelloTerm import terminal
from othelloGUI import GUI

if __name__ == "__main__":
    choice = input("Terminal or GUI? ")
    if choice == "Terminal":
        player1 = input("Enter player 1 name: ")
        player2 = input("Enter player 2 name: ")
        game = terminal(player1, player2)
    elif choice == "GUI":
        game = GUI()
    game.run()