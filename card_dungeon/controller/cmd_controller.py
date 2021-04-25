import cmd
import card_dungeon.model as model

class DoCCLI(cmd.Cmd):
    intro = "Welcome to the Dungeon of Cards CLI.\n" \
            "Type 'start' to get going!\n" \
            "Type 'help' to see available commands.\n"
    prompt = "What next?"

    def __init__(self):
        super().__init__(completekey='tab')
        self.game = None


    def run(self):

        self.cmdloop()

    def do_battle(self,arg):
        ' Run a battle'

        p = model.PlayerCharacter(name="Keith", type="Warrior")
        npc = model.EnemyCharacter(name="George", type = "Goblin")
        self.game = model.Battle(player=p, enemy=npc)
        self.game.initialise()
        self.game.print()

    def do_round(self, arg):
        if self.game is not None:
            self.game.do_round()
        else:
            print("No battle going on!")

    def do_hand(self, arg):

        if self.game is not None:
            print(f'Cards that {self.game.player.name}s Hand:')
            for card in self.game.player_hand:
                card.print()
        else:
            print("No battle going on!")

