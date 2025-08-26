from graphics import Loader
from dynamics import *

class Map:
    player_start_x = 0
    player_start_y = 0
    
    def __init__(self, name, gfx, path = None):
        self.name = name
        self.graphics = gfx

        self.path = "assets/maps/village1.map" if not path else path
        
        tile_names = list(gfx.graphics.keys())

        with open(self.path, 'r') as f:
            self.width = int(f.readline())
            self.height = int(f.readline())
            
            self.tiles = []
            self.solid = []

            for line in f.read().splitlines():
                for element in line.split(','):
                    index, solid = element.split(' ')
                    index = int(index)
                    solid = bool(int(solid))

                    # if index == 0:
                    #     index = random.choice([0, 14])

                    self.tiles.append(tile_names[index])
                    self.solid.append(solid)
    
    def get_tile(self, x, y) -> str:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y * self.width + x]
        return None

    def get_solid(self, x, y) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.solid[y * self.width + x]
        return True

    def populate_dynamics(self) -> list[Dynamic]:
        return []
    
    def on_interaction(self, engine, target) -> bool:
        return False

class Overworld(Map):
    def __init__(self):
        super().__init__("Overworld", Loader("assets/gfx/overworld"), "assets/maps/overworld.map")

    def populate_dynamics(self):
        return [
            MapLoader(1, 1, "Sor'ba", 46, 11)
        ]

class Village1(Map):
    def __init__(self):
        super().__init__("Sor'ba", Loader("assets/gfx/tileset1"), "assets/maps/output.map")

        self.player_start_x = 3
        self.player_start_y = 10
    
    def populate_dynamics(self) -> list[Dynamic]:
        dyns = []

        dyns.append(DynamicCreature("Bjogar the Automata", 10, 10, "automata"))
        dyns.append(ToWorldTeleport(47, 11, 2, 1))
        dyns.append(ToWorldTeleport(47, 12, 2, 1))
        dyns.append(SignPost(10, 8, [
                f"[{dyns[0].name}]",
                "What are you doing here, adventurer?",
                "Go and retrieve my Widget of Wisdom",
                "from Mount Doom!"
            ], None))
        dyns.append(SignPost(45, 10, [
            f"Welcome to {self.name}!"
        ], "signpost"))
        
        return dyns