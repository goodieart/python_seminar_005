from random import randint as rand, choice
import os
from time import sleep

clear = lambda: os.system('cls')

D_EASY = 0
D_HARD = 1
D_HUMAN = 2

player = 'X'
cpu = 'O'
first_player = player
difficulty = D_EASY
first_move = True

map = [i for i in range(9)]


def free_cells(board) -> list:
    return [i for i in range(len(board)) if board[i] != 'X' and board[i] != 'O']


def minimax(board: list, side: int = cpu) -> dict:
    global player
    global cpu
    params = {'score': 0, 'index': 0}
    fc = free_cells(board)

    if conditions(board, player):
        params['score'] = -10
        return params
    elif conditions(board, cpu):
        params['score'] = 10
        return params
    elif len(fc) == 0:
        params['score'] = 0
        return params

    moves = []

    for i in range(len(fc)):
        move = {'index': 0, 'score': 0}
        move['index'] = board[fc[i]]
        board[fc[i]] = side
        if side == cpu:
            result = minimax(board, player)
        else:
            result = minimax(board, cpu)
        move['score'] = result['score']
        board[fc[i]] = move['index']
        moves.append(move)

    best_move = 0
    if side == cpu:
        best_score = -10000
        for i in range(len(moves)):
            if moves[i]['score'] > best_score:
                best_score = moves[i]['score']
                best_move = i
    else:
        best_score = 10000
        for i in range(len(moves)):
            if moves[i]['score'] < best_score:
                best_score = moves[i]['score']
                best_move = i
    return moves[best_move]


def get_mask(board: list, side: str) -> list:
    return [1 if board[i] == side else 0 for i in range(len(board))]

def random_turn(board: list):
    fc = free_cells(board)
    turn = choice(fc)
    return turn

def conditions(board: list, side: str) -> bool:
    t = get_mask(board, side)
    c = [[1, 1, 1, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 1, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 1, 1],
         [1, 0, 0, 0, 1, 0, 0, 0, 1],
         [0, 0, 1, 0, 1, 0, 1, 0, 0],
         [1, 0, 0, 1, 0, 0, 1, 0, 0],
         [0, 1, 0, 0, 1, 0, 0, 1, 0],
         [0, 0, 1, 0, 0, 1, 0, 0, 1]]

    for i in range(len(c)):
        f = 0
        for j in range(len(t)):
            if t[j] == c[i][j] and t[j] == 1:
                f += 1
            if f == 3:
                return True
    return False


def check_winner(board: list, prompt: bool = True):
    global player
    global cpu
    fc = free_cells(map)
    if conditions(board, player):
        if prompt: print('Игрок 1 победил!')
        return player
    elif conditions(board, cpu):
        if prompt: print('Игрок 1 проиграл')
        return cpu
    elif len(fc) == 0:
        if prompt: print('Ничья!')
        return -1
    return 0


def draw_grid(board: list, show_idx: bool = False):
    for i in range(0, len(board), 3):
        buffer = []
        for j in range(i, i + 3):
            if show_idx:
                buffer.append(board[j])
            else:
                buffer.append(f"{board[j] if board[j] == 'X' or board[j] == 'O' else ' '}")
        print(' | '.join(buffer))
        if i < len(board) - 3: print('---------')

def set_first_player():
    global cpu, player, first_player, difficulty
    r = rand(0, 1)
    if r == 1:
        player, cpu = cpu, player
        first_player = cpu
    is_cpu = '(cpu)' if difficulty == 3 else ''
    return f'{f"Игрок 2{is_cpu}" if first_player == cpu else "Игрок 1"}'

def set_difficulty(d: int):
    global difficulty
    difficulty = d

def player_turn(board: list):
    user_input = int(input('Куда ставить метку: '))
    board[user_input] = player

def cpu_turn(board: list):
    global first_move
    global difficulty
    global D_EASY, D_HARD, D_HUMAN
    if difficulty == D_EASY:
        cpu_turn = random_turn(board)
    elif difficulty == D_HARD:
        if first_move:
            cpu_turn = random_turn(board)
            first_move = False
        else:
            cpu_turn = minimax(board)['index']
    else:
        cpu_turn = int(input('Второй игрок, куда ставим?'))
    board[cpu_turn] = cpu
    return cpu_turn


clear()

print('Выберите уровень сложности [0 - 2; 2 - hotseat]: ', end='')
set_difficulty(int(input()))

clear()

if difficulty != D_HUMAN:
    print(f'Вы выбрали {"легкий " if difficulty == D_EASY else "сложный "}уровень')
else:
    print('Вы выбрали игру с человеком')

sleep(2)


print('Кидаем жребий...')
sleep(1)
fp = set_first_player()
sleep(1)
print(f'Перым ходит {first_player} ({fp})!')
sleep(2)
clear()

while True:
    if first_player == player:
        print('Игрок 1, ваш ход!')
        sleep(2)
        draw_grid(map)
        player_turn(map)
    else:
        print('Ход соперника...')
        sleep(1)
        print(f'Он поставил на {cpu_turn(map)}!')
    
    draw_grid(map)
    sleep(3)
    clear()
    
    winner = check_winner(map)
    if winner != 0:
        draw_grid(map)
        sleep(5)
        break

    if first_player == player:
        print('Ход соперника...')
        sleep(1)
        print(f'Он поставил на {cpu_turn(map)}!')
    else:
        print('Игрок 1, ваш ход!')
        sleep(2)
        draw_grid(map)
        player_turn(map)
    
    draw_grid(map)
    sleep(3)
    clear()
    
    winner = check_winner(map)
    if winner != 0:
        draw_grid(map)
        sleep(5)
        break
    
    draw_grid(map)
