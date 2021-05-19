from pathlib import Path
import pandas as pd
import math
from card_dungeon.model.battle_cards import *


class CardFactory():

    CARDS = None

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
        int_columns = ["Melee Attack","Magic Attack","Melee Block","Magic Block", "Quick", "Unblockable","Heal","Extra Card"]
        df[int_columns] = df[int_columns].apply(pd.to_numeric)
        df[int_columns] = df[int_columns].fillna(0)

        print(df.head())
        print(df.dtypes)

    @staticmethod
    def get_entity_by_name(name: str) -> BaseCard:

        assert CardFactory.CARDS is not None, "No entities have been loaded!"

        e = None
        if name in list(CardFactory.CARDS.index):
            row = CardFactory.CARDS.loc[name]

            e = CardFactory.entity_from_row(name, row)

            e.is_attack_unblockable = row["Unblockable"] > 0
            e.is_quick = row["Quick"] > 0
            e.new_card_count = row["Extra Card"]

            e.attacks[CardFeature.ATTACK_MELEE] = row["Melee Attack"]
            e.attacks[CardFeature.ATTACK_MAGIC] = row["Magic Attack"]
            e.blocks[CardFeature.BLOCK_MELEE] = row["Melee Block"]
            e.blocks[CardFeature.BLOCK_MAGIC] = row["Magic Block"]

            heal_value = row["Heal"]
            if heal_value > 0:
                heal_outcome = Outcome._value2member_map_[row["Heal Condition"]]
                e.heals[heal_outcome] = row["Heal"]

            effect = row["Effect"]
            if effect is not None:
                effect_name = Effect._value2member_map_[effect]
                effect_outcome = Outcome._value2member_map_[row["Effect Condition"]]
                e.effects[effect_outcome] = effect_name


        else:
            print(f"Can't find entity {name} in factory!")

        return e

    @staticmethod
    def entity_from_row(index, row) -> BaseCard:

        name = index
        e = BattleCard(name=name)

        return e

def test():
    CardFactory.load("items.csv")
    e = CardFactory.get_entity_by_name("Sword")
    e.print()

    e = CardFactory.get_entity_by_name("Cuirass")
    e.print()




if __name__ == "__main__":
    test()