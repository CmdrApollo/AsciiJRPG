import pygame

from graphics import Loader
from engine import Engine
from theater import Theater
from commands import *

pygame.init()

font = pygame.font.SysFont("cascadiamonoregular", 20)

game_name = "Tactica"

dyn_gfx = Loader("assets/gfx/dynamics")

def clamp(a, minimum, maximum):
    return min(max(a, minimum), maximum)

cache = {}

def main():
    pygame.key.set_repeat(500, 100)

    colors = {
        0: 'white',
        1: '#ff8080',
        2: '#80ff80',
        3: '#8080ff',
        4: '#ffff80',
        5: '#80ffff',
        6: '#ff80ff',
        7: 'white'
    }

    screen_size = (35, 13)

    # game size
    game_size: tuple[int, int] = (screen_size[0] * 3 + 2, screen_size[1] * 3 + 2)

    w, h = game_size

    # half of the terminal width/height
    cx: int = w // 2
    cy: int = h // 2

    char_size = font.size(" ")

    window_size = char_size[0] * game_size[0], char_size[1] * game_size[1]

    window = pygame.Window(title=game_name, size = window_size)
    screen = window.get_surface()

    frame = 0

    engine = Engine()

    cam_x = clamp(engine.player.x - (screen_size[0] // 2), 0, engine.current_map.width - screen_size[0])
    cam_y = clamp(engine.player.y - (screen_size[1] // 2), 0, engine.current_map.height - screen_size[1])

    clock = pygame.time.Clock()
    delta = 0

    running = True

    chars = [(' ', 'white') for _ in range(game_size[0] * game_size[1])]

    def setchar(y, x, char, color = 'white'):
        chars[y * game_size[0] + x] = (char, color)

    def setstr(y, x, string, color = 'white'):
        for i, char in enumerate(string):
            setchar(y, x + i, char, color)

    while running:
        delta = clock.tick_busy_loop(30.0) / 1000.0

        if delta:
            window.title = f"{game_name} - {(1/delta):.1f}fps"

        screen.fill('black')
        # box around the game

        for y in range(game_size[1]):
            if y in [0, game_size[1] - 1]: ch = '+'
            else: ch = '|'
            setchar(y, 0, ch)
            setchar(y, game_size[0] - 1, ch)
        # box around the game
        for x in range(game_size[0]):
            if x in [0, game_size[0] - 1]: ch = '+'
            else: ch = '-'
            setchar(0, x, ch)
            setchar(game_size[1] - 1, x, ch)
        # game title
        setstr(0, 2, game_name)

        for x in range(engine.current_map.width):
            for y in range(engine.current_map.height):
                cx = x - cam_x
                cy = y - cam_y

                if 0 <= cy * 3 < game_size[1] - 2 and 0 <= cx * 3 < game_size[0] - 2:
                    tile = engine.current_map.graphics.get(engine.current_map.get_tile(x, y))
                    for p in engine.dynamics:
                        if x == p.x and y == p.y and p.graphic is not None:
                            tile = dyn_gfx.get(p.graphic)
                    if x == engine.player.x and y == engine.player.y:
                        tile = dyn_gfx.get(f"player-frame-{frame + 1}")
                    for i in range(3):
                        for j in range(3):
                            idx = j * 3 + i
                            setchar(1 + cy * 3 + j, 1 + cx * 3 + i, tile.text[idx], colors[tile.colors[idx]])

        if engine.show_dialogue:
            width, height = max([len(a) for a in engine.dialogue_to_show]) + 2, len(engine.dialogue_to_show) + 2
            bx = game_size[0] // 2 - width // 2
            by = game_size[1] // 4 - height // 2
            for y in range(height):
                for x in range(width):
                    if (x, y) in [(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)]: ch = '+'
                    elif x == 0 or x == width - 1: ch = '|'
                    elif y == 0 or y == height - 1: ch = '-'
                    else: ch = ' '
                    setchar(by + y, bx + x, ch)
            for i, line in enumerate(engine.dialogue_to_show):
                setstr(by + 1 + i, bx + 1, line)
        
        key = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key = event.key

        old_player_x = engine.player.x
        old_player_y = engine.player.y

        if len(engine.theater.commands) == 0:
            if key == pygame.K_UP:
                engine.player.y -= 1
            if key == pygame.K_DOWN:
                engine.player.y += 1
            if key == pygame.K_LEFT:
                engine.player.x -= 1
            if key == pygame.K_RIGHT:
                engine.player.x += 1
            
            for dyn in engine.dynamics: # dynamics list doesn't include player
                if dyn.x == engine.player.x and dyn.y == engine.player.y:
                    # interact with dynamics
                    if dyn.solid_vs_dyn:
                        engine.player.x = old_player_x
                        engine.player.y = old_player_y
                    
                    dyn.on_interact(engine)

        else:
            engine.theater.update(delta)

            if key == pygame.K_SPACE:
                if len(engine.theater.commands) and isinstance(engine.theater.commands[0], AddDialogue):
                    # advance dialogue
                    engine.theater.commands[0].completed = True
                    engine.dialogue_to_show = [] if not len(engine.queued_dialogue) else engine.queued_dialogue.pop(0)
                    engine.show_dialogue = len(engine.dialogue_to_show) > 0
            
        if engine.current_map.get_solid(engine.player.x, engine.player.y):
            engine.player.x = old_player_x
            engine.player.y = old_player_y
        
        if old_player_x != engine.player.x or old_player_y != engine.player.y:
            frame = (frame + 1) % 2
        
            cam_x = clamp(engine.player.x - (screen_size[0] // 2), 0, engine.current_map.width - screen_size[0])
            cam_y = clamp(engine.player.y - (screen_size[1] // 2), 0, engine.current_map.height - screen_size[1])

        for i, char in enumerate(chars):
            x = i % game_size[0]
            y = i // game_size[0]

            if char not in cache:
                cache.update({ char: font.render(char[0], True, char[1], 'black') })
            
            surf = cache[char]

            screen.blit(surf, (x * char_size[0], y * char_size[1]))

        window.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()