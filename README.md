# Dungeon Of Cards
:copyright: :monkey: kwoolter 2021
Card game based on Guild of Dungeoneering concept.

## CLI Version
Command Line Interface to test out the Model.
Typical flow of the game uses these commands:-
* `battle` to start the battle
* `hand` to see the player's hand and what the enemy has
* `pick` to select which card in the player's hand you want to use
* `round` play the round of the player versus the enemy
* `status` see how the player and enemy are doing
* Go back to the `hand` step
* Repeat until someone dies

## Graphics Version
TBC

# The Game
## Player and NPCs

## Battle Cards
Battle cards have the following features:-
* Attack - physical or magical
* Block -  physical or magical
* Unblockable - the attack is unblockable
* Quick - a quick attack goes ahead of the enemy's turn
* Healing - The player is healed
* Dealing - the player receives or loses cards in their hand

The `BattleCard.generate(n)` method will generate a random card with `n` features added.

## Decks
Both the player and an enemy have the following:-
* Deck - a deck of hidden Battle Cards
* Hand - The hand of cards that have been dealt from the deck to play with in a round
* Discard pile - cards that have been used in a round and discarded

