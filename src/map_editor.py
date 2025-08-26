import curses
import random
import time
from graphics import Graphic, Loader
from maps import Overworld

game_name = "Tactica Map Editor"

dyn_gfx = Loader("assets/gfx/dynamics")

def clamp(a, minimum, maximum):
    return min(max(a, minimum), maximum)

def main(stdscr):
    curses.curs_set(False)

    curses.noecho()
    stdscr.keypad(True)
    stdscr.nodelay(True)

    # pyotracker can be used with or without color
    has_color: bool = curses.has_colors()

    if has_color:
        # initialize color pairs
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_CYAN)

    # game size
    game_size: tuple[int, int] = (125, 41)

    # get terminal bounds
    h, w = stdscr.getmaxyx()
    if w < game_size[0] or h < game_size[1]:
        # assure that bounds are of sufficient size
        print(f"{game_name} requires at least {game_size[1]} rows and {game_size[0]} columns\n")
        return

    # half of the terminal width/height
    cx: int = w // 2
    cy: int = h // 2

    ox, oy = cx - game_size[0] // 2, cy - game_size[1] // 2

    screen_size = (41, 13)
    world_size = (64, 32)

    cursor_x = 0
    cursor_y = 0

    cam_x = clamp(cursor_x - (screen_size[0] // 2), 0, world_size[0] - screen_size[0])
    cam_y = clamp(cursor_y - (screen_size[1] // 2), 0, world_size[1] - screen_size[1])

    current_map = Overworld()

    delta = 0
    last_time = time.time()

    gfx = list(current_map.graphics.graphics.keys())

    while True:
        delta = time.time() - last_time
        last_time = time.time()

        stdscr.clear()
        # box around the game

        for y in range(game_size[1]):
            if y in [0, game_size[1] - 1]: ch = '+'
            else: ch = '|'
            stdscr.addch(oy + y, ox, ch)
            stdscr.addch(oy + y, ox + game_size[0] - 1, ch)
        # box around the game
        for x in range(game_size[0]):
            if x in [0, game_size[0] - 1]: ch = '+'
            else: ch = '-'
            stdscr.addch(oy, ox + x, ch)
            stdscr.addch(oy + game_size[1] - 1, ox + x, ch)
        # game title
        stdscr.addstr(oy, ox + 2, game_name)

        for x in range(world_size[0]):
            for y in range(world_size[1]):
                cx = x - cam_x
                cy = y - cam_y

                tile = current_map.graphics.get(current_map.get_tile(x, y))
                
                if x == cursor_x and y == cursor_y and int(time.time() * 4) & 1:
                    tile = Graphic("\\0; 0;/0\n 0;x0; 0\n/0; 0;\\0")

                for i in range(3):
                    for j in range(3):
                        idx = j * 3 + i
                        if 0 <= cy * 3 + j < game_size[1] - 2 and 0 <= cx * 3 + i < game_size[0] - 2 - 30:
                            stdscr.addch(oy + 1 + cy * 3 + j, ox + 1 + cx * 3 + i, tile.text[idx], curses.color_pair(tile.colors[idx]))

        for i in range(26):
            if i >= len(gfx):
                break
            
            ex, ey = i % 3, i // 3
            iy, ix = oy + 2 + 4 * ey, ox + game_size[0] - 30 + 10 * ex
            stdscr.addch(iy, ix, chr(i + ord('a')))

            tile = current_map.graphics.get(gfx[i])

            for j in range(3):
                for k in range(3):
                    idx = k * 3 + j
                    stdscr.addstr(iy + k, ix + 1 + j, tile.text[idx], curses.color_pair(tile.colors[idx]))

        try:
            try:
                key = stdscr.getch()
            except curses.error:
                key = -1
        except KeyboardInterrupt:
            continue

        if key == curses.KEY_UP:
            cursor_y -= 1
        if key == curses.KEY_DOWN:
            cursor_y += 1
        if key == curses.KEY_LEFT:
            cursor_x -= 1
        if key == curses.KEY_RIGHT:
            cursor_x += 1
        if key == 27:
            with open("output.map", "w") as f:
                f.write(f"{current_map.width}\n")
                f.write(f"{current_map.height}\n")
                text = "\n".join([",".join([f"{gfx.index(current_map.get_tile(x, y))} {"1" if current_map.get_solid(x, y) else "0"}" for x in range(current_map.width)]) for y in range(current_map.height)])
                f.write(text)
                f.close()
        if key >= ord('a') and key <= ord('z'):
            idx = key - ord('a')

            if idx < len(gfx):
                current_map.tiles[cursor_y * current_map.width + cursor_x] = gfx[idx]
                current_map.solid[cursor_y * current_map.width + cursor_x] = idx not in [0, 1, 14]

        cursor_x = clamp(cursor_x, 0, world_size[0] - 1)
        cursor_y = clamp(cursor_y, 0, world_size[1] - 1)

        cam_x = clamp(cursor_x - (screen_size[0] // 2), 0, world_size[0] - (screen_size[0] - 10))
        cam_y = clamp(cursor_y - (screen_size[1] // 2), 0, world_size[1] - screen_size[1])

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)