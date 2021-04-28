import cmd
import card_dungeon.model as model
import logging

class DoCCLI(cmd.Cmd):
    intro = "Welcome to the Dungeon of Cards CLI.\n" \
            "Type 'battle' to get going!\n" \
            "Type 'help' to see available commands.\n"
    prompt = "What next?"

    def __init__(self):
        super().__init__(completekey='tab')
        self.game = None


    def run(self):

        self.cmdloop()

    def do_battle(self,arg):
        'Start a battle'

        p = model.PlayerCharacter(name="Keith", type="Warrior")
        npc = model.EnemyCharacter(name="George", type = "Goblin")
        self.game = model.Battle(player=p, enemy=npc)
        self.game.initialise()
        self.game.print()

    def do_round(self, arg):
        'Run the next round of the battle'
        if self.game is not None:
            self.game.do_round()
        else:
            print("No battle going on!")

    def do_hand(self, arg):
        'Show what a player and enemy have in their hands that they want to use in the next round'

        if self.game is not None:
            print(f'\nCards that {self.game.player.name} holds:')
            for i,card in enumerate(self.game.player_cards.hand):
                print(f'{i+1}. ',end="")
                card.print()

            print(f'\nCards that {self.game.enemy.name} holds:')
            for i, card in enumerate(self.game.enemy_cards.hand):
                print(f'{i+1}. ',end="")
                card.print()
        else:
            print("No battle going on!")

    def do_status(self, arg):
        'Print status of the player and enemy'
        self.game.player.print()
        self.game.enemy.print()

    def do_pick(self, arg):
        'Player picks the next card from their hand'
        if self.game is not None:
            print(f'\nCards that {self.game.player.name} holds:')
            for i,card in enumerate(self.game.player_cards.hand):
                print(f'{i+1}. ',end="")
                card.print()

            choice = pick("Card", self.game.player_cards.hand)
            print(f"You picked {choice}")

            self.game.player_selected_card = choice

        else:
            print("No battle going on!")



# Function to ask the user a simple Yes/No confirmation and return a boolean
def confirm(question : str):

    choices = ["Yes", "No"]

    while True:
        print(question)
        for i in range(0, len(choices)):
            print("%i. %s" % (i+1, choices[i]))
        choice = input("Choice?")
        if choice.isdigit() and int(choice) > 0 and int(choice) <= (len(choices)):
            break
        else:
            print("Invalid choice.  Try again!")

    return (int(choice) == 1)


# Function to present a menu to pick an object from a list of objects
# auto_pick means if the list has only one item then automatically pick that item
def pick(object_type: str, objects: list, auto_pick: bool=False):

    selected_object = None
    choices = len(objects)
    vowels ="AEIOU"
    if object_type[0].upper() in vowels:
        a_or_an = "an"
    else:
        a_or_an = "a"

    # If the list of objects is no good the raise an exception
    if objects is None or choices == 0:
        raise(Exception("No %s to pick from." % object_type))

    # If you selected auto pick and there is only one object in the list then pick it
    if auto_pick is True and choices == 1:
        selected_object = objects[0]

    # While an object has not yet been picked...
    while selected_object == None:

        # Print the menu of available objects to select
        print("Select %s %s:-" % (a_or_an, object_type))

        for i in range(0, choices):
            print("\t%i) %s" % (i + 1, str(objects[i])))

        # Along with an extra option to cancel selection
        print("\t%i) Cancel" % (choices + 1))

        # Get the user's selection and validate it
        choice = input("%s?" % object_type)
        if choice.isdigit() is True:
            choice = int(choice)

            if 0 < choice <= choices:
                selected_object = objects[choice -1]
                logging.info("pick(): You chose %s %s." % (object_type, str(selected_object)))
            elif choice == (choices + 1):
                break
            else:
                print("Invalid choice '%i' - try again." % choice)
        else:
            print("You choice '%s' is not a number - try again." % choice)

    return selected_object
