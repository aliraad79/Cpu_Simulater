import random

import numpy as np
import simpy


from config import MOCK, OPTIMIZE

from entity import Queue

from runners import JobCreator, JobLoader, Layer2queue, ResultCreator

Update_Intervals = 0.5

T1 = 5
T2 = 10
K = 3
# Inputs
if not MOCK:
    x, y, z = map(int, input().split())
    tasks_count = int(input())
    simulation_time = int(input())
else:
    x, y, z = 2, 5, 1
    tasks_count = 10
    simulation_time = 90


# Logic
def run_simulation(TIME_PARTS, T1, T2, K, x, y,z, tasks_count, simulation_time):
    env = simpy.Environment()
    priority_queue = Queue()
    layer2queue = Layer2queue(env,z, T1, T2)
    tranform_worker = JobLoader(env, K, TIME_PARTS, priority_queue, layer2queue)
    job_creator = JobCreator(env, x, y, priority_queue, tasks_count)
    result_creator = ResultCreator(env, priority_queue, layer2queue)

    env.run(until=simulation_time)

    result_creator.print_results()


np.random.seed(2322)
random.seed(2322)

for i in range(5):
    print(f"-------------------------- Run {i} --------------------------")
    run_simulation(Update_Intervals, T1, T2, K, x, y,z, tasks_count, simulation_time)


# Optimizer

if OPTIMIZE:

    for i, t in enumerate([(5, 10), (5, 8), (5, 12), (2, 10), (2, 8), (2, 12)]):
        print(

            f"-------------------------- Optimization Run with T1={t[0]} T2={t[1]} --------------------------"
        )
        run_simulation(Update_Intervals, t[0], t[1], K, x, y,z, tasks_count, simulation_time)

