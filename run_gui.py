import card_dungeon.controller as c
import logging


def main():

    logging.basicConfig(level = logging.INFO)
    cli = c.DoCGUIController()
    cli.initialise()
    cli.run()

if __name__ == "__main__":
    main()