import curses
from curses import wrapper
import random
import string
import time


def random_char():
    chars = string.ascii_letters + string.digits + string.punctuation
    return random.choice(chars)


def main(stdscr):
    # init colors
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, 66, -1)
    WHITE = curses.color_pair(1)
    GREEN = curses.color_pair(2)
    GREY = curses.color_pair(3)
    curses.curs_set(False)  # make cursor invisible

    # init variables
    cols = curses.COLS - 1
    lines = curses.LINES - 1

    # setup the grid
    # In the rain animation, only the colors move,
    # the randoms chars stay the same at the same place.
    grid = {}
    for col in range(cols):
        # default column settings
        grid[col] = {
            "start": random.randint(-(lines // 3), lines - 1),
            "length": random.randint(lines // 3, lines - lines // 5),
            "speed": random.randint(1, 6) / 2,
        }

        # fill the grid with random chars
        for case in range(lines):
            grid[col][case] = random_char()

    # start the animation
    while True:
        for col in range(cols):

            # jump 1/2 line to be more beautiful
            if col % 2 != 0:
                continue

            # increment the start of the column to create a moving effect
            # when the rain stream reaches the bottom, it starts a new one
            if grid[col]['start'] >= lines:
                grid[col]['length'] = random.randint(lines // 3, lines - 5)
                grid[col]['start'] = -grid[col]['length']
            else:
                grid[col]['start'] += grid[col]['speed']

            # shortcut variable names
            start = grid[col]['start']
            length = grid[col]['length']
            end = start + length % lines

            # colorize the column cases depending on rain stream position
            for case in range(lines):
                # ~1/4 of the stream rain is fade
                tail_len = min(length // 4, lines // 4)

                # note: clear the all screen causes screen blinking
                # erasing instead of clearing is more efficient
                if case < start or case > end:
                    stdscr.addstr(case, col, " ", WHITE)

                # draw the stream
                else:
                    char = grid[col][case]

                    # head of the stream
                    if case == end:
                        stdscr.addstr(case, col, char, WHITE)

                    # tail of the stream
                    elif case <= start + tail_len:
                        stdscr.addstr(case, col, char, GREY)

                    # stream body
                    else:
                        stdscr.addstr(case, col, char, GREEN)

        stdscr.refresh()
        time.sleep(0.1)


wrapper(main)
