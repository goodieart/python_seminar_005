from random import randint as rand, choice
D_EASY = 0
D_HARD = 1
D_HUMAN = 2

player = 'X'
cpu = 'O'
first_player = player
difficulty = D_EASY
first_move = True


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


def get_mask(board: list, side: str) -> list:
    return [1 if board[i] == side else 0 for i in range(len(board))]


def free_cells(board) -> list:
    return [i for i in range(len(board)) if board[i] != 'X' and board[i] != 'O']


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
        fc = free_cells(board)
        while True:
            cpu_turn = int(input('Второй игрок, куда ставим?'))
            if not cpu_turn in fc:
                print('Клетка занята!')
            else:
                break
    board[cpu_turn] = cpu
    return cpu_turn


def random_turn(board: list):
    fc = free_cells(board)
    turn = choice(fc)
    return turn


def set_difficulty(d: int):
    global difficulty
    difficulty = d


def player_turn(board: list):
    fc = free_cells(board)
    while True:
        user_input = int(input('Куда ставить метку: '))
        if not user_input in fc:
            print('Клетка занята!')
        else:
            board[user_input] = player
            break
