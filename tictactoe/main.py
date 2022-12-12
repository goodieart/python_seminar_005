import ai
import os
from ai import cpu, player, difficulty, first_player
from time import sleep


def clear(): return os.system('cls')


map = [i for i in range(9)]

def show_winner(game_result: str):
    anim = ['-', chr(92), '|', '/']
    i = 0
    while i < 10:
        clear()
        print(anim[i] * 32)
        print(f'{anim[i]} {game_result}' + (29 - len(game_result)) * ' ' + anim[i])
        print(anim[i] * 32)
        sleep(1)
        i += 1
        if i > 3: i = 0
    exit()

def check_winner(board: list, prompt: bool = True):
    global player
    global cpu
    fc = ai.free_cells(map)
    if ai.conditions(board, player):
        if prompt:
            show_winner('Игрок 1 победил!')
        return False
    elif ai.conditions(board, cpu):
        if prompt:
            show_winner('Игрок 2 победил!')
        return False
    elif len(fc) == 0:
        if prompt:
            show_winner('Ничья!')
        return False
    return True


def draw_grid(board: list, show_idx: bool = False):
    for i in range(0, len(board), 3):
        buffer = []
        for j in range(i, i + 3):
            if show_idx:
                buffer.append(board[j])
            else:
                buffer.append(
                    f"{board[j] if board[j] == 'X' or board[j] == 'O' else ' '}")
        print(' | '.join(buffer))
        if i < len(board) - 3:
            print('---------')


def draw_interface(prompt):
    print(f'--------------------------------')
    print(f'| {prompt}' + (29 - len(prompt)) * ' ' + '|')
    print(f'--------------------------------')


def set_first_player():
    global cpu, player, first_player, difficulty
    r = ai.rand(0, 1)
    if r == 1:
        first_player = cpu
    is_cpu = '(cpu)' if difficulty == 3 else ''
    return f'{f"Игрок 2{is_cpu}" if first_player == cpu else "Игрок 1"}'


def update_game_screen(board: list, prompt: str, interval_before: float = 2, interval_after: float = 2, todo=None):
    sleep(interval_before)
    clear()
    draw_interface(prompt)
    draw_grid(board)

    if not todo == None:
        todo(board)

    sleep(interval_after)


clear()

print('Выберите уровень сложности [0 - 2; 2 - hotseat]: ', end='')
ai.set_difficulty(int(input()))

clear()

if ai.difficulty != ai.D_HUMAN:
    print(
        f'Вы выбрали {"легкий " if ai.difficulty == ai.D_EASY else "сложный "}уровень')
else:
    print('Вы выбрали игру с человеком')

sleep(2)


print('Кидаем жребий...')
sleep(1)
fp = set_first_player()
sleep(1)
print(f'Первым ходит {first_player} ({fp})!')
sleep(2)
clear()

running = True

while running:
    if first_player == player:
        clear()
        print('Игрок 1, ваш ход!')
        update_game_screen(map, 'Игрок 1 ходит',
                           interval_after=0, todo=ai.player_turn)
        update_game_screen(map, 'Игрок 1 ходит',
                           interval_before=0, interval_after=2)
    else:
        clear()
        print('Ход соперника...')
        update_game_screen(map, 'Игрок 2 ходит',
                           interval_after=0, todo=ai.cpu_turn)
        update_game_screen(map, 'Игрок 2 ходит',
                           interval_before=0, interval_after=2)

    running = check_winner(map)

    if running:
        if first_player == player:
            clear()
            print('Ход соперника...')
            update_game_screen(map, 'Игрок 2 ходит',
                               interval_after=0, todo=ai.cpu_turn)
            update_game_screen(map, 'Игрок 2 ходит',
                               interval_before=0, interval_after=2)
        else:
            clear()
            print('Игрок 1, ваш ход!')
            update_game_screen(map, 'Игрок 1 ходит',
                               interval_after=0, todo=ai.player_turn)
            update_game_screen(map, 'Игрок 1 ходит',
                               interval_before=0, interval_after=2)

    running = check_winner(map)
