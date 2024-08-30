def create_board():
    # Create a 6x7 Connect 4 board and initialise with None value
    board = [[None for _ in range(7)] for _ in range(6)]
    return board

def print_board(board):
    for row in board:
        print("| ", end="")
        for cell in row:
            print('-' if cell is None else cell, end=" | ")
        print()


def drop_piece(board, symbol, column):
    # This function sets the bottom row with player's symbol.
    for rows in range(5,-1,-1):
        if board[rows][column-1] == None:
            board[rows][column-1] = symbol
            break
        if rows == 0:
            # Print error if trying to drop piece into top row
            print('This column is fully filled. Please choose another column.')
            break
    return board


def check_winner(board):
    # This function checks for a winner. Returns true if there's a winner
    """
    TODO: Implement checking winning combination
    """
    return False


def main():
    print('Welcome to Connect 4!')
    players = ['Chin', 'Computer']
    symbols = ['X', 'O']
    active_player_index = 0
    # Create an empty board
    board = create_board()

    while not check_winner(board):
        while True:
            try:
                column = int(
                    input(f"It is {players[active_player_index]}'s turn! Choose your column to drop your piece!: "))
                if column < 8:
                    break  # Exit the loop if the input is valid and less than 7
                else:
                    print("Please enter a number less than 7.")
            except ValueError:
                print("Invalid input! Please enter an integer.")
        board = drop_piece(board, symbols[active_player_index],column)
        print_board(board)

        # Change player
        active_player_index = (active_player_index + 1) % len(players)
        input('Paused')

if __name__ == '__main__':
    main()

