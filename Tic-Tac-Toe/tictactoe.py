import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

def get_empty_cells(board):
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                empty_cells.append((i, j))
    return empty_cells

def make_move(board, cell, player):
    board[cell[0]][cell[1]] = player

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    current_player = 0

    for _ in range(9):
        print_board(board)
        if current_player == 0:
            row = int(input("Enter the row (0-2): "))
            col = int(input("Enter the column (0-2): "))
            if board[row][col] != " ":
                print("Cell already taken! Try again.")
                continue
            make_move(board, (row, col), players[current_player])
        else:
            empty_cells = get_empty_cells(board)
            move = random.choice(empty_cells)
            make_move(board, move, players[current_player])
            print(f"AI chose cell: {move}")

        if check_winner(board, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} wins!")
            return

        current_player = 1 - current_player

    print_board(board)
    print("It's a draw!")

if __name__ == "__main__":
    main()
