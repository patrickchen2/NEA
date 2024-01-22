from othelloTerm import terminal
from othelloGUI import GUI

if __name__ == "__main__":
    #skill class B - generation of objects based on simple OOP
    choice = input("Terminal or GUI? ")
    if choice.lower() == "terminal":
        player1 = input("Enter player 1 name: ")
        player2 = input("Enter player 2 name: ")
        
        game = terminal(player1, player2)
    elif choice.lower() == "gui":
        game = GUI()
    game.run()