from enum import Enum


class Level(Enum):
    LOW = 1
    Normal = 2
    High = 3

class Queue(Enum):
    Round_Robin_T1 = 1
    Round_Robin_T2 = 2
    FCFS = 3