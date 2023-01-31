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
    for t1 in [1, 2, 3, 5]:
        for t2 in [8, 10, 12]:
            np.random.seed(235)
            random.seed(235)
            print(
                f"-------------------------- Optimization Run with T1={t1} T2={t2} --------------------------"
            )
            run_simulation(Update_Intervals, t1, t2, K, x, y, tasks_count, simulation_time)
