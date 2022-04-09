import argparse
import curses
from curses import wrapper
import pickle
from game_field import Field
import os


def find_max_size_of_sheep(n, k):  # максимальный размер кораблика
    for i in range(1, max(k, n)):
        s = 0
        for j in range(1, i + 1):
            s += (i - j + 1) * j
        if s > n * k / 5:
            return i - 1
        if s == n * k / 5:
            return i


def draw(screen, data):  # отрисовываем по координатам
    for i in range(0, len(data)):
        if data[i][2] == '>' or data[i][2] == 'V' or data[i][2] == 'X':
            screen.addstr(data[i][1], data[i][0], data[i][2], curses.color_pair(1))
        else:
            screen.addstr(data[i][1], data[i][0], data[i][2])


def visual(screen, field, impact_x, impact_y, phase):
    screen.clear()
    screen_height, screen_width = screen.getmaxyx()
    draw(screen, field.coordinates(screen_width))
    draw(screen, field.sheep_coordinates(screen_width))
    draw(screen, field.shots_coordinates(screen_width))
    draw(screen, field.computer_shots_coordinates(screen_width))
    draw(screen, field.correction_of_fire(screen_width, impact_x, impact_y))

    padding_x = int((screen_width / 2 - field.k * 2) / 2)
    padding_y = 3
    screen.addstr(padding_y + field.n + 3, padding_x, PLAYER_NAME)  # имя игрока
    screen.addstr(padding_y + field.n + 3, padding_x + int(screen_width / 2),
                  "COMPUTER")  # нижняя полоса поля игрока

    if field.player.square == 0:
        screen.addstr(padding_y + field.n + 6, 0, "DEFEAT")
        screen.addstr(padding_y + field.n + 7, 0, "press n for new game")
        screen.addstr(padding_y + field.n + 8, 0, "press q for exit to the menu")
        phase = "end"
    elif field.computer.square == 0:
        screen.addstr(padding_y + field.n + 6, 0, "VICTORY")
        screen.addstr(padding_y + field.n + 7, 0, "press n for new game")
        screen.addstr(padding_y + field.n + 8, 0, "press q for exit to the menu")
        phase = "end"
    elif phase == "generation":
        screen.addstr(padding_y + field.n + 6, 0, "press q for menu,press g for new generation")
        screen.addstr(padding_y + field.n + 7, 0, "if you are satisfied with the generation press p ")
    elif phase == "correction":
        screen.addstr(padding_y + field.n + 6, 0, "press q for exit")
        screen.addstr(padding_y + field.n + 7, 0, "press s for saving game")
        screen.addstr(padding_y + field.n + 8, 0, "correct x,y coordinates of impact with arrow keys (->,^,<-,v)")
        screen.addstr(padding_y + field.n + 9, 0, "after press Enter for fire")
    return phase


def input_control(user_input, field, impact_x, impact_y, phase):
    status = "normal"
    if user_input == ord('g') and phase == "generation":
        field.update_generation()
    if user_input == ord('q'):
        status = "exit"
    elif user_input == ord('p') and phase == "generation":
        phase = "correction"
    elif user_input == curses.KEY_RIGHT and phase == "correction":
        impact_x = (impact_x + 1) % K
    elif user_input == curses.KEY_LEFT and phase == "correction":
        impact_x = (impact_x - 1) % K
    elif user_input == curses.KEY_UP and phase == "correction":
        impact_y = (impact_y - 1) % N
    elif user_input == curses.KEY_DOWN and phase == "correction":
        impact_y = (impact_y + 1) % N
    elif (user_input == curses.KEY_ENTER or user_input == 10 or user_input == 13) and phase == "correction":
        fire1 = field.computer.shot_in(impact_x, impact_y)  # огонь по короблям компьютера
        if fire1:
            field.computer.square -= 1
        if not fire1:
            k1, k2 = field.computer.shot_out()
            while field.player.shot_in(k1, k2):  # огонь по короблям игрока
                field.player.square -= 1
                k1, k2 = field.computer.shot_out()
    elif user_input == ord('s') and phase == "correction":
        saving_file = open('data.pkl', 'wb')
        pickle.dump(field, saving_file)
        saving_file.close()
    elif user_input == ord('n') and phase == "end":
        status = "new_game"

    return [status, field, impact_x, impact_y, phase]


def play(screen, save_mod):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    M = find_max_size_of_sheep(N, K)

    phase = "generation"
    impact_x = 0
    impact_y = 0

    if save_mod == 's' and os.path.exists('data.pkl'):  # если было сохранение грузим из файла
        pkl_file = open('data.pkl', 'rb+')
        field = pickle.load(pkl_file)
        pkl_file.close()
        phase = "correction"
    else:
        field = Field(N, K, M)
    screen.clear()
    while True:
        screen_height, screen_width = screen.getmaxyx()

        if screen_height < field.n + 15 or screen_width < 2 * field.k + 1:
            screen.refresh()
            screen.addstr(0, 0, "Please make your terminal screen larger.")
            continue
        phase = visual(screen, field, impact_x, impact_y, phase)
        user_input = screen.getch()
        status, field, impact_x, impact_y, phase = input_control(user_input, field, impact_x, impact_y, phase)
        if status == "new_game":
            play(screen, save_mod)
        elif status == "exit":
            main(screen)
            return


def main(screen):
    while True:
        screen.clear()
        screen_height, screen_width = screen.getmaxyx()

        screen.addstr(0, 0, GAME_TITLE)
        screen.addstr(1, 0, "Press 'n' to open new gamwe ")
        screen.addstr(2, 0, "press 's' to open last saving game")
        screen.addstr(3, 0, "press 'q' to exit")

        # Get user input
        answer = screen.getch()
        if answer == ord('n'):
            play(screen, 'n')
        if answer == ord('s'):
            play(screen, 's')
        if answer == ord('q'):
            return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("your_name", help="your name", type=str)
    parser.add_argument("k", help="Number of rows", type=int)
    parser.add_argument("n", help="Number of columns", type=int)

    args = parser.parse_args()

    GAME_TITLE = "SEE BATTLE"
    N = 10
    K = 10
    PLAYER_NAME = ""

    if args.n < 5 or args.k < 5:
        print("the width and height must be greater than 5")
    else:
        K = args.k
        N = args.n
        PLAYER_NAME = args.your_name
        a = N + 20
        b = 2 * K + 10

        wrapper(main)
