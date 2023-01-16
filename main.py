import simpy

from runners import (Layer2queue, PriorityQueueRunner, Scheduler,
                     JobLoader)

DEBUG = True


TIME_PARTS = 0.5

T1 = 5
T2 = 10
K = 3
# Inputs
if not DEBUG:
    x, y, z = map(int, input().split())
    cpu_count = int(input())
    simulation_time = int(input())
else:
    x, y, z = 5, 3, 0
    cpu_count = 1
    simulation_time = 90


# Logic
# np.random.seed(176)
for i in range(5):
    print(f"-------------------------- Run {i} --------------------------")
    env = simpy.Environment()
    queue = PriorityQueueRunner(env)
    layer2queue = Layer2queue(env,T1,T2)
    tranform_worker = JobLoader(
        env, K, TIME_PARTS, queue, layer2queue
    )
    poper = Scheduler(env, x, y, queue)

    env.run(until=simulation_time)
