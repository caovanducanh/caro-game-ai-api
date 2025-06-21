import random

def get_empty_positions(board):
    return [(i, j) for i, row in enumerate(board) for j, cell in enumerate(row) if cell == ""]

def get_best_move(board, player, difficulty="medium"):
    empty = get_empty_positions(board)
    if not empty:
        return None

    if difficulty == "easy":
        return random.choice(empty)
    elif difficulty == "medium":
        for i, j in empty:
            board[i][j] = player
            if check_win(board, player):
                board[i][j] = ""
                return (i, j)
            board[i][j] = ""
        opponent = "O" if player == "X" else "X"
        for i, j in empty:
            board[i][j] = opponent
            if check_win(board, opponent):
                board[i][j] = ""
                return (i, j)
            board[i][j] = ""
        return random.choice(empty)
    else:
        return random.choice(empty)

def check_win(board, player):
    n = len(board)
    for i in range(n):
        if all(board[i][j] == player for j in range(n)):
            return True
        if all(board[j][i] == player for j in range(n)):
            return True
    if all(board[i][i] == player for i in range(n)):
        return True
    if all(board[i][n-1-i] == player for i in range(n)):
        return True
    return False 