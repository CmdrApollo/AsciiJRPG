def lerp(a, b, t) -> float:
    return a + (b - a) * t

class Command:
    def __init__(self):
        self.started: bool = False
        self.completed: bool = False
    
    def update(self, engine, delta: float) -> None:
        pass

class MoveTo(Command):
    def __init__(self, obj, tx: int = 0, ty: int = 0, duration: float = 1.0):
        super().__init__()
        self.obj = obj
        self.ox, self.oy = obj.x, obj.y
        self.tx = tx
        self.ty = ty
        self.duration = duration
        self.time_so_far = 0.0
    
    def update(self, engine, delta):
        self.time_so_far += delta
        if self.time_so_far >= self.duration:
            self.completed = True
            self.time_so_far = self.duration
            self.obj.x = self.tx
            self.obj.y = self.ty
            return
        
        self.obj.x = int(lerp(self.ox, self.tx, self.time_so_far / self.duration))
        self.obj.y = int(lerp(self.oy, self.ty, self.time_so_far / self.duration))

class WaitCommand(Command):
    def __init__(self, duration: float = 1.0):
        super().__init__()
        self.duration: float = duration
        self.time_so_far: float = 0.0
    
    def update(self, engine, delta: float) -> None:
        self.time_so_far += delta
        if self.time_so_far >= self.duration:
            self.completed = True

class AddDialogue(Command):
    def __init__(self, dialogue: list[str]):
        super().__init__()
        self.dialogue = dialogue
    
    def update(self, engine, delta):
        if not self.started:
            engine.queue_dialogue(self.dialogue)

class RemoveDynamic(Command):
    def __init__(self, dyn):
        super().__init__()
        self.dyn = dyn
    
    def update(self, engine, delta):
        if not self.started:
            engine.dynamics.remove(self.dyn)
            self.completed = True

class ChangeMap(Command):
    def __init__(self, map_name: str, map_x: int, map_y: int):
        super().__init__()
        self.map_name: str = map_name
        self.map_x: int = map_x
        self.map_y: int = map_y
    
    def update(self, engine, delta):
        if not self.started:
            engine.load_map(self.map_name, self.map_x, self.map_y)
            self.completed = True