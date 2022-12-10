#import gamepy
from random import randint as rand

player = 'X'
cpu = 'O'
first_player = player
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


def check_winner(board: list):
    global player
    global cpu
    fc = free_cells(map)
    if conditions(board, player):
        return player
    elif conditions(board, cpu):
        return cpu
    elif len(fc) == 0:
        return -1
    return 0


def draw_grid(board: list, show_idx: bool = False):
    for i in range(0, len(board), 3):
        for j in range(i, i + 3):
            if show_idx:
                print(board[j], end=' ')
            else:
                print(
                    f"{board[j] if board[j] == 'X' or board[j] == 'O' else ' '}", end=' ')
        print()

def set_first_player():
    global player
    global cpu
    global first_player
    r = rand(0, 1)
    if rand == 1:
        player, cpu = cpu, player
    first_player = cpu

while True:
    user_input = int(input('Куда ставить метку: '))
    map[user_input] = player
    draw_grid(map)
    winner = check_winner(map)
    if winner == player:
        print('Вы победили!')
        break
    elif winner == cpu:
        print('Вы проиграли')
        break
    elif winner == -1:
        print('Ничья!')
        break
    print('Ход соперника...')
    cpu_turn = minimax(map)['index']
    map[cpu_turn] = cpu
    print(f'Он поставил на {cpu_turn}!')
    draw_grid(map)
    winner = check_winner(map)
    if winner == player:
        print('Вы победили!')
        break
    elif winner == cpu:
        print('Вы проиграли')
        break
    elif winner == -1:
        print('Ничья!')
        break
