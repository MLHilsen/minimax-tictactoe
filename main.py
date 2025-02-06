import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI():
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = Board()  # Your Board class
        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.pack()
        self.draw_board()

        # Initialize players
        self.player1 = Player('X') # Human player
        self.player2 = AIPlayer('O') # AI player

        # Bind mouse click to handle_click method
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        # Draw the Tic-Tac-Toe grid
        for i in range(1, 3):
            self.canvas.create_line(i * 100, 0, i * 100, 300, fill="black")  # Vertical lines
            self.canvas.create_line(0, i * 100, 300, i * 100, fill="black")  # Horizontal lines

    def draw_symbol(self, row, col, symbol):
        # Draw 'X' or 'O' at the specified cell
        x = col * 100 + 50
        y = row * 100 + 50
        if symbol == 'X':
            self.canvas.create_line(x - 30, y - 30, x + 30, y + 30, fill="blue", width=2)
            self.canvas.create_line(x + 30, y - 30, x - 30, y + 30, fill="blue", width=2)
        elif symbol == 'O':
            self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, outline="red", width=2)

    def handle_click(self, event):
        # Convert mouse coordinates to grid position
        col = event.x // 100
        row = event.y // 100

        # Human player's move
        if self.board.make_move((row, col), self.player1.symbol):
            self.draw_symbol(row, col, self.player1.symbol)
            if self.board.check_winner():
                messagebox.showinfo("Game Over", "You win!")
                self.reset_game()
            elif self.board.is_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                # AI's move
                ai_move = self.player2.get_move(self.board)
                if ai_move:
                    self.board.make_move(ai_move, self.player2.symbol)
                    self.draw_symbol(ai_move[0], ai_move[1], self.player2.symbol)
                    if self.board.check_winner():
                        messagebox.showinfo("Game Over", "AI wins!")
                        self.reset_game()
                    elif self.board.is_full():
                        messagebox.showinfo("Game Over", "It's a draw!")
                        self.reset_game()

    def reset_game(self):
        # Reset the board and canvas
        self.board = Board()
        self.canvas.delete("all")
        self.draw_board()
        

class Board:
    def __init__(self):
        # Initialize the board state
        self.state = ['','','',
                      '','','',
                      '','','',]

    def display(self):
        for i in range(0, 9, 3):
            print(f"{self.state[i]} | {self.state[i + 1]} | {self.state[i + 2]}")
            if i < 6:
                print("---------")

    def is_full(self):
        # Check if the board is full
        return not ('' in set(self.state))

    def check_winner(self):
    # Check rows
        for i in range(0, 9, 3):
            if self.state[i] == self.state[i + 1] == self.state[i + 2] and self.state[i] != '':
                return self.state[i]  # Return the winning symbol

        # Check columns
        for i in range(3):
            if self.state[i] == self.state[i + 3] == self.state[i + 6] and self.state[i] != '':
                return self.state[i]  # Return the winning symbol

        # Check diagonals
        if self.state[0] == self.state[4] == self.state[8] and self.state[0] != '':
            return self.state[0]  # Return the winning symbol
        if self.state[2] == self.state[4] == self.state[6] and self.state[2] != '':
            return self.state[2]  # Return the winning symbol

        return None  # No winner

    def make_move(self, position, player):
        # Update the board with a move
        if self.state[position] == '':
            self.state[position] = player
            return True
        return False

    def undo_move(self, position):
        # Revert a move
        self.state[position] = ''

    def get_cell_center(self, row, col):
        # Assuming each cell is 100x100 pixels
        x = col * 100 + 50
        y = row * 100 + 50
        return x, y


class Player:
    def __init__(self, symbol):
        # Initialize player symbol
        self.symbol = "X"

    def get_move(self, board):
        # Get the player's move
        pass


class AIPlayer(Player):
    def minimax(self, board, depth, is_maximizing):
        # Implement the Minimax algorithm
        self.symbol = "O"
        pass

    def get_move(self, board):
        # Use Minimax to determine the best move
        pass


def evaluate(board):
    # Evaluate the board state
    pass


def get_available_moves(board):
    # Get available moves
    pass


def play_game():
    # Main game loop
    pass


# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()