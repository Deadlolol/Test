import curses
import random
import time


def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    while True:
        play(stdscr)
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        msg = "Game Over! Press 'r' to restart or 'q' to quit."
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(h // 2, max(0, (w - len(msg)) // 2), msg)
        stdscr.attroff(curses.color_pair(2))
        stdscr.refresh()
        while True:
            key = stdscr.getch()
            if key == ord('r'):
                break
            elif key == ord('q'):
                return


def play(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    border_top = 2
    border_left = 0
    border_bottom = h - 1
    border_right = w - 1

    play_h = border_bottom - border_top
    play_w = border_right - border_left

    def draw_border():
        stdscr.attron(curses.color_pair(4))
        stdscr.border()
        stdscr.attroff(curses.color_pair(4))

    start_y = (border_top + border_bottom) // 2
    start_x = (border_left + border_right) // 2
    snake = [[start_y, start_x], [start_y, start_x - 1], [start_y, start_x - 2]]
    direction = curses.KEY_RIGHT

    def random_food(snake_body):
        while True:
            fy = random.randint(border_top + 1, border_bottom - 1)
            fx = random.randint(border_left + 1, border_right - 1)
            if [fy, fx] not in snake_body:
                return [fy, fx]

    food = random_food(snake)
    score = 0
    base_delay = 0.15
    min_delay = 0.04

    stdscr.nodelay(True)
    stdscr.keypad(True)

    last_direction = direction

    while True:
        delay = max(min_delay, base_delay - (score * 0.005))

        draw_border()

        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(0, 2, f" Score: {score} ")
        stdscr.attroff(curses.color_pair(3))

        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(food[0], food[1], '*')
        stdscr.attroff(curses.color_pair(2))

        stdscr.attron(curses.color_pair(1))
        for i, segment in enumerate(snake):
            ch = '@' if i == 0 else 'o'
            stdscr.addstr(segment[0], segment[1], ch)
        stdscr.attroff(curses.color_pair(1))

        stdscr.refresh()

        start_time = time.time()
        key = -1
        while time.time() - start_time < delay:
            k = stdscr.getch()
            if k != -1:
                key = k
            time.sleep(0.01)

        opposites = {
            curses.KEY_UP: curses.KEY_DOWN,
            curses.KEY_DOWN: curses.KEY_UP,
            curses.KEY_LEFT: curses.KEY_RIGHT,
            curses.KEY_RIGHT: curses.KEY_LEFT,
        }

        if key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
            if key != opposites.get(last_direction):
                direction = key

        head = snake[0]
        if direction == curses.KEY_UP:
            new_head = [head[0] - 1, head[1]]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0] + 1, head[1]]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1] - 1]
        elif direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1] + 1]
        else:
            new_head = [head[0], head[1] + 1]

        last_direction = direction

        if (
            new_head[0] <= border_top
            or new_head[0] >= border_bottom
            or new_head[1] <= border_left
            or new_head[1] >= border_right
            or new_head in snake
        ):
            return

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = random_food(snake)
        else:
            tail = snake.pop()
            stdscr.addstr(tail[0], tail[1], ' ')


if __name__ == '__main__':
    curses.wrapper(main)
