from random import randint

import numpy as np

from enums import Level


class Task:
    def __init__(self, priority: Level, arrival_time, service_time) -> None:
        self.arrival_time = arrival_time
        self.priority = priority
        self.service_time = service_time
        self.remaining_time = service_time

    def run_for_n_time(self, n):
        self.remaining_time -= n

    def is_done(self):
        return self.remaining_time <= 0

    @classmethod
    def create_task(self, y, arrival_time) -> "Task":
        service_time = np.random.exponential(y, size=1)[0]
        level = generate_priority()

        return Task(level, arrival_time, service_time)


class Queue:
    def __init__(self) -> None:
        self.q = []

    def add_to_queue(self, item):
        if isinstance(item, list):
            self.q.extend(item)
        else:
            self.q.append(item)

    def pop_fifo(self):
        return self.q.pop(0)

    def pop(self, n):
        return self.q.pop(n)

    def pop_n_item(self, n):
        items = self.q[:n]
        del self.q[:n]
        return items

    def __len__(self):
        return len(self.q)


class TimedQueue(Queue):
    def get_job_with_wait_time(self) -> tuple[Task, int]:
        raise NotImplementedError()


class RRQueue(TimedQueue):
    def __init__(self, time) -> None:
        super().__init__()
        self.time = time

    def get_job_with_wait_time(self):
        return self.q.pop(), self.time


class FCFSQueue(TimedQueue):
    def get_job_with_wait_time(self):
        task: Task = self.q.pop()
        return task, task.service_time


def generate_priority():
    rand = randint(1, 10)
    if 1 <= rand <= 7:
        level = Level.LOW
    elif 8 <= rand <= 9:
        level = Level.Normal
    elif 10 <= rand <= 10:
        level = Level.High
    return level
