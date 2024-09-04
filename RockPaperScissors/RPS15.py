import random
from colorama import Fore
import csv

def print_welcome():
    print(Fore.LIGHTCYAN_EX)
    print("----------------------")
    print("Welcome to Rock Paper Scissors 15-Way Edition!!")
    print("----------------------")
    print(Fore.LIGHTYELLOW_EX)

def read_rolls():
    win_table = {}
    with open('battle-table.csv') as fin:
        reader = csv.DictReader(fin)
        for row in reader:
            key = row['Attacker']
            win_table[key] = read_roll(row)
    return win_table

def read_roll(row: dict):
    # Delete Attacker key from dict
    del row['Attacker']
    return row

def check_win(player_roll, computer_roll, win_table):
    """
    :return: "win" if player wins, "lose" if player loses, "draw" if player draws
    """
    return win_table[player_roll][computer_roll]

class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

def main():
    print_welcome()
    win_table = read_rolls()

    name = input("What is your name? ")
    player1 = Player(name,0)
    player2 = Player("Computer",0)
    win = ""

    rounds = 5
    i = 0
    while i < rounds:
        computer_roll = random.choice(list(win_table.keys()))
        '''
        TODO: Need to print choices for player to choose, and also check for errors, before sending it to check for
        for winning scenario.
        '''
        player_roll = input(f'Which roll do you want to play, {player1.name}? Here are the options. Please key in the full string.\n{list(win_table.keys())}')
        if player_roll.rstrip() not in list(win_table.keys()):
            print(f'Invalid Option! Please try again.')
            continue
        else:
            print(f'Valid')
            win = check_win(player_roll.rstrip(), computer_roll, win_table)
            i += 1

        if win == "win":
            print(Fore.GREEN)
            print(f'You win! Computer played {computer_roll}')
            player1.score += 1
            print(f'Score for Round {i} is {player1.name}: {player1.score}... {player2.name}: {player2.score}')
            print(Fore.LIGHTYELLOW_EX)
        elif win == "lose":
            print(Fore.RED)
            print(f'You lose... Computer played {computer_roll}')
            player2.score += 1
            print(f'Current score for Round {i} is {player1.name}: {player1.score}... {player2.name}: {player2.score}')
            print(Fore.LIGHTYELLOW_EX)
        else:
            print(Fore.BLUE)
            print(f'Its a tie! Computer played {computer_roll}')
            print(f'Current score for Round {i} is {player1.name}: {player1.score}... {player2.name}: {player2.score}')
            print(Fore.LIGHTYELLOW_EX)

    # Print message for overall winner
    if player1.score > player2.score:
        print(Fore.GREEN)
        print(f'You win the game!')
    elif player2.score > player1.score:
        print(Fore.RED)
        print(f'You lose the game!')
    else:
        print(Fore.BLUE)
        print('It is a tie!!')

if __name__ == '__main__':
    main()