from commands import *

class Theater:
    def __init__(self, engine = None):
        self.engine = engine
        self.commands: list[Command] = []
    
    def add_command(self, command: Command):
        self.commands.append(command)
    
    def update(self, delta: float) -> None:
        cmd = self.commands[0]

        cmd.update(self.engine, delta)
        
        if cmd.completed:
            self.commands.pop(0)
        else:
            if not cmd.started:
                cmd.started = True