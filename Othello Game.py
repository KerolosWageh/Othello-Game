import tkinter as tk
import copy
from tkinter import messagebox

class Othello:
    def __init__(self, depth):
        if depth is None:
            depth = 0  # Default depth for human vs human mode
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'W'
        self.board[4][4] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.current_player = 'B'
        self.game_over = False
        self.depth = depth  # Depth for Alpha-Beta Pruning
        self.disk_count = {'B': 30, 'W': 30}  # Number of disks each player has

    def is_valid_move(self, row, col):
        if not (0 <= row < 8) or not (0 <= col < 8) or self.board[row][col] != ' ':
            return False
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Only horizontal and vertical directions
        opponent_color = 'W' if self.current_player == 'B' else 'B'
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent_color:
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent_color:
                    r, c = r + dr, c + dc
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                    return True
        return False

    def make_move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            self.flip_disks(row, col)
            self.disk_count[self.current_player] -= 1  # Decrement disk count for current player
            self.current_player = 'W' if self.current_player == 'B' else 'B'
            if not self.get_valid_moves(self.current_player):  # Check if current player has no valid moves
                self.current_player = 'W' if self.current_player == 'B' else 'B'  # Switch back to previous player
                if not self.get_valid_moves(self.current_player):  # Check if previous player also has no valid moves
                    self.game_over = True

    def flip_disks(self, row, col):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        opponent_color = 'W' if self.current_player == 'B' else 'B'
        for dr, dc in directions:
            r, c = row + dr, col + dc
            to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent_color:
                to_flip.append((r, c))
                r, c = r + dr, c + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                for flip_row, flip_col in to_flip:
                    self.board[flip_row][flip_col] = self.current_player

    def get_valid_moves(self, color):
        valid_moves = []
        for r in range(8):
            for c in range(8):
                if self.is_valid_move(r, c):
                    valid_moves.append((r, c))
        return valid_moves

    def is_game_over(self):
        valid_moves_black = self.get_valid_moves('B')
        valid_moves_white = self.get_valid_moves('W')
        if len(valid_moves_black) == 0 and len(valid_moves_white) == 0:  # Check if no valid moves for either player
            return True
        else:
            return False

    def get_winner(self):
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        if black_count > white_count:
            return 'Black'
        elif white_count > black_count:
            return 'White'
        else:
            return 'Draw'

    def calculate_score(self):
        black_score = sum(row.count('B') for row in self.board)
        white_score = sum(row.count('W') for row in self.board)
        return black_score, white_score

    def Alpha_Beta_Search(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_game_over():
            return self.evaluate(), None

        valid_moves = self.get_valid_moves(self.current_player)
        if maximizing_player:
            value = float('-inf')
            best_move = None
            for move in valid_moves:
                temp_board = copy.deepcopy(self)
                temp_board.make_move(move[0], move[1])
                new_value, _ = temp_board.Alpha_Beta_Search(depth - 1, alpha, beta, False)
                if new_value > value:
                    value = new_value
                    best_move = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_move
        else:
            value = float('inf')
            best_move = None
            for move in valid_moves:
                temp_board = copy.deepcopy(self)
                temp_board.make_move(move[0], move[1])
                new_value, _ = temp_board.Alpha_Beta_Search(depth - 1, alpha, beta, True)
                if new_value < value:
                    value = new_value
                    best_move = move
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value, best_move

    def evaluate(self):
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        return black_count - white_count  # Simple evaluation function

    def make_computer_move(self):
        if not self.game_over:
            value, best_move = self.Alpha_Beta_Search(self.depth, float('-inf'), float('inf'), True)
            if best_move:
                self.make_move(best_move[0], best_move[1])



class Gui:
    def __init__(self, root_custom):
        self.root_custom = root_custom
        self.game = None
        self.create_widgets()

    def create_widgets(self):
        self.root_custom.geometry("500x500")  # window size
        self.root_custom.configure(bg="blue")  # background color

        # Title label
        tk.Label(self.root_custom, text="Othello Game", font=("Arial", 24), fg="white", bg="#1e272e").pack(pady=20)

        # Difficulty level selection buttons
        tk.Label(self.root_custom, text="Select difficulty level:", font=("Times New Roman", 18)).pack()
        tk.Button(self.root_custom, text="Play with Friend", command=lambda: self.start_game(None), font=("Times New Roman", 18)).pack()
        tk.Button(self.root_custom, text="Bott-Depth 1", command=lambda: self.start_game(1), font=("Times New Roman", 18)).pack()
        tk.Button(self.root_custom, text="Medium-Depth 3", command=lambda: self.start_game(3), font=("Times New Roman", 18)).pack()
        tk.Button(self.root_custom, text="Hard-Depth 5", command=lambda: self.start_game(5), font=("Times New Roman", 18)).pack()

    def start_game(self, depth):
        self.game = Othello(depth)
        self.create_game_widgets()
        self.update_board()
        if depth == 5: 
            self.game.make_computer_move()
            self.update_board()

    def create_game_widgets(self):
        for widget in self.root_custom.pack_slaves():
            widget.pack_forget()  # Remove previous widgets
        self.canvas = tk.Canvas(self.root_custom, width=400, height=400 )
        self.canvas.pack()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.make_move)  # Bind left mouse click to make_move method
        self.disk_counter_label = tk.Label(self.root_custom, text="Disk Count: Black - 30, White - 30", font=("Times New Roman", 18))
        self.disk_counter_label.pack()
        self.score_label = tk.Label(self.root_custom, text="Score:", font=("Times New Roman", 18))
        self.score_label.pack()

    def draw_board(self):
        for r in range(8):
            for c in range(8):
                x0, y0 = c * 50, r * 50
                x1, y1 = x0 + 50, y0 + 50
                if (r, c) in self.game.get_valid_moves(self.game.current_player):
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="light blue", outline="black")
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="green", outline="black")
                if self.game.board[r][c] == 'B':
                    self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="black", outline="black")
                elif self.game.board[r][c] == 'W':
                    self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="white", outline="black")

    def update_board(self):
        self.canvas.delete("all")
        self.draw_board()
        self.disk_counter_label.config(text=f"Disk Count: Black - {self.game.disk_count['B']}, White - {self.game.disk_count['W']}")
        black_score, white_score = self.game.calculate_score()
        self.score_label.config(text=f"Score: Black - {black_score}, White - {white_score}")

    def make_move(self, event):
        if not self.game.game_over:
            x, y = event.x, event.y
            row, col = y // 50, x // 50

            if self.game.is_valid_move(row, col):
                self.game.make_move(row, col)
                self.update_board()
                black_score, white_score = self.game.calculate_score()
                print(f"Black Score: {black_score}, White Score: {white_score}")
                if self.game.game_over:
                    self.end_game()
                else:
                    self.game.make_computer_move()  # Make the computer move after human player's valid move
                    self.update_board()
                    black_score, white_score = self.game.calculate_score()
                    print(f"Black Score: {black_score}, White Score: {white_score}")
                    if not self.game.get_valid_moves(self.game.current_player):  # Check if current player has no valid moves
                        self.game.current_player = 'W' if self.game.current_player == 'B' else 'B'  # Switch to next player
                        self.game.make_computer_move()
                        self.update_board()
                        black_score, white_score = self.game.calculate_score()
                        print(f"Black Score: {black_score}, White Score: {white_score}")
                        if not self.game.get_valid_moves(self.game.current_player):  # Check again after computer move
                            self.game.current_player = 'W' if self.game.current_player == 'B' else 'B'  # Switch back to previous player
                            self.game.game_over = True
                            self.end_game()
            else:
                print("Invalid move! Please try again.")

    def end_game(self):
        black_score, white_score = self.game.calculate_score()
        winner = self.game.get_winner()
        if winner:
            messagebox.showinfo("Game Over", f"Winner: {winner} (Black: {black_score}, White: {white_score})")

if __name__ == "__main__":
    root_custom = tk.Tk()
    root_custom.title("Othello Game")
    app = Gui(root_custom)
    root_custom.mainloop()
    