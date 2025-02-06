import tkinter as tk
from tkinter import messagebox

class Board:
    def __init__(self):
        # Initialize the board state
        self.state = ['', '', '',
                      '', '', '',
                      '', '', '']

    def is_full(self):
        # Check if the board is full
        return '' not in self.state

    def check_winner(self):
        # Check for a winner
        # Rows
        for i in range(0, 9, 3):
            if self.state[i] == self.state[i + 1] == self.state[i + 2] and self.state[i] != '':
                return self.state[i]  # Return the winning symbol ('X' or 'O')

        # Columns
        for i in range(3):
            if self.state[i] == self.state[i + 3] == self.state[i + 6] and self.state[i] != '':
                return self.state[i]  # Return the winning symbol ('X' or 'O')

        # Diagonals
        if self.state[0] == self.state[4] == self.state[8] and self.state[0] != '':
            return self.state[0]  # Return the winning symbol ('X' or 'O')
        if self.state[2] == self.state[4] == self.state[6] and self.state[2] != '':
            return self.state[2]  # Return the winning symbol ('X' or 'O')

        return None  # No winner

    def make_move(self, position, player):
        # Update the board with a move
        if self.state[position] == '':
            self.state[position] = player
            return True  # Move successful
        return False  # Move invalid (position already occupied)

    def undo_move(self, position):
        # Revert a move
        self.state[position] = ''

    def get_cell_center(self, row, col):
        # Get center coordinates of a given cell
        x = col * 100 + 50
        y = row * 100 + 50
        return x, y
    
    def get_available_moves(self):
        moves = []
        for index, symbol in enumerate(self.state):
            if symbol == '':
                moves.append(index)
        return moves


class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        # Human player's move (handled by GUI)
        pass


class AIPlayer:
    def __init__(self, symbol):
        self.symbol = symbol  # AI's symbol ('X' or 'O')

    def minimax(self, board, depth, is_maximizing):
        """
        Minimax algorithm to determine the best move for the AI.
        :param board: The current board state.
        :param depth: The depth of the recursion (used to prioritize faster wins).
        :param is_maximizing: True if it's the AI's turn, False if it's the human's turn.
        :return: The best score for the current board state.
        """
        # Base cases: check if the game is over
        winner = board.check_winner()
        if winner == self.symbol:  # AI wins
            return 10 - depth
        elif winner is not None:  # Human wins
            return depth - 10
        elif board.is_full():  # Draw
            return 0

        # Recursive case
        if is_maximizing:
            best_score = -float('inf')  # Initialize to worst possible score for maximizing player
            for move in board.get_available_moves():
                board.make_move(move, self.symbol)  # Simulate AI's move
                score = self.minimax(board, depth + 1, False)  # Recursively evaluate human's turn
                board.undo_move(move)  # Undo the move
                best_score = max(score, best_score)  # Update best score
            return best_score
        else:
            best_score = float('inf')  # Initialize to worst possible score for minimizing player
            for move in board.get_available_moves():
                board.make_move(move, self.get_opponent_symbol())  # Simulate human's move
                score = self.minimax(board, depth + 1, True)  # Recursively evaluate AI's turn
                board.undo_move(move)  # Undo the move
                best_score = min(score, best_score)  # Update best score
            return best_score

    def get_move(self, board):
        """
        Determines the best move for the AI using the Minimax algorithm.
        :param board: The current board state.
        :return: The best move (index of the cell).
        """
        best_move = None
        best_score = -float('inf')
        for move in board.get_available_moves():
            board.make_move(move, self.symbol)  # Simulate AI's move
            score = self.minimax(board, 0, False)  # Evaluate the move
            board.undo_move(move)  # Undo the move
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def get_opponent_symbol(self):
        """
        Returns the symbol of the opponent.
        :return: 'X' if AI is 'O', 'O' if AI is 'X'.
        """
        return 'X' if self.symbol == 'O' else 'O'


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")

        # Initialize the board and players
        self.board = Board()
        self.player1 = Player('X')  # Human player
        self.player2 = AIPlayer('O')  # AI player

        # Create a canvas for the game board
        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.pack()

        # Draw the initial board
        self.draw_board()

        # Bind mouse click to handle_click method
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        # Draw the Tic-Tac-Toe grid
        for i in range(1, 3):
            self.canvas.create_line(i * 100, 0, i * 100, 300, fill="black")  # Vertical lines
            self.canvas.create_line(0, i * 100, 300, i * 100, fill="black")  # Horizontal lines

    def draw_symbol(self, row, col, symbol):
        # Draw 'X' or 'O' at the specified cell
        x, y = self.board.get_cell_center(row, col)
        if symbol == 'X':
            self.canvas.create_line(x - 30, y - 30, x + 30, y + 30, fill="blue", width=2)
            self.canvas.create_line(x + 30, y - 30, x - 30, y + 30, fill="blue", width=2)
        elif symbol == 'O':
            self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, outline="red", width=2)
        self.canvas.update()

    def handle_click(self, event):
        # Convert mouse coordinates to grid position
        col = event.x // 100
        row = event.y // 100
        position = row * 3 + col

        # Human player's move
        if self.board.make_move(position, self.player1.symbol):
            self.draw_symbol(row, col, self.player1.symbol)
            winner = self.board.check_winner()
            if winner:
                messagebox.showinfo("Game Over", f"{winner} wins!")
                self.reset_game()
            elif self.board.is_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                # AI's move
                ai_move = self.player2.get_move(self.board)
                if ai_move is not None:
                    ai_row, ai_col = ai_move // 3, ai_move % 3
                    self.board.make_move(ai_move, self.player2.symbol)
                    self.draw_symbol(ai_row, ai_col, self.player2.symbol)
                    winner = self.board.check_winner()
                    if winner:
                        messagebox.showinfo("Game Over", f"{winner} wins!")
                        self.reset_game()
                    elif self.board.is_full():
                        messagebox.showinfo("Game Over", "It's a draw!")
                        self.reset_game()

    def reset_game(self):
        # Reset the board and canvas
        self.board = Board()
        self.canvas.delete("all")
        self.draw_board()


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()