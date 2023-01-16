from entity import Queue, RRQueue, Task




class Scheduler1:
    def __init__(self, T1, T2, x, y, max_time, k) -> None:
        self.priority_queue = Queue()
        self.RR_t1 = RRQueue(T1)
        self.RR_t2 = RRQueue(T2)
        self.fcfs = Queue()
        self.max_time = max_time
        self.k = k

        self.jobs_in_level2_queue = 0
        self.clock = 0

    def run(self):
        if self.tasks[0].arrival_time < self.clock:
            self.JobCreator(self.tasks.pop(0))

        if self.jobs_in_level2_queue < self.k:
            self.JobLoader()

    def JobCreator(self, task: Task):
        self.priority_queue.add_to_queue(task)

    def JobLoader(self):
        self.priority_queue.pop_n_item(self.k)

    def dispatcher(self):
        ...
        # if len(self.RR_t1) > 0:
