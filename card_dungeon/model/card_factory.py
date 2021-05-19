import logging
from pathlib import Path
import pandas as pd
from card_dungeon.model.battle_cards import *


class CardFactory():
    CARDS = None
    PLAYER_CARDS = None
    ENEMY_CARDS = None
    CARDS_BY_LEVEL = {}

    def __init__(self):
        pass

    @staticmethod
    def load(file_name: str):

        # Create path for the file that we are going to load
        data_folder = Path(__file__).resolve().parent
        file_to_open = data_folder / "data" / file_name

        # Read in the csv file
        CardFactory.CARDS = pd.read_csv(file_to_open)
        df = CardFactory.CARDS
        df.set_index("Name", drop=True, inplace=True)

        # Convert a bunch of columns to integer data type
        int_columns = ["Is Player", "Melee Attack", "Magic Attack", "Melee Block", "Magic Block", "Quick",
                       "Unblockable", "Heal", "Extra Card"]
        df[int_columns] = df[int_columns].apply(pd.to_numeric)
        df[int_columns] = df[int_columns].fillna(0)
        for col in int_columns:
            df[col] = df[col].astype(int)

        # Set boolean columns
        df["Quick"] = df["Quick"] > 0
        df["Unblockable"] = df["Unblockable"] > 0
        df["Is Player"] = df["Is Player"] > 0
        df["Is Enemy"] = df["Is Enemy"] > 0

        # Build lists of player and enemy cards
        CardFactory.PLAYER_CARDS = list(df[df["Is Player"] == True].index)
        CardFactory.ENEMY_CARDS = list(df[df["Is Enemy"] == True].index)

        print(df.head())
        print(df.dtypes)

    @staticmethod
    def get_list_of_entities(player_cards_only: bool = False) -> list:

        assert CardFactory.CARDS is not None, "No entities have been loaded!"

        if player_cards_only is True:
            return CardFactory.PLAYER_CARDS
        else:
            return CardFactory.ENEMY_CARDS

    @staticmethod
    def get_entity_by_name(name: str) -> BaseCard:

        assert CardFactory.CARDS is not None, "No entities have been loaded!"

        e = None

        # Check if the specified entity is in the factory...
        if name in list(CardFactory.CARDS.index):

            # Get the entity details from teh Data Frame
            row = CardFactory.CARDS.loc[name]

            # Create a basic BattleCard
            e = BattleCard(name=name, description=row["Description"])

            # Add features to thE basic card according to what is in the data frame
            e.is_attack_unblockable = (row["Unblockable"] == True)
            e.is_quick = (row["Quick"] == True)
            e.new_card_count = row["Extra Card"]
            e.slot = enum_value_to_key(CharacterSlot, row["Slot"], default=CharacterSlot.NONE)

            e.attacks[CardFeature.ATTACK_MELEE] = row["Melee Attack"]
            e.attacks[CardFeature.ATTACK_MAGIC] = row["Magic Attack"]
            e.blocks[CardFeature.BLOCK_MELEE] = row["Melee Block"]
            e.blocks[CardFeature.BLOCK_MAGIC] = row["Magic Block"]

            # If there a Heal feature for this card?
            heal_value = row["Heal"]
            if heal_value != 0:

                # See if there is a condition for the heal
                condition = row["Heal Condition"]
                heal_outcome = enum_value_to_key(Outcome, condition, Outcome.NEVER)
                if heal_outcome != Outcome.NEVER:
                    e.heals[heal_outcome] = row["Heal"]
                else:
                    logging.info(
                        f"Card {name}: Failed adding Heal feature because of unrecognised condition '{condition}'")

            # Is there and Effect?
            effect = row["Effect"]

            # If the effect name looks like a string...
            if type(effect) == str:

                # Attempt to map the effect name to Effect Enum
                effect_name = enum_value_to_key(Effect, effect)

                # If we successfully mapped it...
                if effect_name is not None:

                    # Add the condition that must be met for the Effect to apply
                    condition = row["Effect Condition"]
                    effect_outcome = enum_value_to_key(Outcome, condition, Outcome.NEVER)

                    # Did we recognise the condition?
                    if effect_outcome != Outcome.NEVER:
                        e.effects[effect_outcome] = effect_name
                    else:
                        logging.info(
                            f"Card {name}:Failed adding effect '{effect}' because of unrecognised condition '{condition}'")
                else:
                    logging.info(f"Card {name}:Failed adding effect '{effect}' as not recognised Effect")
        else:
            logging.info(f"Can't find entity {name} in factory!")

        return e


def test():
    logging.basicConfig(level=logging.INFO)

    CardFactory.load("items.csv")
    objects = CardFactory.get_list_of_entities()
    for o in objects:
        e = CardFactory.get_entity_by_name(o)
        e.print()


if __name__ == "__main__":
    test()
