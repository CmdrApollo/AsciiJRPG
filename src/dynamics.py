from commands import AddDialogue

class Dynamic:
    def __init__(self, name: str, x: int, y: int, graphic: str|None = None, solid_vs_map: bool = False, solid_vs_dyn: bool = False) -> None:
        self.name = name

        self.x = x
        self.y = y

        self.graphic = graphic

        self.solid_vs_map = solid_vs_map
        self.solid_vs_dyn = solid_vs_dyn

    def on_interact(self, engine):
        pass

class DynamicCreature(Dynamic):
    def __init__(self, name: str, x: int, y: int, graphic: str = "player"):
        super().__init__(name, x, y, graphic, True, True)

class SignPost(Dynamic):
    def __init__(self, x, y, text, graphic = None):
        super().__init__("signpost", x, y, graphic, False, True)
        self.text = text
    
    def on_interact(self, engine):
        engine.add_dialogue(self.text)

class ToWorldTeleport(Dynamic):
    def __init__(self, x, y, to_x, to_y):
        super().__init__("toworldteleport", x, y, None, False, False)
        self.to_x = to_x
        self.to_y = to_y

    def on_interact(self, engine):
        engine.load_overworld(self.to_x, self.to_y)

class MapLoader(Dynamic):
    def __init__(self, x, y, to_map, to_x=None, to_y=None):
        super().__init__("maploader", x, y, None, False, False)
        self.to_map = to_map
        self.to_x = to_x
        self.to_y = to_y

    def on_interact(self, engine):
        engine.load_map(self.to_map, self.to_x, self.to_y)