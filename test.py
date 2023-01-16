import simpy
import numpy as np


class Queue(object):
    def __init__(self, env) -> None:
        self.env = env

        self.q = []
        self.i = 0

        self.action = env.process(self.run())

    def run(self):
        while True:
            print("Create Task at %d" % env.now)
            charge_duration = np.random.poisson(5, size=1)[0]

            self.q.append(f"T{self.i}")
            self.i += 1

            try:
                yield self.env.timeout(np.inf)
            except simpy.Interrupt:
                ...


class Poper:
    def __init__(self, env, queue: Queue) -> None:
        self.env = env
        self.queue = queue

        self.action = env.process(self.run())

    def run(self):
        while True:
            diff = np.random.exponential(2, size=1)[0]
            yield self.env.timeout(diff)
            print(self.queue.q.pop(0))
            self.queue.action.interrupt()

from random import choice
print(choice([]))
