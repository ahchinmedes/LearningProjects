print('Welcome to Connect4!')
'''
TODO: Build the board
TODO: Toggle players

'''
def create_board():
    ## Initialise a 6x7 board
    board = [[None for _ in range(7)] for _ in range(6) ]
    return board

def print_board(board):
    for row in board:
        print(row)

def main():
    players = ['Chin', 'Computer']
    symbols = ['X', 'O']
    active_player_index = 0
    board = create_board()
    print_board(board)


if __name__ == '__main__':
    main()