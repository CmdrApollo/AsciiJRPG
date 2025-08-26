from dynamics import *
from maps import *
from theater import Theater
from commands import *

class Engine:
    def __init__(self):

        self.all_maps = [Overworld(), Village1()]

        self.current_map = self.all_maps[1]

        self.player: Dynamic = DynamicCreature("Player", self.current_map.player_start_x, self.current_map.player_start_y)
        self.dynamics: list[Dynamic] = self.current_map.populate_dynamics()

        self.theater = Theater(self)

        for command in [
            MoveTo(self.player, 9, 10, 2),
            WaitCommand(0.5),
            AddDialogue([
                f"[{self.dynamics[0].name}]",
                "Bring me my Widget of Wisdom from Mount Doom!"
            ]),
            AddDialogue([
                f"[{self.dynamics[0].name}]",
                "This thing is of utmost importance!"
            ]),
            MoveTo(self.dynamics[0], 10, 8, 1),
            WaitCommand(0.5),
            RemoveDynamic(self.dynamics[0])
        ]:
            self.theater.add_command(command)
        
        self.show_dialogue = False
        self.dialogue_to_show = []
        self.queued_dialogue = []

    def queue_dialogue(self, block: list[str]):
        if self.dialogue_to_show == []:
            self.dialogue_to_show = block
        else:
            self.queued_dialogue.append(block)

        self.show_dialogue = True

    # TODO naming is confusing
    def add_dialogue(self, block: list[str]):
        self.theater.add_command(AddDialogue(block))
    
    def load_map(self, map_name, x=None, y=None):
        map_to_load = None
        for m in self.all_maps:
            if m.name == map_name:
                map_to_load = m
                break
        
        if map_to_load is not None:
            self.current_map = map_to_load

            self.player.x = x if x else self.current_map.player_start_x
            self.player.y = y if y else self.current_map.player_start_y

            self.dynamics = self.current_map.populate_dynamics()

            self.add_dialogue([
                "=" * 40,
                self.current_map.name.rjust(20 + len(self.current_map.name) // 2, ' '),
                "=" * 40
            ])

    def load_overworld(self, x, y):
        self.load_map("Overworld", x, y)