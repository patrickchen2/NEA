import tkinter as tk
from abc import ABC, abstractmethod
from othello import Othello

class UI(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError
    
class GUI(UI):
    def __init__(self):
        self.help_win = None
        self._game_win = None
        root = tk.Tk()
        root.title("Othello")
        frame = tk.Frame(root)
        frame.pack()

        tk.Button(frame, text="Play", command=self.play).pack(fill=tk.X)
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
        
        self._game = Othello()
        self._finished = False

        game_win = tk.Toplevel(self._root)
        game_win.title("Othello")
        frame = tk.Frame(game_win)

        tk.Grid.rowconfigure(game_win, 0, weight=1)
        tk.Grid.columnconfigure(game_win, 0, weight=1)
        frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self._buttons = [[None for _ in range(8)] for  _ in range(8)]

        for row in range(8):
            for col in range(8):
                b = tk.StringVar()
                b.set(self._game.getPieceAt(row, col))

                cmd = lambda r=row, c=col: self._move(r, c)