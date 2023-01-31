from random import randint

from enums import Level,Queue


def generate_priority():
    rand = randint(1, 10)
    if 1 <= rand <= 7:
        level = Level.LOW
    elif 8 <= rand <= 9:
        level = Level.Normal
    elif 9 <= rand <= 10:
        level = Level.High
    return level

def choose_queue(arr):
    rand = randint(1, 10)
    if 1 <= rand <= 8:
        queue = arr[0]
    elif 8 <= rand <= 9:
        queue = arr[1]
    elif 9 <= rand <= 10:
        queue = arr[2]
    return queue