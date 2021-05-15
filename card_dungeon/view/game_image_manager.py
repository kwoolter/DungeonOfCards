from . view import *
from card_dungeon.model import PlayerType, EnemyType, CardFeature, CharacterFeature, Effect
import os
import logging

class DoCImageManager(ImageManager):

    def __init__(self):
        pass

    def initialise(self):
        if ImageManager.initialised is False:
            super().initialise()
            print("Initialising {0}".format(__class__))
            self.load_skins()
            self.load_sprite_sheets()

    def load_skins(self):

        new_skin_name = ImageManager.DEFAULT_SKIN
        new_skin = (new_skin_name, {

            PlayerType.CHUMP: ("Ginger.png","Rosie.png"),
            PlayerType.BARBARIAN: ("Ginger.png","Rosie.png"),
            PlayerType.WARRIOR: ("Ginger.png","Rosie.png"),

            EnemyType.RAT: "Rat.png",
            EnemyType.GHOST: "Ghost.png",
            EnemyType.GOBLIN: "Goblin.png",
            EnemyType.MIMIC: "Mimic.png",
            EnemyType.SCORPION: "Scorpion.png",
            EnemyType.PIGGY: "Wild_Piggy.png",
            EnemyType.RATMAN: "Ratman.png",
            EnemyType.SNAKE: "Snake.png",
            EnemyType.BUNNY: "Angry_Bunny.png",

            CharacterFeature.HEALTH: "heart_small.png",

            CardFeature.ATTACK_MAGIC: "attack_magic.png",
            CardFeature.ATTACK_MELEE: "attack_melee.png",
            CardFeature.BLOCK_MAGIC: "block_magic.png",
            CardFeature.BLOCK_MELEE: "block_melee.png",
            CardFeature.UNBLOCKABLE: "unblockable.png",
            CardFeature.QUICK: "quick.png",
            CardFeature.DEAL: "extra_card.png",
            CardFeature.HEAL: "heart.png",

            Effect.CONFUSED : "confused.png",
            Effect.SLEEP : "sleeping.png",
            Effect.BLIND : "blinded.png",
            Effect.DECAY : "decay.png",
            Effect.BURNING : "burning.png",
            Effect.BLESSED : "blessed.png",
            Effect.INVINCIBLE : "invincible.png"

        })

        ImageManager.skins[new_skin_name] = new_skin

    def load_sprite_sheets(self):

        sheet_file_name = "token.png"
        for i in range(0, 5):
            self.sprite_sheets["token{0}.png".format(i)] = (sheet_file_name, (i * 8, 0, 8, 8))
