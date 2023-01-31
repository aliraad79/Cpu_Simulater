import numpy as np

from enums import Level
from helper import generate_priority


class Task:
    def __init__(self, priority: Level, arrival_time, service_time) -> None:
        self.arrival_time = arrival_time
        self.priority = priority
        self.service_time = service_time
        self.remaining_time = service_time
        self.time_waited_in_layer1 = 0
        self.time_waited_in_layer2 = 0
        self.dumped = False

    def run_for_n_time(self, n):
        self.remaining_time -= n

    def is_done(self):
        return self.remaining_time <= 0

    def is_dumped(self):
        self.remaining_time = 0
        self.dumped = True

    def time_waited(self):
        return self.time_waited_in_layer1 + self.time_waited_in_layer2

    @classmethod
    def create_task(self, y, arrival_time) -> "Task":
        service_time = np.random.exponential(y, size=1)[0]
        level = generate_priority()

        return Task(level, arrival_time, service_time)

    def __str__(self) -> str:
        return (
            f"Task<arrival={self.arrival_time} service={self.service_time} remaining_time={self.remaining_time} "
            + f"wait_1={self.time_waited_in_layer1} wait_2={self.time_waited_in_layer2}>"
        )

    def __repr__(self) -> str:
        return self.__str__()


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

    def pop_n_priority_item(self, n):
        self.q.sort(key=lambda x: x.priority.value, reverse=True)
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
        task: Task = self.q.pop()
        return task, min(self.time, task.remaining_time)


class FCFSQueue(TimedQueue):
    def get_job_with_wait_time(self):
        task: Task = self.q.pop()
        return task, task.service_time
