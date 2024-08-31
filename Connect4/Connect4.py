import json
import os
import datetime
import sys
from tabnanny import check

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
    # This function sets the lowest valid row with player's symbol.
    # Returns board status and the row selected for checking of winning sequence
    selected_row = 999
    for rows in range(5,-1,-1):
        if board[rows][column] == None:
            board[rows][column] = symbol
            selected_row = rows
            break
        elif rows == 0:
            # Print error if trying to drop piece into top row and it's already filled
            print('This column is fully filled. Please choose another column.')
            break

    return board, selected_row


def check4(row, col, dir_row, dir_col, board, symbol):
    # This function is to check for 4 consecutive piece of the same symbol. Returns True if check pass
    # print(f'Checking 4 consecutively {symbol}: {dir_row}:{dir_col}')
    for i in range(1, 4):
        # Calculate new position
        new_row = row + i * dir_row
        new_col = col + i * dir_col

        # Check if the new position is out of bounds
        if new_row < 0 or new_row >= len(board) or new_col < 0 or new_col >= len(board[0]):
     #       print(f'Out of bounds - Position ({new_row}, {new_col})')
            return False

        # Check if the symbol matches
        if board[new_row][new_col] != symbol:
      #      print(f'Wrong symbol at ({new_row}, {new_col}): found {board[new_row][new_col]}, expected {symbol}')
            return False

    # If we pass all checks, return True
    # print(f'Found 4 consecutive {symbol} starting at ({row}, {col}) in direction ({dir_row}, {dir_col})')
    return True

def check_winner(board, symbol, row, col):
    # This function checks for a winner. Returns true if there's a winner

    print(f'Checking winner for row {row}, col {col}')
    # Check vertical direction
    if check4(row,col,1,0,board,symbol) or check4(row,col, -1,0,board,symbol):
        return True
    # Check horizontal direction
    if check4(row,col,0,1,board,symbol) or check4(row,col, 0,-1,board,symbol):
        return True
    # Check \ direction
    if check4(row, col, -1, -1, board, symbol) or check4(row, col, 1, 1, board, symbol):
        return True
    # Check / direction
    if check4(row, col, 1, -1, board, symbol) or check4(row, col, -1, 1, board, symbol):
        return True
    return False


def main():
    print_welcome()
    players = ['Chin', 'Computer']
    symbols = ['X', 'O']
    active_player_index = 0
    log(f'It is {players[active_player_index]}\'s turn')

    # Create an empty board
    board = create_board()
    log('Board created')

    while True:
        # Initialise row and column for checking of winning sequence later
        row = 999
        column = 0
        while row == 999:
            # Get player's choice of column to drop piece. Print error message if invalid input
            # Keep looping until there's a valid column chosen
            try:
                column = int(input(f'It is {players[active_player_index]}\'s turn! Choose your column to drop your piece!: '))
                if column < 8:
                    # Minus 1 for list index
                    column -= 1
                else:
                    print(Fore.RED + "Please enter a number less than 7.")
                    print(Fore.LIGHTYELLOW_EX)
            except ValueError:
                print(Fore.RED + "Invalid input! Please enter an integer.")
                print(Fore.LIGHTYELLOW_EX)
            # Keep looping until valid row is selected
            # Game will keep in loop if player selects a fully filled column
            board, row = drop_piece(board, symbols[active_player_index], column)

        log(f'{players[active_player_index]} choose to drop piece at row {row} column {column+1}')

        if not check_winner(board, symbols[active_player_index],row,column):
            # No winner
            # Print board for next turn
            print_board(board)
            # Change player
            active_player_index = (active_player_index + 1) % len(players)
        else:
            # Player wins
            print(Fore.GREEN + f'Player {players[active_player_index]} wins!')
            log(f'Player {players[active_player_index]} wins!')
            print_board(board)
            # Exit game
            break

if __name__ == '__main__':
    main()

