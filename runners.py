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

        self.is_cpu_busy = False
        self.finalized_tasks: list[Task] = []

        self.action = env.process(self.run())

    def number_of_task_in_all_queues(self):
        return len(self.q1) + len(self.q2) + len(self.q3)

    def add_tasks(self, tasks):
        self.q1.add_to_queue(tasks)

    def get_all_tasks(self) -> list[Task]:
        return [*self.q1.q, *self.q2.q, *self.q3.q]

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
            self.is_cpu_busy = True
            yield self.env.timeout(time)
            self.is_cpu_busy = False
            task.run_for_n_time(time)

            if not task.is_done():
                next_queue.add_to_queue(task)
            else:
                self.finalized_tasks.append(task)
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
            # Load jobs from priority queue to main queues
            if len(self.priority_queue.q) > 0:
                if self.layer_2_queue.number_of_task_in_all_queues() < self.k:
                    # Pop from layer 1 and move to layer 1
                    tasks = self.priority_queue.pop_n_item(
                        self.k - self.layer_2_queue.number_of_task_in_all_queues()
                    )

                    self.layer_2_queue.add_tasks(tasks)


class JobCreator:
    def __init__(self, env, x, y, priority_queue: Queue, tasks_count) -> None:
        self.env = env
        self.priority_queue = priority_queue

        self.x = x
        self.y = y
        self.tasks_count = tasks_count
        self.created_tasks = 0

        self.action = env.process(self.run())

    def run(self):
        while True:
            # Add task to priority queue
            next_arrival = np.random.poisson(self.x, size=1)[0]
            yield self.env.timeout(next_arrival)
            # Add to priority queue
            self.priority_queue.q.append(Task.create_task(self.y, self.env.now))
            # Break After max number of tasks reached
            self.created_tasks += 1
            if self.created_tasks == self.tasks_count:
                break


class ResultCreator:
    def __init__(self, env, priority_queue, layer2queue) -> None:
        self.env = env
        self.priority_queue: Queue = priority_queue
        self.layer2queue: Layer2queue = layer2queue

        self.queue_length = []
        self.is_cpu_busy = []
        self.action = env.process(self.run())

    def run(self):
        while True:
            yield self.env.timeout(1)
            self.queue_length.append(len(self.priority_queue))
            self.is_cpu_busy.append(self.layer2queue.is_cpu_busy)

            # Add time to tasks in priority queue
            for i in self.priority_queue.q:
                i.time_waited_in_layer1 += 1
            # Add time to tasks in layer 2 tasks
            for i in self.layer2queue.get_all_tasks():
                i.time_waited_in_layer2 += 1

    def print_results(self):
        print(
            "Avarage Queue Length -> ",
            round(sum(self.queue_length) / len(self.queue_length), 3),
        )

        wait_in_line1, wait_in_line2 = self.calc_wait_in_lines()
        print(
            "Avarage Time in line 1 -> ",
            round(wait_in_line1 / len(self.layer2queue.finalized_tasks), 3),
        )
        print(
            "Avarage Time in line 2 -> ",
            round(wait_in_line2 / len(self.layer2queue.finalized_tasks), 3),
        )

        print(
            "Cpu utilization -> ",
            round(sum(self.is_cpu_busy) / len(self.is_cpu_busy), 3),
        )

    def calc_wait_in_lines(self):
        wait_in_line1 = 0
        wait_in_line2 = 0
        for i in self.layer2queue.finalized_tasks:
            wait_in_line1 += i.time_waited_in_layer1
            wait_in_line2 += i.time_waited_in_layer2
        return wait_in_line1, wait_in_line2
