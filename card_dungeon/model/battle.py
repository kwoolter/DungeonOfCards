import logging

from .battle_cards import *
from .characters import *
from .events import *
from .card_factory import CardFactory


class Battle():
    ATTACK_BLOCKS = {
        CardFeature.ATTACK_MAGIC: CardFeature.BLOCK_MAGIC,
        CardFeature.ATTACK_MELEE: CardFeature.BLOCK_MELEE
    }

    def __init__(self, player: PlayerCharacter, enemy: EnemyCharacter):

        # Properties
        self.round = 0
        self.is_round_complete = False
        self.player_max_cards_per_hand = 4

        # Components
        self.events = EventQueue()
        self.player = player
        self.enemy = enemy

        self.player_deck = []
        self.enemy_deck = []

        self.player_selected_card = None
        self.player_round_card = None

        self.enemy_selected_card = None
        self.enemy_round_card = None

        self.player_cards = CardManager(max_hand_size=3)
        self.enemy_cards = CardManager(max_hand_size=1)

    @property
    def is_game_over(self):
        return self.player.is_dead or self.enemy.is_dead

    def print(self):
        print(
            f"Round {self.round}: Battle between {self.player.name} the {self.player.type} and {self.enemy.name} the {self.enemy.type}")

    def initialise(self):
        """
        Initialise the battle so that we are ready to start a round
        :rtype: object
        """

        # Build random decks for the player and the enemy
        self.build_deck(card_count=10, is_player_deck=True, deck=self.player_deck)
        self.build_deck(card_count=10, is_player_deck=False, deck=self.enemy_deck)

        self.player_cards.deck = self.player_deck
        self.enemy_cards.deck = self.enemy_deck

        self.reset_round()

    def build_deck(self, card_count: int, is_player_deck: bool, deck: list):
        """
        Add a specified number of randomly generated cards to a deck
        :param card_count: the number of cards that you want to add to the deck
        :param deck: the deck that you want to add the cards to
        """
        for i in range(card_count):
            new_card = BattleCard(name=f"Card {i}", description="Bog Standard")
            new_card.generate(random.randint(1, 3), is_player_deck)
            #deck.append(new_card)

        factory_cards = CardFactory.get_list_of_entities(is_player_deck)
        for i in range(card_count):
            new_card = CardFactory.get_entity_by_name(random.choice(factory_cards))
            deck.append(new_card)

    def do_attack(self, attacker_card: BattleCard, attacker: BaseCharacter, defender_card: BattleCard,
                  defender: BaseCharacter):
        """
        Perform an attack on a defender using teh specified attack and defend cards
        :param attacker_card: The card that the attacker is going to use
        :param attacker: The attacker
        :param defender_card: The card that the defender is going to use
        :param defender: The defender
        """
        print(f"\n{attacker.name} attacks {defender.name}...")
        attacker.print()
        attacker_card.print()
        defender.print()
        defender_card.print()

        attempted_attacks = 0
        succeeded_attacks = 0
        suceeded_blocks = 0

        # If the attacker is awake...
        if attacker.is_sleeping == False:

            # Attempt all of the element attacks in the attackers card
            for attack, attack_count in attacker_card.attacks.items():

                # If numebr of attacks is 0 then loop
                if attack_count < 1:
                    continue

                # Log event
                # self.events.add_event(Event(type=Event.BATTLE,
                #                             name=Event.ACTION_INFO,
                #                             description=f"{attacker.name} attacks {defender.name} with {attack.value}"))

                attempted_attacks += attack_count

                # For this attack, how many blocks does the defender have?
                # If attack is unblockable then 0 blocks
                # If defender is sleeping then 0 blocks
                block = Battle.ATTACK_BLOCKS[attack]
                block_count = defender_card.blocks.get(block, 0) * (attacker_card.is_attack_unblockable == False) * (
                            defender.is_sleeping == False)

                # Calculate the damage of the attack which must not be negative.
                damage = max(attack_count - block_count, 0)

                # Update attacks and blocks stats
                succeeded_attacks += damage
                suceeded_blocks += (attack_count * (damage == 0))

                # Print the results of the defender's block
                if block_count > 0:
                    print(f"{defender.name} blocks {min(block_count, attack_count)} {attack.value}(s)")

                    # Log event
                    if defender.is_player:
                        ename = Event.PLAYER_INFO
                    else:
                        ename = Event.ENEMY_INFO

                    self.events.add_event(Event(type=Event.BATTLE,
                                                name=ename,
                                                description=f"{defender.name} blocks {min(block_count, attack_count)} of {attacker.name}'s {attack.value}(s)"))

                # Print the results of the attacker's attack
                if damage > 0:
                    # If defender is invincible then damage = 0
                    if defender.is_invincible:
                        damage = 0
                        print(f"{defender.name} is Invincible!")
                    else:
                        defender.health -= damage

                    print(f"{attacker.name}'s {attack.value} does {damage} damage")
                    # Log event
                    if attacker.is_player:
                        ename = Event.PLAYER_INFO
                    else:
                        ename = Event.ENEMY_INFO
                    self.events.add_event(Event(type=Event.BATTLE,
                                                name=ename,
                                                description=f"{attacker.name}'s {attack.value} does {damage} damage to {defender.name}"))

        else:
            print(f"{attacker.name} is asleep ZZZZzzzzz")
            # Log event
            if attacker.is_player:
                ename = Event.PLAYER_INFO
            else:
                ename = Event.ENEMY_INFO
            self.events.add_event(Event(type=Event.BATTLE,
                                        name=ename,
                                        description=f"{attacker.name} is asleep ZZZzzzzzz"))

        print(f"attack success={succeeded_attacks}/{attempted_attacks} blocks={suceeded_blocks}")

        return succeeded_attacks, attempted_attacks, suceeded_blocks

    def do_round(self):
        """
        Do a round in the battle
        :return:
        """
        if self.is_game_over:
            print("Battle is over!")
            for c in [self.player, self.enemy]:
                if c.is_dead:
                    print(f"{c.name} the {c.type} is dead!")
            return

        results = {}

        # Get a new card from player's hand
        self.player_round_card = self.player_cards.play_card(self.player_selected_card)

        # Get a new card from enemy's hand
        self.enemy_round_card = self.enemy_cards.play_card(self.enemy_selected_card)

        assert self.player_round_card is not None, "The Player has not picked a card for this round"
        assert self.enemy_round_card is not None, "The Enemy has not picked a card for this round"

        # See if the player is going first...
        if self.player_round_card.is_quick:
            results["Player"] = self.do_attack(self.player_round_card, self.player, self.enemy_round_card, self.enemy)
            if self.enemy.is_dead == False:
                results["Enemy"] = self.do_attack(self.enemy_round_card, self.enemy, self.player_round_card,
                                                  self.player)
        # Else the enemy goes first
        else:
            results["Enemy"] = self.do_attack(self.enemy_round_card, self.enemy, self.player_round_card, self.player)
            results["Player"] = self.do_attack(self.player_round_card, self.player, self.enemy_round_card, self.enemy)

        # Add any bonus or penalty to the number of cards a player is allowed in their hand
        self.player.cards_per_hand += self.player_round_card.new_card_count
        self.player.cards_per_hand -= self.enemy_round_card.new_card_count

        # Cap and floor the number of cards that a player is allowed to hold
        self.player.cards_per_hand = max(self.player.cards_per_hand, 1)
        self.player.cards_per_hand = min(self.player.cards_per_hand, self.player_max_cards_per_hand)

        # Heal the player if applicable
        succeeded_attacks, attempted_attacks, succeeded_blocks = results.get("Player",(0,0,0))
        for k, v in self.player_round_card.heals.items():

            logging.info(f"Attempting Player heal if {k}={v}...")
            logging.info(f"{succeeded_attacks}/{attempted_attacks} attacks; {succeeded_blocks} blocks")
            # Heal in every outcome
            if k == Outcome.ALL:
                heal_amount = v
            # Heal if we landed a hit
            elif k == Outcome.HIT:
                heal_amount = v * (succeeded_attacks > 0)
            # Heal if we landed ALL hits
            elif k == Outcome.HIT_ALL:
                heal_amount = v * (succeeded_attacks == attempted_attacks)
            # Heal if we blocked
            elif k == Outcome.BLOCK:
                heal_amount = v * (succeeded_blocks > 0)
            # Heal if we landed ALL hits
            elif k == Outcome.BLOCK_ALL:
                heal_amount = v * (succeeded_blocks == attempted_attacks)
            # Looks like nothing happened?
            else:
                print("How did we end up here?")
                heal_amount = 0

            self.player.health += heal_amount

            if heal_amount > 0:
                logging.info(f"Player healed by {heal_amount}")
                self.events.add_event(Event(type=Event.BATTLE,
                                            name=Event.PLAYER_INFO,
                                            description=f"{self.player.name} healed by {heal_amount}"))
            elif heal_amount < 0:
                logging.info(f"Player is drained by {abs(heal_amount)}")
                self.events.add_event(Event(type=Event.BATTLE,
                                            name=Event.PLAYER_INFO,
                                            description=f"{self.player.name} drained by {abs(heal_amount)}"))


        # Heal the enemy if applicable
        succeeded_attacks, attempted_attacks, succeeded_blocks = results.get("Enemy",(0,0,0))

        for k, v in self.enemy_round_card.heals.items():

            logging.info(f"Attempting Enemy heal if {k}={v}...")
            # Heal in every outcome
            if k == Outcome.ALL:
                heal_amount = v
            # Heal if we landed a hit
            elif k == Outcome.HIT:
                heal_amount = v * (succeeded_attacks > 0)
            # Heal if we landed ALL hits
            elif k == Outcome.HIT_ALL:
                heal_amount = v * (succeeded_attacks == attempted_attacks)
            # Heal if we blocked
            elif k == Outcome.BLOCK:
                heal_amount = v * (succeeded_blocks > 0)
            # Heal if we blocked ALL hits
            elif k == Outcome.BLOCK_ALL:
                heal_amount = v * (succeeded_blocks == attempted_attacks)
            # Looks like nothing happened?
            else:
                print("How did we end up here?")
                heal_amount = 0

            self.enemy.health += heal_amount

            if heal_amount > 0:
                logging.info(f"Enemy healed by {heal_amount}")
                self.events.add_event(Event(type=Event.BATTLE,
                                            name=Event.ENEMY_INFO,
                                            description=f"{self.enemy.name} healed by {heal_amount}"))
            elif heal_amount < 0:
                logging.info(f"Enemy is drained by {abs(heal_amount)}")
                self.events.add_event(Event(type=Event.BATTLE,
                                            name=Event.PLAYER_INFO,
                                            description=f"{self.enemy.name} drained by {abs(heal_amount)}"))

        # Apply effects to player if Player outcomes match...
        # Get the results of the Player action
        succeeded_attacks, attempted_attacks, succeeded_blocks = results.get("Player",(0,0,0))

        # Loop through the effects that are on the Player's Battle Card
        for k, v in self.player_round_card.effects.items():

            logging.info(f"Attempting to add effect {v.name} to Player if outcome = {k}...")
            # Every outcome
            if k == Outcome.ALL:
                success = True
            # If we landed a hit
            elif k == Outcome.HIT:
                success = (succeeded_attacks > 0)
            # If we landed ALL hits
            elif k == Outcome.HIT_ALL:
                success = (succeeded_attacks == attempted_attacks)
            # If we blocked
            elif k == Outcome.BLOCK:
                success = (succeeded_blocks > 0)
            # If we blocked ALL hits
            elif k == Outcome.BLOCK_ALL:
                success = (succeeded_blocks == attempted_attacks)
            # Looks like nothing happened?
            else:
                success = False

            # If the Player outcome succeeded then add the effect to the player
            if success:
                logging.info(f"Effect {v.name} added to Player")
                self.player.add_effect(v)
                self.events.add_event(Event(type=Event.BATTLE,
                                            name=Event.PLAYER_INFO,
                                            description=f"{self.player.name} is now {v.value}"))
            else:
                logging.info(f"Failed to add effect {v.name} to Player")

        # Get the results of the Enemy action
        succeeded_attacks, attempted_attacks, succeeded_blocks = results.get("Enemy",(0,0,0))

        # Loop through the effects that are on the Enemy's Battle Card
        for k, v in self.enemy_round_card.effects.items():

            logging.info(f"Attempting to add effect {v.name} to Player if outcome = {k}...")
            # Every outcome
            if k == Outcome.ALL:
                success = True
            # If we landed a hit
            elif k == Outcome.HIT:
                success = (succeeded_attacks > 0)
            # If we landed ALL hits
            elif k == Outcome.HIT_ALL:
                success = (succeeded_attacks == attempted_attacks)
            # If we blocked
            elif k == Outcome.BLOCK:
                success = (succeeded_blocks > 0)
            # If we blocked ALL hits
            elif k == Outcome.BLOCK_ALL:
                success = (succeeded_blocks == attempted_attacks)
            # Looks like nothing happened?
            else:
                success = False

            # If the Enemy outcome succeeded then add the effect to the player
            if success:
                logging.info(f"Effect {v.name} added to Player")
                self.player.add_effect(v)
                self.events.add_event(Event(type=Event.BATTLE,
                                            name=Event.PLAYER_INFO,
                                            description=f"{self.player.name} is now {v.value}"))
            else:
                logging.info(f"Failed to add effect {v.name} to Player")

        # Log event if player died
        if self.player.is_dead:
            self.events.add_event(Event(type=Event.BATTLE,
                                        name=Event.PLAYER_INFO,
                                        description=f"{self.player.name} the {self.player.type.value} is dead!"))

        # Log event if enemy died
        if self.enemy.is_dead:
            self.events.add_event(Event(type=Event.BATTLE,
                                        name=Event.ENEMY_INFO,
                                        description=f"{self.enemy.name} the {self.enemy.type.value} is dead!"))

        # Discard cards from the player's hand based on enemy hits
        for i in range(self.enemy_round_card.new_card_count):
            self.player_cards.play_card()

        # Log end of round event
        self.events.add_event(Event(type=Event.BATTLE,
                                    name=Event.BATTLE_ROUND_OVER,
                                    description=f"End of round {self.round}"))

        self.is_round_complete = True

    def reset_round(self):

        # Replenish Player's hand with new cards
        self.player_cards.replenish(self.player.cards_per_hand)

        # Replenish Enemy's hand with new cards
        self.enemy_cards.replenish(self.enemy.cards_per_hand)

        # Reset the round cards
        self.player_round_card = None
        self.enemy_round_card = None
        self.player_selected_card = None

        # Select the first card in the enemy's hand
        self.enemy_selected_card = self.enemy_cards.default_hand_card

        # Clear event log
        self.events.clear()

        # Increment the count of completed rounds
        self.round += 1
        self.player.tick()
        self.player.rounds += 1

        self.enemy.tick()
        self.enemy.rounds += 1

        # Flag that indicates if a round has finished or not
        self.is_round_complete = False


def test():
    print(f"\nTesting {__file__}\n")

    p = PlayerCharacter(name="Keith", type="Warrior")
    npc = EnemyCharacter(name="George", type="Goblin")

    b = Battle(player=p, enemy=npc)
    b.initialise()
    b.print()

    b.start()


if __name__ == "__main__":
    test()
