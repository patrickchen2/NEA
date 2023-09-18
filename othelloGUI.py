import tkinter as tk
from abc import ABC, abstractmethod
from othello import Othello
from player import Player

class UI(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError
    
class GUI(UI):
    def __init__(self):
        self.timerentry = -1
        self.help_win = None
        self._game_win = None
        root = tk.Tk()
        root.title("Othello")
        frame = tk.Frame(root)
        frame.pack()

        tk.Button(frame, text="Play", command=self.options).pack(fill=tk.X)
        tk.Button(frame, text="Quit", command=root.quit).pack(fill=tk.X)

        scroll = tk.Scrollbar(frame)
        console = tk.Text(frame, height=4, width=50)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        console.pack(side=tk.LEFT, fill=tk.Y)

        scroll.config(command=console.yview)
        console.config(yscrollcommand=scroll.set)

        self._root = root
        self._console = console
    
    def play(self):
        if self._game_win:
            return
        self._timer = self.timerentry.get()
        self._player1 = self.player1entry.get()
        self._player2 = self.player2entry.get()

        self._game = Othello(self._player1, self._player2, self._timer, 1)
        self._finished = False

        game_win = tk.Toplevel(self._root)
        game_win.title("Othello")
        #game_win.geometry("500x500")
        frame = tk.Frame(game_win)

        tk.Grid.rowconfigure(game_win, 0, weight=1)
        tk.Grid.columnconfigure(game_win, 0, weight=1)
        frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        c = tk.Canvas(game_win, width=500, height=500, bg="dark green")
        c.grid(row = 0, column = 0, padx= 5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

        ratio = 500/8
        for i in range(8):
            c.create_line(0, i*ratio, 500, i*ratio)
            c.create_line(i*ratio, 0, i*ratio, 500)

        c.create_oval(3*ratio, 3*ratio, 4*ratio, 4*ratio, fill="white")
        c.create_oval(3*ratio, 4*ratio, 4*ratio, 5*ratio, fill="black")
        c.create_oval(4*ratio, 3*ratio, 5*ratio, 4*ratio, fill="black")
        c.create_oval(4*ratio, 4*ratio, 5*ratio, 5*ratio, fill="white")
        c.bind("<Button-1>", self.move)

        

    def gameClose(self):
        self._game_win.destroy()
        self._game_win = None

    def move(self, row, col, event):
        if self._game.getTurn()%2 == 1:
            colour = 1
        else:
            colour = 2
        x,y = event.x, event.y
        ratio = 500/8
        # finding the nearest whole ratio for x and y
        x = int(x//ratio)
        y = int(y//ratio)
        self._game.playGame(self._game.getTurn(), x, y, )

    def run(self):
        self._root.mainloop()

    def options(self):
        newwindow = tk.Toplevel(self._root)
        newwindow.title("Options")
        newwindow.geometry("300x300")
        
        player1label = tk.Label(newwindow, text="Player 1: ")
        player1label.pack()
        self.player1entry = tk.Entry(newwindow, width = 60)
        self.player1entry.pack()

        player2label = tk.Label(newwindow, text="Player 2: ")
        player2label.pack()
        self.player2entry = tk.Entry(newwindow, width = 60)
        self.player2entry.pack()
        
        timerlabel = tk.Label(newwindow, text="timer (-1): ")
        timerlabel.pack()
        self.timerentry = tk.Entry(newwindow, width = 60)
        self.timerentry.pack()

        nextbutton = tk.Button(newwindow, text="Next", command=self.play)
        nextbutton.pack()
        #timerlabel.grid(row=0, column=0)
        #timerentry.grid(row=0, column=1)
        #nextbutton.grid(row=1, column=0, columnspan=2)

        



ui = GUI()
ui.run()