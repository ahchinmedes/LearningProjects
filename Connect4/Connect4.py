import json
import os
import datetime
from colorama import Fore

def print_welcome():
    print(Fore.LIGHTCYAN_EX)
    print("----------------------")
    print("Welcome to Connect 4! ")
    print("----------------------")
    print(Fore.LIGHTYELLOW_EX)

def log(msg):
    # Logging message throughout the status of game with timestamp in front
    folder = os.path.dirname(__file__)
    file = os.path.join(folder, "c4_log.txt")
    time_text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file, 'a') as fout:
        fout.write(f'{time_text}: {msg} \n')

def write_leaderboard():
    """
    TODO: Record winner into a leaderboard file to document the win and increase the
    number of wins for the player if he is in the leaderboard previously.
    :return:
    """

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
            # Print error if trying to drop piece into top row and it's already filled
            print('This column is fully filled. Please choose another column.')
            break
    return board


def check4(rows, symbol):
    """
    TODO: Implement the check
    :param rows:
    :param symbol:
    :return: TRUE or FALSE
    """
    # This function is to check for 4 consecutive piece of the same symbol


def check_winner(board, symbol):
    # This function checks for a winner. Returns true if there's a winner
    """
    TODO: Implement checking winning combination
    """

    return False


def main():
    print_welcome()
    players = ['Chin', 'Computer']
    symbols = ['X', 'O']
    active_player_index = 0
    last_player = active_player_index
    log(f'It is {last_player}\'s turn')

    # Create an empty board
    board = create_board()
    log('Board created')

    while not check_winner(board, symbols[last_player]):
        while True:
            try:
                column = int(input(f'It is {players[active_player_index]}\'s turn! Choose your column to drop your piece!: '))
                if column < 8:
                    break  # Exit the loop if the input is valid and less than 7
                else:
                    print(Fore.RED + "Please enter a number less than 7.")
                    print(Fore.LIGHTYELLOW_EX)
            except ValueError:
                print(Fore.RED + "Invalid input! Please enter an integer.")
                print(Fore.LIGHTYELLOW_EX)

        board = drop_piece(board, symbols[active_player_index],column)
        log(f'{players[active_player_index]} choose to drop piece at column {column}')

        print_board(board)

        # Store player index for checking wins before changing player
        last_player = active_player_index

        # Change player
        active_player_index = (active_player_index + 1) % len(players)

    print(f'Player {players[last_player]} wins!')
    log(f'Player {players[last_player]} wins!')

if __name__ == '__main__':
    main()

