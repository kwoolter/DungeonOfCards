# Dungeon Of Cards
:copyright: :monkey: kwoolter 2021
Card game based on Guild of Dungeoneering concept.
Thanks to GAMBRIBNOUS for inspiration and borrowing graphics.


## Graphics Version
`run_gui.py` pygame GUI to play the game.
Typical flow of the game:-
* `SPACE` to start a game
* `1` - `4` to select a card that you want to play next
* `Enter` to play a round with the selected card
* Repeat until someone dies

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
## Player and NPCs
TBC

## Battle Cards
Battle cards have the following features:-
* Attack - physical or magical
* Block -  physical or magical
* Unblockable - the attack is unblockable
* Quick - a quick attack goes ahead of the opponent's turn
* Healing - the player is healed dependent on an outcome e.g. successful block
* Effects - an effect is added to the card that is dependent on an outcome e.g. successful attack
* Dealing - the player receives or loses cards in their hand

The `BattleCard.generate(n)` method will generate a random card with `n` features added.

## Player Effects
* Decay - lose 1 health per round
* Blessed - gain 1 health per round
* Burning - lose 1 health per round
* Invincible - enemy attacks do no damage
* Sleep - player neither attacks nor blocks
* Confused - you can't see the cards in your own hand
* Blinded - you can't see the enemy's card

## Decks
Both the player and an enemy have the following:-
* Deck - a deck of hidden Battle Cards
* Hand - The hand of cards that have been dealt from the deck to play with in a round
* Discard pile - cards that have been used in a round and discarded

