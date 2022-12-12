from random import randint as rand
from time import sleep
import os


def clear(): return os.system('cls')


two_players = False
sweets = 117
player = {'id': 'Игрок 1', 'score': 0}
cpu = {'id': 'Игрок 2', 'score': 0}

first_player = player
turn = player


def random_turn():
    return rand(1, 28)


def make_turn():
    global sweets, turn, two_players
    if two_players:
        player_turn()
    elif not two_players and turn['id'] == 'Игрок 2':
        if sweets > 28:
            grab = random_turn()
            sweets -= grab
            turn['score'] += grab
            print(f'{turn["id"]} взял {grab} конфет')
        else:
            grab = sweets
            sweets = 0
            turn['score'] += grab
            print(f'{turn["id"]} взял {grab} конфет')
    else:
        player_turn()
    print(f'Осталось {sweets} конфет')


def next_turn():
    global turn, player, cpu
    turn = player if turn == cpu else cpu


def player_turn():
    global sweets
    while True:
        user_input = int(input('Введите количество конфет: '))
        if user_input > sweets or user_input > 28:
            print('Нельзя взять столько конфет!')
        else:
            break
    sweets -= user_input
    turn['score'] += user_input


def set_first_player():
    global cpu, player, first_player, two_players
    r = rand(0, 1)
    if r == 1:
        first_player = cpu
    is_cpu = '' if two_players else '(cpu)'
    return f'{f"Игрок 2{is_cpu}" if first_player == cpu else "Игрок 1"}'


def check_winner(prompt: bool = True):
    global player
    global cpu
    if sweets == 0:
        if prompt:
            print(f'{turn["id"]} победил со счетом {turn["score"]}!')
        return False
    return True


user_input = ''
while user_input not in ['y', 'n']:
    clear()
    user_input = input('Играем с компьютером? (y/n): ')
two_players = user_input == 'n'

running = True
while running:
    clear()
    print(f"{turn['id']} ходит")
    sleep(1)
    make_turn()
    sleep(1)
    running = check_winner()
    sleep(2)
    next_turn()
