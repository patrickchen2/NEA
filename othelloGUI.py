import tkinter as tk
from abc import ABC, abstractmethod
from othello import Othello
from player import Player
from computer import Computer
from database import dbms
from hashlib import sha256
import tkinter.messagebox as messagebox
import copy
import random
import time

class UI(ABC):
    # class A skill - inheritance, polymorphism
    @abstractmethod
    def run(self):
        '''
            Method: run
            Parameters: None
            Returns: None
            Does: Runs the game
        '''
        raise NotImplementedError
    
class GUI(UI):
    def __init__(self):
        self.datams = dbms()
        super().__init__()
        self.help_win = None
        self._game_win = None
        root = tk.Tk()
        root.title("Othello")
        root.geometry("300x300")
        self.loggedin = False
        self.pref = None

        tk.Button(root, text= "Login", command=self.login).grid(row=0, column=0, padx=5, pady=5, columnspan = 5)
        tk.Button(root, text= "Register", command=self.register).grid(row=1, column=0, padx=5, pady=5, columnspan = 5)
        tk.Button(root, text= "Play As Guest", command=self.mainscreen).grid(row=2, column=0, padx=5, pady=5, columnspan = 5)
        
        self._root = root

    def mainscreen(self):
        '''
        Displays the main screen after logging in or playing as guest. 
        logged in:
        - Multi Player
        - Single Player
        - Load Game
        - How to Play
        - Profile
        - Preferences
        - Leaderboard
        - Quit
        
        not logged in:
        - Multi Player
        - Single Player
        - Load Game
        - How to Play
        - Quit'''
        mainscreen = tk.Toplevel(self._root)
        tk.Button(mainscreen, text="Multi Player", command=self.options1).grid(row=0, column=0, padx=5, pady=5, columnspan = 5)
        tk.Button(mainscreen, text="Single Player", command=self.options2).grid(row=1, column=0, padx=5, pady=5, columnspan = 5)
        tk.Button(mainscreen, text="Load Game", command=self.loadGame).grid(row=2, column=0, padx=5, pady=5, columnspan = 5)
        tk.Button(mainscreen, text="How to Play", command=self.help).grid(row=3, column=0, padx=5, pady=5, columnspan = 5)

        if self.loggedin:
            tk.Button(mainscreen, text="Profile", command=self.profile).grid(row=4, column=0, padx=5, pady=5, columnspan = 5)
            tk.Button(mainscreen, text = "Preferences", command=self.preferences).grid(row=5, column=0, padx=5, pady=5, columnspan = 5)
            tk.Button(mainscreen, text = "Leaderboard", command=self.leaderboard).grid(row=6, column=0, padx=5, pady=5, columnspan = 5)
            tk.Button(mainscreen, text="Quit", command=self._root.quit).grid(row=7, column=0, padx=5, pady=5, columnspan = 5)
        else:
            tk.Button(mainscreen, text="Quit", command=self._root.quit).grid(row=4, column=0, padx=5, pady=5, columnspan = 5)

    def leaderboard(self):
        '''Displays the leaderboard of the top 5 scores along with their player names
        1. name: score
        etc'''
        leaderboard = tk.Toplevel(self._root)
        leaderboard.title("Leaderboard")
        stats = self.datams.getallstats()
        stats.sort(key=lambda x: x[3], reverse=True)
        #take the top 5
        if len(stats) > 5:
            stats = stats[:5]
            for i in range(len(stats)):
                tk.Label(leaderboard, text=f"{i+1}. {stats[i][0]}: {stats[i][3]}").grid(row=i, column=0)
        else:
            for i in range(len(stats)):
                tk.Label(leaderboard, text=f"{i+1}. {stats[i][0]}: {stats[i][3]}").grid(row=i, column=0)

    def login(self):
        '''
        Displays the login screen
        Username:
        Password:
        Login (button)
        '''
        login = tk.Toplevel(self._root)
        user = tk.Label(login, text="Username: ")
        user.grid(row=0, column=0)
        self.userentry = tk.Entry(login, width = 60)
        self.userentry.grid(row=0, column=1)

        password = tk.Label(login, text="Password: ")
        password.grid(row=1, column=0)
        self.passwordentry = tk.Entry(login, width = 60, show="*")
        self.passwordentry.grid(row=1, column=1)

        loginbutton = tk.Button(login, text="Login", command=self.login2)
        loginbutton.grid(row=2, column=0, columnspan=2)

    def login2(self):
        '''
        checks if a username and password are valid by matching to the database
        '''
        username = self.userentry.get()
        password = self.passwordentry.get()
        self.datams = dbms()
        validation = self.datams.checkUser(username, self.hash(password))
        if validation == []:
            messagebox.showinfo("Invalid Login", "Invalid Login")
        else:
            self.user = username
            self.loggedin = True
            self.mainscreen()

    def register(self):
        '''
        displays the register screen
        Username:
        Password:
        Register (button)
        '''
        register = tk.Toplevel(self._root)
        user = tk.Label(register, text="Username: ")
        user.grid(row=0, column=0)
        self.userentry = tk.Entry(register, width = 60)
        self.userentry.grid(row=0, column=1)

        password = tk.Label(register, text="Password: ")
        password.grid(row=1, column=0)
        self.passwordentry = tk.Entry(register, width = 60, show="*")
        self.passwordentry.grid(row=1, column=1)

        registerbutton = tk.Button(register, text="Register", command=self.register2)
        registerbutton.grid(row=2, column=0, columnspan=2)

    def register2(self):
        '''
        checks if a username is taken and if not, registers the user, by adding the relevant records into the tables
        '''
        username = self.userentry.get()
        password = self.passwordentry.get()
        if self.datams.checkifUserExists(username):
            messagebox.showinfo("Username Taken", "Username Taken")
        else:  
            self.datams.Insert("usernames", f"('{username}', '{self.hash(password)}')")
            self.datams.Insert("statistics", f"('{username}', 0, 0, 0)")
            self.datams.Insert("preferences", f"('{username}', 1, 0, 'dark green', 0, 1)")
            self.datams.Insert("preferences", f"('{username}', 1, 0, 'dark green', 0, 2)")
            self.datams.Insert("preferences", f"('{username}', 1, 0, 'dark green', 0, 3)")

    def hash(self, password):
        '''
        hashes the password using sha256
        '''
        hashed_password = sha256(password.encode()).hexdigest()
        return hashed_password
    
    def profile(self):
        '''
        displays the profile screen
        wins:
        losses:
        score:
        '''
        pro = tk.Toplevel(self._root)
        stats = self.datams.getstatistics(self.user)
        wins = tk.Label(pro, text="Wins: " + str(stats[0][1]))
        wins.grid(row=0, column=0)
        loss = tk.Label(pro, text="Loss: " + str(stats[0][2]))
        loss.grid(row=1, column=0)
        score = tk.Label(pro, text="Score: " + str(stats[0][3]))
        score.grid(row=2, column=0)

    def preferences(self):
        '''
        displays the preferences screen
        Computer Difficulty:
        Hints:
        Board Colour:
        Valid Moves:
        Save 1 (button)
        Save 2 (button)
        Save 3 (button)

        is shown later on to choose between 3 or a new one
        '''

        pref = tk.Toplevel(self._root)

        computerdifficulty = tk.Label(pref, text="Computer Difficulty: ")
        computerdifficulty.grid(row=0, column=0)
        self.computerdifficultyentry = tk.Entry(pref, width = 60)
        self.computerdifficultyentry.grid(row=0, column=1)

        hints = tk.Label(pref, text="Hints (0 or 1): ")
        hints.grid(row=1, column=0)
        self.hintsentry = tk.Entry(pref, width = 60)
        self.hintsentry.grid(row=1, column=1)

        boardcolour = tk.Label(pref, text="Board Colour: ")
        boardcolour.grid(row=2, column=0)
        self.boardcolourpref = tk.Button(pref, text="dark green", command=self.boardcolourp, bg="dark green")
        self.boardcolourpref.grid(row=2, column=1, columnspan=2)

        valids = tk.Label(pref, text="Valid Moves (0 or 1): ")
        valids.grid(row=3, column=0)
        self.validsentry = tk.Entry(pref, width = 60)
        self.validsentry.grid(row=3, column=1)

        save1 = tk.Button(pref, text="Save 1", command=self.savepref1)
        save1.grid(row=4, column=0, columnspan=2)

        save2 = tk.Button(pref, text="Save 2", command=self.savepref2)
        save2.grid(row=4, column=1, columnspan=2)

        save3 = tk.Button(pref, text="Save 3", command=self.savepref3)
        save3.grid(row=4, column=2, columnspan=2)

    def savepref1(self):
        ###########################
        # Excellent Coding Style - Good Exception Handling
        ###########################
        try:
            computerdifficulty = int(self.computerdifficultyentry.get())
            hints = int(self.hintsentry.get())
            valids = int(self.validsentry.get())
        except ValueError:
            messagebox.showinfo("Invalid Preferences", "Invalid Preferences")
        self.datams.editpreference(self.user, "computerdiff", computerdifficulty, 1)
        self.datams.editpreference(self.user, "hints", hints, 1)
        self.datams.editpreference(self.user, "boardcolour", self.boardcolourpref.cget("text"), 1)
        self.datams.editpreference(self.user, "validmoves", valids, 1)
    
    def savepref2(self):
        try:
            computerdifficulty = int(self.computerdifficultyentry.get())
            hints = int(self.hintsentry.get())
            valids = int(self.validsentry.get())
        except ValueError:
            messagebox.showinfo("Invalid Preferences", "Invalid Preferences")
        self.datams.editpreference(self.user, "computerdiff", computerdifficulty, 2)
        self.datams.editpreference(self.user, "hints", hints, 2)
        self.datams.editpreference(self.user, "boardcolour", self.boardcolourpref.cget("text"), 2)
        self.datams.editpreference(self.user, "validmoves", valids, 2)

    def savepref3(self):
        try:
            computerdifficulty = int(self.computerdifficultyentry.get())
            hints = int(self.hintsentry.get())
            valids = int(self.validsentry.get())
        except ValueError:
            messagebox.showinfo("Invalid Preferences", "Invalid Preferences")
        self.datams.editpreference(self.user, "computerdiff", computerdifficulty, 3)
        self.datams.editpreference(self.user, "hints", hints, 3)
        self.datams.editpreference(self.user, "boardcolour", self.boardcolourpref.cget("text"), 3)
        self.datams.editpreference(self.user, "validmoves", valids, 3)
        
    def boardcolourp(self):
        '''
        toggles the board colour button, to change the colour of the board in the game
        '''
        colours = ["dark green", "blue", "red", "yellow", "orange", "purple", "pink", "brown"]
        index = colours.index(self.boardcolourpref.cget("text"))
        if index == len(colours)-1:
            index = 0
        else:
            index += 1
        
        self.boardcolourpref.config(text=colours[index])
        self.boardcolourpref.config(bg=colours[index])
    
    def help(self):
        '''
        displays the help screen and explains how to play the game
        '''
        howtoplay = tk.Toplevel(self._root)
        howtoplay.title("How to Play")
        howtoplay.geometry("500x300")
        howtoplaytext = tk.Text(howtoplay, height=20, width=50)
        howtoplaytext.grid(row=0, column=0, padx=5, pady=5, columnspan = 5)
        howtoplaytext.insert(tk.END, "How to Play\n")
        howtoplaytext.insert(tk.END, "1. The game starts with 4 pieces in the middle of the board, 2 black and 2 white\n2. Black always goes first\n3. The goal of the game is to have the most pieces on the board\n4. To place a piece, click on the square you want to place it in\n5. You can only place a piece in a square that will flip at least one of your opponent's pieces\n6. If you cannot place a piece, you must pass\n7. The game ends when there are no more valid moves\n8. The player with the most pieces wins\n")                                  
    
    def play(self, gamemode, loadno):
        if self._game_win:
            return
        if loadno != 0:
            self._game = Othello(Player("Player 1"), Player("Player 2"), 1)
            self._player1 = self._game.getPlayer1Name()
            self._player2 = self._game.getPlayer2Name()
            self._game.loadGame(loadno)
            self.isloaded = True
            self._game.pushstack()
        elif loadno > 3 or loadno < 0:
            ############################
            # Excellent Coding Style - Defensive Programming
            ############################
            return
        else:
            self.isloaded = False
            self._player1 = self.player1entry.get()
            #self._player2 = self.player2entry.get()

            if gamemode == 2:
                self._player2 = self.player2entry.get()
                self._game = Othello(Player(self._player1), Player(self._player2), 1)
            else:
                if self.pref:
                    # checks whether the user has chosen to use one of their preset preferences
                    self._player1 = self.pref[0]
                    self._player2 = "Computer"
                    self._difficulty = self.pref[1]
                else:
                    self._player1 = self.player1entry.get()
                    self._player2 = "Computer"
                    ###########################
                    # Excellent Coding Style - Good Exception Handling
                    ###########################

                    ############################
                    # Good Coding Style - Managed Casting of Types
                    ############################
                    try:
                        self._difficulty = int(self.difficultentry.get())
                        if self._difficulty == 0 or self._difficulty >= 5:
                            messagebox.showinfo("Invalid Difficulty", "Invalid Difficulty")
                            self._difficulty = 1
                    except ValueError:
                        #someone has entered an incorrect value so the difficulty is set to 1
                        self._difficulty = 1
                
                self._game = Othello(Player(self._player1), Computer(self._player2), 1)
                self._game.setDifficult(self._difficulty)

            self._game.setupGame()
            self._game.setGamemode(gamemode)

        
        self._game.pushstack()
        self._finished = False

        # sets the start numbers for the end score
        self.undos = 0
        self.hint = 0

        self._game_win = tk.Toplevel(self._root)
        self._game_win.title("Othello")
        #game_win.geometry("500x500")
        
        self.canvassize = 700
        tk.Grid.rowconfigure(self._game_win, 0, weight=1)
        tk.Grid.columnconfigure(self._game_win, 0, weight=1)

        #establish the board and the colour depending on their choice
        if self.pref:
            self.c = tk.Canvas(self._game_win, width=self.canvassize, height=self.canvassize, bg=self.pref[3])
        elif loadno == 0:
            self.c = tk.Canvas(self._game_win, width=self.canvassize, height=self.canvassize, bg=self.boardcolourbutton.cget("text"))
        else:
            self.c = tk.Canvas(self._game_win, width=self.canvassize, height=self.canvassize, bg="dark green")

        self.c.grid(row = 0, column = 0, padx= 5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.c.bind("<Button-1>", self.move)
        
        # display who's turn it is
        if self._game.getTurn()%2 == 1:
            self.indicator = tk.Label(self._game_win, text="Black's Turn")
        else:
            self.indicator = tk.Label(self._game_win, text="White's Turn")
        self.indicator.grid(row = 0, column = 2, padx= 5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

        # log of all the moves
        self.t = tk.Text(self._game_win, height=2, width=30)
        self.t.grid(row = 0, column = 1, padx= 5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

        self.blackscore = tk.Label(self._game_win, text="Black: " + str(self._game.getBlackScore(self._game.getBoard())))
        self.blackscore.grid(row=1, column=1, columnspan=2)

        self.whitescore = tk.Label(self._game_win, text="White: " + str(self._game.getWhiteScore(self._game.getBoard())))
        self.whitescore.grid(row=1, column=2, columnspan=2)

        self.savebutton = tk.Button(self._game_win, text="Save", command=self.saveGame)
        self.savebutton.grid(row=2, column=1, columnspan=2)

        #self.loadbutton = tk.Button(self._game_win, text="Load", command=self.loadGame)
        #self.loadbutton.grid(row=2, column=2, columnspan=2)

        self.u = tk.Button(self._game_win, text = "Undo", command = self.undo)
        self.u.grid(row=1, column=0, columnspan=5)

        # display the hint button
        if gamemode == 1 and loadno == 0:
            if self.hintbutton.cget("text") == "Enabled":
                self.hintbutton = tk.Button(self._game_win, text="Hint", command=self.givehint)
                self.hintbutton.grid(row=3, column=1, columnspan=2)
            elif self.pref:
                if self.pref[2] == 1:
                    self.hintbutton = tk.Button(self._game_win, text="Hint", command=self.givehint)
                    self.hintbutton.grid(row=3, column=1, columnspan=2)

        self.quitbutton = tk.Button(self._game_win, text="Quit", command=self.gameClose)
        self.quitbutton.grid(row=2, column=0, columnspan=5)

        self.displayBoard(self._game_win)

    def move(self, event):
        if self._game.getTurn()%2 == 1:
            colour = 1
        else:
            colour = 2

        x,y = event.x, event.y
        ratio = self.canvassize/8
        ###########################
        # Excellent Coding Style - Good Exception Handling
        ###########################
        try:
            x = int(x//ratio)
            y = int(y//ratio)
        except Exception as e:
            print(e)

        # to check if the location is valid
        validmoves = self._game.getValidMoves(self._game.getBoard(), colour)
        valid, dir = self._game.isvalidmove(self._game.getBoard(), x, y, colour)

        if valid:
            # play the move
            self._game.playGame(None, x, y, colour, dir)
            if colour == 1:
                self.t.insert(tk.END, self._player1 + ": " + str(x) + "," + str(y) + "\n")
                self.indicator.config(text="White's Turn")
            elif colour == 2:
                self.t.insert(tk.END, self._player2 + ": " + str(x) + "," + str(y) + "\n")
                self.indicator.config(text="Black's Turn")

            # if it is a single player game, process the computer move
            if self._game.getGamemode() == 1:
                
                self._game.setTurn(1)

                ended = self.checkend()
                if ended:
                    self.gameClose()
                    return
                self.displayBoard(self._game_win)

                # update the canvas and window
                self._root.update()
                self._root.update_idletasks()

                #computer's turn
                if colour == 1:
                    computercolour = 2
                else:
                    computercolour = 1
                validmoves = self._game.getValidMoves(self._game.getBoard(), computercolour)
                # if the computer can't play any moves skip their turn
                if len(validmoves) == 0:
                    self._game.setTurn(1)
                    self.indicator.config(text="Black's Turn")
                    self.t.insert(tk.END, "Black: No valid moves\n")
                    self._root.update()
                    self._root.update_idletasks()
                    return
                while True:
                    #unbind all the buttons and canvas
                    self.c.unbind("<Button-1>")
                    self.u.config(state=tk.DISABLED)
                    self.savebutton.config(state=tk.DISABLED)
                    self.quitbutton.config(state=tk.DISABLED)
                    try:
                        self.hintbutton.config(state=tk.DISABLED)
                    except:
                        pass
                    self._root.update()
                    self._root.update_idletasks()

                    compmove = self._game.cmove()
                    if compmove:
                        self._game.playGame(None, compmove[0][1], compmove[0][0], computercolour, compmove[1])
                        self.t.insert(tk.END, self._player2 + ": " + str(compmove[0][1]) + "," + str(compmove[0][0]) + "\n")
                        time.sleep(2)

                    #rebind all the buttons and canvas
                    self.c.bind("<Button-1>", self.move)
                    self.u.config(state=tk.NORMAL)
                    self.savebutton.config(state=tk.NORMAL)
                    self.quitbutton.config(state=tk.NORMAL)
                    try:
                        self.hintbutton.config(state=tk.NORMAL)
                    except:
                        pass
                    self._root.update()
                    self._root.update_idletasks()

                    #display the new board                
                    self.displayBoard(self._game_win)
                    self._root.update()
                    self._root.update_idletasks()
           
                    #do the necessary updates
                    self.whitescore.config(text="White: " + str(self._game.getWhiteScore(self._game.getBoard())))
                    self.blackscore.config(text="Black: " + str(self._game.getBlackScore(self._game.getBoard())))
                    ended = self.checkend()
                    if ended:
                        self.gameClose()
                        return

                    #checking whether the user can play any moves
                    if len(self._game.getValidMoves(self._game.getBoard(), colour)) != 0:
                        self._game.setTurn(1)
                        break
                    else:
                        self.t.insert(tk.END, self._player2 + ": " + "Pass" + "\n")
                        self._game.setTurn(2)
                self._game.pushstack()

            if colour == 1:
                validmoves = self._game.getValidMoves(self._game.getBoard(), 2)
            else:
                validmoves = self._game.getValidMoves(self._game.getBoard(), 1)

            if self._game.getGamemode() == 2:
                self._game.pushstack()
                if len(validmoves) == 0:
                    self._game.setTurn(1)
                self._game.setTurn(1)

            self._root.update()
            self._root.update_idletasks()

            self.displayBoard(self._game_win)
            self.whitescore.config(text="White: " + str(self._game.getWhiteScore(self._game.getBoard())))
            self.blackscore.config(text="Black: " + str(self._game.getBlackScore(self._game.getBoard())))
            self.checkend()
            if self._game.getTurn() %2 == 1:
                self.indicator.config(text="Black's Turn")
            else:
                self.indicator.config(text="White's Turn")
        else:
            #messagebox.showinfo("Invalid Move", "Invalid Move")
            print("Invalid Move")
        
    
    def displayBoard(self, window):
        ratio = self.canvassize/8
        self.c.delete("all")
        for i in range(8):
            self.c.create_line(0, i*ratio, self.canvassize, i*ratio)
            self.c.create_line(i*ratio, 0, i*ratio, self.canvassize)
        #getting the borders of the board
        self.c.create_line(0, self.canvassize, self.canvassize, self.canvassize)
        self.c.create_line(0, 0, 0, self.canvassize)
        self.c.create_line(self.canvassize, 0, self.canvassize, self.canvassize)
        self.c.create_line(0, 0, self.canvassize, 0)

        #print all the pieces of the board onto the canvas
        board = self._game.getBoard()
        for row in range(8):
            for col in range(8):
                if board[row][col]:
                    if board[row][col] == 1:
                        self.c.create_oval(col*ratio, row*ratio, (col+1)*ratio, (row+1)*ratio, fill="black")
                    else:
                        self.c.create_oval(col*ratio, row*ratio, (col+1)*ratio, (row+1)*ratio, fill="white")

        #display valid moves
        if not self.isloaded:
            if self.validbutton.cget("text") == "Enabled":  
                if self._game.getTurn()%2 == 1: # black
                    validlocations = self._game.getValidMoves(board, 1)
                else:
                    validlocations = self._game.getValidMoves(board, 2)
                for location in validlocations:
                    self.c.create_oval(location[0][1]*ratio, location[0][0]*ratio, (location[0][1]+1)*ratio, (location[0][0]+1)*ratio, fill="grey")
            else:
                if self.pref:
                    if self.pref[4] == 1:
                        if self._game.getTurn()%2 == 1: # black
                            validlocations = self._game.getValidMoves(board, 1)
                        else:
                            validlocations = self._game.getValidMoves(board, 2)
                        for location in validlocations:
                            self.c.create_oval(location[0][1]*ratio, location[0][0]*ratio, (location[0][1]+1)*ratio, (location[0][0]+1)*ratio, fill="grey")

    def undo(self):
        #class A skill - stacks
        #class A skill - stack operations
        self._game.undo()
        if self._game.getTurn()%2 == 1:
            self.indicator.config(text="Black's Turn")
        else:
            self.indicator.config(text="White's Turn")
        
        if self._game.getGamemode() == 1:
            #self._game.setTurn(-1)
            self.undos += 1
        self.c.delete("all")
        self.t.insert(tk.END, "Undo\n")
        self.displayBoard(self._game_win)

    def options1(self):
        '''
        Displays the options for multiplayer
        Player 1:
        Player 2:
        Valid Moves:
        Board Colour:
        Next (button)
        '''
        newwindow = tk.Toplevel(self._root)
        newwindow.title("Options")
        newwindow.geometry("300x300")
        
        player1label = tk.Label(newwindow, text="Player 1: ")
        player1label.grid(row=0, column=0)
        self.player1entry = tk.Entry(newwindow, width = 60)
        self.player1entry.grid(row=0, column=1)

        player2label = tk.Label(newwindow, text="Player 2: ")
        player2label.grid(row=1, column=0)
        self.player2entry = tk.Entry(newwindow, width = 60)
        self.player2entry.grid(row=1, column=1)

        self.validlabel = tk.Label(newwindow, text="Valid Moves: ")
        self.validlabel.grid(row=2, column=0)
        self.validbutton = tk.Button(newwindow, text="Disabled", command=self.valids, bg="red")
        self.validbutton.grid(row=2, column=1, columnspan=2)

        self.boardcolourlabel = tk.Label(newwindow, text="Board Colour: ")
        self.boardcolourlabel.grid(row=3, column=0)
        self.boardcolourbutton = tk.Button(newwindow, text="dark green", command=self.boardcolour, bg="dark green")
        self.boardcolourbutton.grid(row=3, column=1, columnspan=2)

        nextbutton = tk.Button(newwindow, text="Next", command=lambda: self.play(2,0))
        nextbutton.grid(row=4, column=0, columnspan=2)

    def boardcolour(self):
        '''
        toggles the board colour button, to change the colour of the board in the game
        '''
        colours = ["dark green", "blue", "red", "yellow", "orange", "purple", "pink", "brown"]
        index = colours.index(self.boardcolourbutton.cget("text"))
        if index == len(colours)-1:
            index = 0
        else:
            index += 1
        
        self.boardcolourbutton.config(text=colours[index])
        self.boardcolourbutton.config(bg=colours[index])
        
    def options2(self):
        '''
        Displays the options for single player
        Player 1:
        Difficulty:
        Hints:
        Board Colour:
        Valid Moves:
        Next (button)
        '''
        option2 = tk.Toplevel(self._root)
        option2.title("Options")
        if not self.loggedin:
            option2.geometry("300x300")

            player1label = tk.Label(option2, text="Player 1: ")
            player1label.grid(row=0, column=0)
            self.player1entry = tk.Entry(option2, width = 60)
            self.player1entry.grid(row=0, column=1)

            difficultlabel = tk.Label(option2, text="Difficulty: ")
            difficultlabel.grid(row=1, column=0)
            self.difficultentry = tk.Entry(option2, width = 60)
            self.difficultentry.grid(row=1, column=1)

            self.validlabel = tk.Label(option2, text="Valid Moves: ")
            self.validlabel.grid(row=2, column=0)
            self.validbutton = tk.Button(option2, text="Disabled", command=self.valids, bg="red")
            self.validbutton.grid(row=2, column=1, columnspan=2)

            self.hintlabel = tk.Label(option2, text="Hint: ")
            self.hintlabel.grid(row=3, column=0)
            self.hintbutton = tk.Button(option2, text="Disabled", command=self.hints, bg="red")
            self.hintbutton.grid(row=3, column=1, columnspan=2)

            self.boardcolourlabel = tk.Label(option2, text="Board Colour: ")
            self.boardcolourlabel.grid(row=4, column=0)
            self.boardcolourbutton = tk.Button(option2, text="dark green", command=self.boardcolour, bg="dark green")
            self.boardcolourbutton.grid(row=4, column=1, columnspan=2)

            nextbutton = tk.Button(option2, text="Next", command=lambda: self.play(1,0))
            nextbutton.grid(row=5, column=0, columnspan=2)
        else:
            preferences = self.datams.getpreferences(self.user)
            pref1 = preferences[0]
            pref2 = preferences[1]
            pref3 = preferences[2]
            ### display first set of preferences

            pref1label = tk.Label(option2, text="Preference 1: ")
            pref1label.grid(row=0, column=0)
            
            difficulty1label = tk.Label(option2, text=f"Difficulty: {pref1[1]}")
            difficulty1label.grid(row=1, column=0)

            hints1label = tk.Label(option2, text=f"Hints: {pref1[2]}")
            hints1label.grid(row=2, column=0)

            boardcolour1label = tk.Label(option2, text=f"Board Colour: {pref1[3]}")
            boardcolour1label.grid(row=3, column=0)

            valids1label = tk.Label(option2, text=f"Valid Moves: {pref1[4]}")
            valids1label.grid(row=4, column=0)

            pref1choose = tk.Button(option2, text="Choose", command=lambda: self.choosepref(1))
            pref1choose.grid(row=5, column=0)

            ### display second set of preferences
            pref2label = tk.Label(option2, text="Preference 2: ")
            pref2label.grid(row=0, column=1)

            difficulty2label = tk.Label(option2, text=f"Difficulty: {pref2[1]}")
            difficulty2label.grid(row=1, column=1)

            hints2label = tk.Label(option2, text=f"Hints: {pref2[2]}")
            hints2label.grid(row=2, column=1)

            boardcolour2label = tk.Label(option2, text=f"Board Colour: {pref2[3]}")
            boardcolour2label.grid(row=3, column=1)

            valids2label = tk.Label(option2, text=f"Valid Moves: {pref2[4]}")
            valids2label.grid(row=4, column=1)

            pref2choose = tk.Button(option2, text="Choose", command=lambda: self.choosepref(2))
            pref2choose.grid(row=5, column=1)

            ### display third set of preferences
            pref3label = tk.Label(option2, text="Preference 3: ")
            pref3label.grid(row=0, column=2)

            difficulty3label = tk.Label(option2, text=f"Difficulty: {pref3[1]}")
            difficulty3label.grid(row=1, column=2)
            
            hints3label = tk.Label(option2, text=f"Hints: {pref3[2]}")
            hints3label.grid(row=2, column=2)

            boardcolour3label = tk.Label(option2, text=f"Board Colour: {pref3[3]}")
            boardcolour3label.grid(row=3, column=2)

            valids3label = tk.Label(option2, text=f"Valid Moves: {pref3[4]}")
            valids3label.grid(row=4, column=2)

            pref3choose = tk.Button(option2, text="Choose", command=lambda: self.choosepref(3))
            pref3choose.grid(row=5, column=2)

            ### display new preferences
            player1label = tk.Label(option2, text="Player 1: ")
            player1label.grid(row=0, column=3)
            self.player1entry = tk.Entry(option2, width = 60)
            self.player1entry.grid(row=0, column=4)

            difficultlabel = tk.Label(option2, text="Difficulty: ")
            difficultlabel.grid(row=1, column=3)
            self.difficultentry = tk.Entry(option2, width = 60)
            self.difficultentry.grid(row=1, column=4)

            self.validlabel = tk.Label(option2, text="Valid Moves: ")
            self.validlabel.grid(row=2, column=3)
            self.validbutton = tk.Button(option2, text="Disabled", command=self.valids, bg="red")
            self.validbutton.grid(row=2, column=4, columnspan=2)

            self.hintlabel = tk.Label(option2, text="Hint: ")
            self.hintlabel.grid(row=3, column=3)
            self.hintbutton = tk.Button(option2, text="Disabled", command=self.hints, bg="red")
            self.hintbutton.grid(row=3, column=4, columnspan=2)

            self.boardcolourlabel = tk.Label(option2, text="Board Colour: ")
            self.boardcolourlabel.grid(row=4, column=3)
            self.boardcolourbutton = tk.Button(option2, text="dark green", command=self.boardcolour, bg="dark green")
            self.boardcolourbutton.grid(row=4, column=4, columnspan=2)

            nextbutton = tk.Button(option2, text="Next", command=lambda: self.play(1,0))
            nextbutton.grid(row=5, column=3, columnspan=2)

    def choosepref(self, prefno):
        '''
        chooses the preference that the user has chosen
        '''
        preferences = self.datams.getpreferences(self.user)
        self.pref = preferences[prefno-1]  
        self.play(1,0)    

    def valids(self):
        '''
        toggles the valid moves button, to display the valid moves in the game
        '''
        if self.validbutton.cget("text") == "Disabled":
            self.validbutton.config(text="Enabled", bg="green")
        else:
            self.validbutton.config(text="Disabled", bg="red")

    def hints(self):
        '''
        toggles the hint button, to display the hint in the game
        '''
        if self.hintbutton.cget("text") == "Disabled":
            self.hintbutton.config(text="Enabled", bg="green")
        else:
            self.hintbutton.config(text="Disabled", bg="red")
    
    def checkend(self):
        '''
        checks whether the game is over, and updates allthe databases accordingly
        '''
        if self._game.checkgameover(self._game.getBoard()):
            if self._game.getGamemode() == 1:
                if not self.loggedin:
                    self.displayBoard(self._game_win)
                    self.gameClose()
                    game_win = None
                    if self._game.getBlackScore(self._game.getBoard()) > self._game.getWhiteScore(self._game.getBoard()):
                        messagebox.showinfo("Game Over", "Player 1 Wins")
                    elif self._game.getBlackScore(self._game.getBoard()) < self._game.getWhiteScore(self._game.getBoard()):
                        messagebox.showinfo("Game Over", "Computer Wins")
                    else:
                        messagebox.showinfo("Game Over", "Tie")
                else:
                    self.displayBoard(self._game_win)
                    self.gameClose()
                    if self._game.getBlackScore(self._game.getBoard()) > self._game.getWhiteScore(self._game.getBoard()):
                        stats = self.datams.getstatistics(self.user)
                        print(stats)
                        newscore = stats[0][3] + self.calcScorew()
                        self.datams.editstatistics(self.user, "wins", stats[0][1]+1)
                        self.datams.editstatistics(self.user, "score", newscore)
                        messagebox.showinfo("Game Over", "Player 1 Wins")
                    elif self._game.getBlackScore(self._game.getBoard()) < self._game.getWhiteScore(self._game.getBoard()):
                        stats = self.datams.getstatistics(self.user)
                        newscore = stats[0][3] + self.calcScorel()
                        print(newscore)
                        self.datams.editstatistics(self.user, "loss", stats[0][2]+1)
                        self.datams.editstatistics(self.user, "score", newscore)
                        messagebox.showinfo("Game Over", "Computer Wins")
                    else:
                        messagebox.showinfo("Game Over", "Tie")
            elif self._game.getGamemode() == 2:
                self.displayBoard(self._game_win)
                self.gameClose()
                if self._game.getBlackScore(self._game.getBoard()) > self._game.getWhiteScore(self._game.getBoard()):
                    messagebox.showinfo("Game Over", "Black Wins")
                elif self._game.getBlackScore(self._game.getBoard()) < self._game.getWhiteScore(self._game.getBoard()):
                    messagebox.showinfo("Game Over", "White Wins")
                else:
                    messagebox.showinfo("Game Over", "Tie")
            return True
        
        return False

    def givehint(self):
        #play the game from the player's perspective using minimax
        if self._game.getTurn() % 2 == 1:

            #unbind all the buttons and canvas
            self.c.unbind("<Button-1>")
            self.u.config(state=tk.DISABLED)
            self.savebutton.config(state=tk.DISABLED)
            self.quitbutton.config(state=tk.DISABLED)
            self.hintbutton.config(state=tk.DISABLED)
            self._root.update()
            self._root.update_idletasks()

            hintmove, score = self._game.minimax(self._game.getBoard(), 5, True, 1, -100000, 100000)
            
            #rebind all the buttons and canvas
            self.c.bind("<Button-1>", self.move)
            self.u.config(state=tk.NORMAL)
            self.savebutton.config(state=tk.NORMAL)
            self.quitbutton.config(state=tk.NORMAL)
            self.hintbutton.config(state=tk.NORMAL)
            self._root.update()
            self._root.update_idletasks()

            #display the hint
            ratio = self.canvassize/8
            self.c.create_oval(hintmove[0][1]*ratio, hintmove[0][0]*ratio, (hintmove[0][1]+1)*ratio, (hintmove[0][0]+1)*ratio, fill="yellow")
            self.hint += 1
            #force the update
            self._root.update()
            self._root.update_idletasks()

    def saveGame(self):
        '''
        saves the game to a file
        '''
        savewindow = tk.Toplevel(self._game_win)
        savewindow.title("Save Game")
        savewindow.geometry("300x300")
        
        savenumberlabel = tk.Label(savewindow, text="Save Number: ")
        savenumberlabel.grid(row=0, column=0)
        self.savenumberentry = tk.Entry(savewindow, width = 60)
        self.savenumberentry.grid(row=0, column=1)

        savebutton = tk.Button(savewindow, text="Save", command=self.save)
        savebutton.grid(row=1, column=0, columnspan=2)
        
    def save(self):
        '''
        saves the game to a file
        '''
        try:
            savenumber = int(self.savenumberentry.get())
        except:
            messagebox.showinfo("Invalid Save Number", "Invalid Save Number")
        self._game.saveGame(savenumber)

    def loadGame(self):
        '''
        loads the game from a file
        '''
        loadwindow = tk.Toplevel(self._game_win)
        loadwindow.title("Load Game")
        loadwindow.geometry("300x300")
        
        loadnumberlabel = tk.Label(loadwindow, text="Load Number: ")
        loadnumberlabel.grid(row=0, column=0)
        self.loadnumberentry = tk.Entry(loadwindow, width = 60)
        self.loadnumberentry.grid(row=0, column=1)

        loadbutton = tk.Button(loadwindow, text="Load", command=self.load)
        loadbutton.grid(row=1, column=0, columnspan=2)
    
    def load(self):
        '''
        loads the game from a file
        '''
        try:
            loadnumber = int(self.loadnumberentry.get())
        except:
            messagebox.showinfo("Invalid Load Number", "Invalid Load Number")

        self.play(0, loadnumber)

    def calcScorew(self):
        '''
        if the user wins, a score is calculated
        score = pieces(friendly) - pieces(enemy) + turn + 2(difficulty) - undos - hints'''
        score = 0
        for row in range(8):
            for col in range(8):
                if self._game.getBoard()[row][col] == 1:
                    score += 1
                elif self._game.getBoard()[row][col] == 2:
                    score -= 1
        #factor in the turn
        score += self._game.getTurn()

        #factor in the difficulty
        score += (self._game.getDifficulty()*2)

        #factor in the number of undos
        score -= self.undos

        #factor in the number of hints
        score -= self.hint

        if score < 0:
            score = 0
        return score

    def calcScorel(self):
        '''
        if the user loses, a score is calculated
        score = - pieces(enemy) - turn + 2(difficulty) + undos + hints
        '''
        score = 0
        for row in range(8):
            for col in range(8):
                if self._game.getBoard()[row][col] == 2:
                    score -= 1
        #factor in the turn
        score -= self._game.getTurn()

        #factor in the difficulty
        score += (self._game.getDifficulty()*2)

        #factor in the number of undos
        score -= self.undos

        #factor in the number of hints
        score -= self.hint
        print(score)
        if score > 0:
            score = 0
        return score
    
    def run(self):
        self._root.mainloop()

    def gameClose(self):
        self._game_win.quit()