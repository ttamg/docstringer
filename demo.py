""" A simple demo to illustrate how docstringer works """
import logging
import random
import snoop

from docstringer import docstringer
from docstringer.formatters import (
    LoggerFormatter,
    EventListFormatter,
    DefaultFormatter,
    PrintSimpleFormatter,
)

snoop_formatted = snoop.Config(color=False, prefix="", columns=[]).snoop

formatter = PrintSimpleFormatter()

# # Using the LoggerFormatter ...
# logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
# formatter = LoggerFormatter(logging, "info")

# # Using the EventListFormatter ...
# event_list = []
# formatter = EventListFormatter(event_list)


@docstringer(formatter=formatter)
def roll_the_dice(rolls: int, sides: int = 6) -> tuple:
    """
    This is a function where we roll a number of dice.  

    Parameters:
    - rolls (int) - the number of dice to roll
    - sides (int) - the number of sides on the dice (default = 6)

    Returns a tuple of:
    - total score on all dice
    - a list of the dice rolls
    """

    results = []
    for _ in range(rolls):
        results.append(roll(sides))

    return (sum(results), results)


@docstringer(formatter=formatter)
@snoop_formatted
def roll(sides: int = 6) -> int:
    """
    An individual die roll.

    Parameters:
    - sides (int) - the number of sides on the dice (default = 6)

    Returns:
    - the value of the die roll
    """
    return random.randint(1, sides)


if __name__ == "__main__":
    """ Demo example to run """

    print("Hello world.  This is a very simple dice roll demo.")

    rolls = 2
    sides = 6
    result = roll_the_dice(rolls=rolls, sides=sides)

    print(f"I'm done.  The result was {result}.")

    # print("\n\n".join([str(e.__dict__) for e in event_list]))
