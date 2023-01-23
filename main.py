import simpy

from config import DEBUG, MOCK
from entity import Queue
from runners import JobLoader, Layer2queue, ResultCreator, JobCreator

TIME_PARTS = 0.5

T1 = 5
T2 = 10
K = 3
# Inputs
if not MOCK:
    x, y, z = map(int, input().split())
    tasks_count = int(input())
    simulation_time = int(input())
else:
    x, y, z = 2, 5, 0
    tasks_count = 10
    simulation_time = 90


# Logic
for i in range(5):
    print(f"-------------------------- Run {i} --------------------------")
    env = simpy.Environment()
    priority_queue = Queue()
    layer2queue = Layer2queue(env, T1, T2)
    tranform_worker = JobLoader(env, K, TIME_PARTS, priority_queue, layer2queue)
    job_creator = JobCreator(env, x, y, priority_queue, tasks_count)
    result_creator = ResultCreator(env, priority_queue, layer2queue)

    env.run(until=simulation_time)

    result_creator.print_results()
