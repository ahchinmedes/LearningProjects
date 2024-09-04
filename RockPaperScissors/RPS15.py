import random
from colorama import Fore
import csv

def print_welcome():
    print(Fore.LIGHTCYAN_EX)
    print("----------------------")
    print("Welcome to Rock Paper Scissors!")
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

def check_win():
    '''
    TODO: Need to implement the checks for wins.
    :return:
    '''

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

    rounds = 5
    i = 0
    while i < rounds:
        computer_roll = random.choice(list(win_table.keys()))
        '''
        TODO: Need to print choices for player to choose, and also check for errors, before sending it to check for
        for winning scenario.
        '''
        player_roll = input(f'Which roll do you want to play? [S]cissors, [R]ock [P]aper, {player1.name}  ')
        if player_roll.lower() == 's':
            print(f'You choose Scissors!')
            win = scissors.check_win(computer_roll)
        elif player_roll.lower() == 'r':
            print(f'You choose Rock!')
            win = rock.check_win(computer_roll)
        elif player_roll.lower() == 'p':
            print(f'You choose Paper!')
            win = paper.check_win(computer_roll)
        else:
            # invalid input from player
            print(f'Please select "S", "R", "P" only!')
            continue

        if win == "win":
            print(Fore.GREEN)
            print(f'You win! Computer played {computer_roll}')
            player1.score += 1
            print(f'Score for Round {i+1} is {player1.name}: {player1.score}... {player2.name}: {player2.score}')
            i += 1
            print(Fore.LIGHTYELLOW_EX)
        elif win == "lose":
            print(Fore.RED)
            print(f'You lose... Computer played {computer_roll}')
            player2.score += 1
            print(f'Current score for Round {i+1} is {player1.name}: {player1.score}... {player2.name}: {player2.score}')
            i += 1
            print(Fore.LIGHTYELLOW_EX)
        else:
            print(Fore.BLUE)
            print(f'Its a tie! Computer played {computer_roll}')
            print(f'Current score for Round {i+1} is {player1.name}: {player1.score}... {player2.name}: {player2.score}')
            i += 1
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