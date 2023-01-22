import simpy

from config import DEBUG, MOCK
from entity import Queue
from runners import JobLoader, Layer2queue, ResultCreator, Scheduler

TIME_PARTS = 0.5

T1 = 5
T2 = 10
K = 3
# Inputs
if not MOCK:
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
    priority_queue = Queue()
    layer2queue = Layer2queue(env, T1, T2)
    tranform_worker = JobLoader(env, K, TIME_PARTS, priority_queue, layer2queue)
    poper = Scheduler(env, x, y, priority_queue)
    result_creator = ResultCreator(env, priority_queue)

    env.run(until=simulation_time)
