import numpy as np

from enums import Level
from helper import generate_priority


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

    def __str__(self) -> str:
        return f"Task<arrival={self.arrival_time} service={self.service_time} remaining_time={self.remaining_time}>"


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
        # I ask a question in forums and after the answer this can be changed
        task: Task = self.q.pop()
        return task, min(self.time, task.remaining_time)


class FCFSQueue(TimedQueue):
    def get_job_with_wait_time(self):
        task: Task = self.q.pop()
        return task, task.service_time
