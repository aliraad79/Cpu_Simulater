from random import randint

from enums import Level


def generate_priority():
    rand = randint(1, 10)
    if 1 <= rand <= 7:
        level = Level.LOW
    elif 8 <= rand <= 9:
        level = Level.Normal
    elif 10 <= rand <= 10:
        level = Level.High
    return level
