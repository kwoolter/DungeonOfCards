# Dungeon Of Cards
:copyright: :monkey: kwoolter 2021
Card game based on Guild of Dungeoneering concept.
Thanks to GAMBRINOUS for inspiration and borrowing graphics.

## Graphics Version
`run_gui.py` pygame GUI to play the game.
Typical flow of the game:-
* `SPACE` to start a game
* `1` - `4` to select a card that you want to play next
* `Enter` to play a round with the selected card
* Repeat until someone dies

OR, use the mouse and just click on stuff.
## CLI Version
`run.py` Command Line Interface to test out the Model.
Typical flow of the game uses these commands:-
* `battle` to start the battle
* `hand` to see the player's hand and what the enemy has
* `pick` to select which card in the player's hand you want to use
* `round` play the round of the player versus the enemy
* `status` see how the player and enemy are doing
* Go back to the `hand` step
* Repeat until someone dies
# The Game
The game consists of Battles between a Player character and an Enemy character.
Each character has their own deck of Battle Cards that they can play to determine the next action of their character.
Each Battle starts by selecting a Player and an Enemy.  A Battle consists of a number of Rounds where each character 
picks which card they are going to play in that Round then the outcome of the Round is determined.  
If both character's survive the Round then new cards are dealt and a new Round starts 
If your Player survives a Battle then they move on to the next 
Battle with their health restored.  If they defeat an Enemy of the same of higher level then the Player levels up. 
If a Player dies in battle then a new Player is created to take on the challenge in the next Battle.

## Battle Cards
Battle cards have the following features:-

<table>
    <tr>
        <td><img src="https://github.com/kwoolter/DungeonOfCards/blob/Loot/card_dungeon/view/resources/attack_melee32x32.png?raw=true" align="center"></td>
        <td>Melee Attack</td>
        <td>Attempt a melee attack on the opponent</td>
    </tr>
    <tr>
        <td><img src="https://github.com/kwoolter/DungeonOfCards/blob/Loot/card_dungeon/view/resources/attack_magic32x32.png?raw=true" align="center"></td>
        <td>Magic Attack</td>
        <td>Attempt a magic attack on the opponent</td>
    </tr>
    <tr>
        <td><img src="https://github.com/kwoolter/DungeonOfCards/blob/Loot/card_dungeon/view/resources/block_melee32x32.png?raw=true" align="center"></td>
        <td>Melee Block</td>
        <td>Attempt to block an opponent's melee attack</td>
    </tr>
    <tr>
        <td><img src="https://github.com/kwoolter/DungeonOfCards/blob/Loot/card_dungeon/view/resources/block_magic32x32.png?raw=true" align="center"></td>
        <td>Magic Block</td>
        <td>Attempt to block an opponent's magic attack</td>
    </tr>
    <tr>
        <td><img src="https://github.com/kwoolter/DungeonOfCards/blob/Loot/card_dungeon/view/resources/unblockable32x32.png?raw=true" align="center"></td>
        <td>Unblockable Attack</td>
        <td>Indicates this attack connot be blocked by the opponent</td>
    </tr>
    <tr>
        <td><img src="https://github.com/kwoolter/DungeonOfCards/blob/Loot/card_dungeon/view/resources/quick32x32.png?raw=true" align="center"></td>
        <td>Quick Attack</td>
        <td>The Player can perform a quick attack ahead of the Enemy</td>
    </tr>
    <tr>
        <td><img src="https://github.com/kwoolter/DungeonOfCards/blob/Loot/card_dungeon/view/resources/heart32x32.png?raw=true" align="center"></td>
        <td>Healing</td>
        <td>The player is healed dependent on an outcome e.g. successful block</td>
    </tr>
    <tr>
        <td><img src="https://github.com/kwoolter/DungeonOfCards/blob/Loot/card_dungeon/view/resources/extra_card32x32.png?raw=true" align="center"></td>
        <td>Dealing</td>
        <td>The player receives or loses cards in their hand</td>
    </tr>
</table>


The `BattleCard.generate(n)` method will generate a random card with `n` features added.

## Player Effects
In addition a Battle Card can have an effect on the Player that lasts a number of turns.
<table>
    <tr>
        <td><img src="https://github.com/kwoolter/DungeonOfCards/blob/Loot/card_dungeon/view/resources/blessed32x32.png?raw=true" align="center"></td>
        <td>Blessed</td>
        <td>Gain 1 health per round</td>
    </tr>
    <tr>
        <td><img src="https://github.com/kwoolter/DungeonOfCards/blob/0024724b8d9f54ae0d70305ec1e44726ff8c3a2d/card_dungeon/view/resources/blinded32x32.png?raw=true" align="center"></td>
        <td>Blinded</td>
        <td>You can't see the enemy's card</td>
    </tr>
    <tr>
        <td><img src="https://github.com/kwoolter/DungeonOfCards/blob/Loot/card_dungeon/view/resources/burning32x32.png?raw=true" align="center"></td>
        <td>Burning</td>
        <td>Lose 1 health per round</td>
    </tr>
    <tr>
        <td><img src="https://github.com/kwoolter/DungeonOfCards/blob/Loot/card_dungeon/view/resources/confused32x32.png?raw=true" align="center"></td>
        <td>Confused</td>
        <td>You can't see the cards in your own hand</td>
    </tr>
    <tr>
        <td><img src="https://github.com/kwoolter/DungeonOfCards/blob/Loot/card_dungeon/view/resources/decay32x32.png?raw=true" align="center"></td>
        <td>Decay</td>
        <td>Lose 1 health per round</td>
    </tr>
    <tr>
        <td><img src="https://github.com/kwoolter/DungeonOfCards/blob/0024724b8d9f54ae0d70305ec1e44726ff8c3a2d/card_dungeon/view/resources/invincible32x32.png?raw=true" align="center"></td>
        <td>Invincible</td>
        <td>Enemy attacks do no damage to the Player</td>
    </tr>
    <tr>
        <td><img src="https://github.com/kwoolter/DungeonOfCards/blob/0024724b8d9f54ae0d70305ec1e44726ff8c3a2d/card_dungeon/view/resources/sleeping32x32.png?raw=true" align="center"></td>
        <td>Sleep</td>
        <td>The Player neither attacks nor blocks in the round</td>
    </tr>
</table>

## Decks
Both the player and an enemy have the following:-
* Deck - a deck of hidden Battle Cards
* Hand - The hand of cards that have been dealt from the deck to play with in a round
* Discard pile - cards that have been used in a round and discarded

