from random import choice

import numpy as np

from config import DEBUG
from entity import FCFSQueue, Queue, RRQueue, Task, TimedQueue


class Layer2queue(object):
    def __init__(self, env, T1, T2) -> None:
        self.env = env
        self.q1 = RRQueue(T1)
        self.q2 = RRQueue(T2)
        self.q3 = FCFSQueue()

        self.action = env.process(self.run())

    def number_of_task_in_all_queues(self):
        return len(self.q1) + len(self.q2) + len(self.q3)

    def add_tasks(self, tasks):
        self.q1.add_to_queue(tasks)

    def choice_queue(self) -> tuple[TimedQueue, TimedQueue]:
        not_empty_queues = []
        if len(self.q1) != 0:
            not_empty_queues.append(self.q1)
        if len(self.q2) != 0:
            not_empty_queues.append(self.q2)
        if len(self.q3) != 0:
            not_empty_queues.append(self.q3)

        if len(not_empty_queues) == 0:
            return None, None

        my_choice = choice(not_empty_queues)
        if my_choice == self.q1:
            return my_choice, self.q2
        elif my_choice == self.q2:
            return my_choice, self.q3
        elif my_choice == self.q3:
            return my_choice, None

    def run(self):
        while True:
            # Choose a queue
            selected_q, next_queue = self.choice_queue()
            if selected_q == None:
                # Bug must be fixed
                yield self.env.timeout(1)
                continue

            # Run task based on queue decipline
            task, time = selected_q.get_job_with_wait_time()
            yield self.env.timeout(time)
            task.run_for_n_time(time)

            if not task.is_done():
                next_queue.add_to_queue(task)
            else:
                if DEBUG:
                    print(f"Task: {task} is completed")


class JobLoader:
    def __init__(self, env, k, update_interval, priority_queue, layer_2_queue) -> None:
        self.env = env
        self.priority_queue: Queue = priority_queue
        self.layer_2_queue: Layer2queue = layer_2_queue

        self.update_interval = update_interval

        self.k = k

        self.action = env.process(self.run())

    def run(self):
        while True:
            yield self.env.timeout(self.update_interval)
            #
            if len(self.priority_queue.q) > 0:
                if self.layer_2_queue.number_of_task_in_all_queues() < self.k:
                    # Pop from layer 1 and move to layer 1
                    tasks = self.priority_queue.pop_n_item(
                        self.k - self.layer_2_queue.number_of_task_in_all_queues()
                    )

                    self.layer_2_queue.add_tasks(tasks)


class Scheduler:
    def __init__(self, env, x, y, priority_queue: Queue) -> None:
        self.env = env
        self.priority_queue = priority_queue

        self.x = x
        self.y = y

        self.action = env.process(self.run())

    def run(self):
        while True:
            # Add task to priority queue
            # JobCreator
            next_arrival = np.random.poisson(self.x, size=1)[0]
            yield self.env.timeout(next_arrival)
            self.priority_queue.q.append(Task.create_task(self.y, self.env.now))
            if DEBUG:
                print(
                    f"Add to priority queue at {self.env.now} | current queue length : {len(self.priority_queue.q)}"
                )


class ResultCreator:
    def __init__(self, env, priority_queue) -> None:
        self.env = env
        self.priority_queue = priority_queue

        self.action = env.process(self.run())

    def run(self):
        while True:
            yield self.env.timeout(1)
            # print(len(self.priority_queue))
