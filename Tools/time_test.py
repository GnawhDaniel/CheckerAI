import time
import subprocess

ITER = 5
time_list = []
for i in range(ITER):
    start = time.time()
    subprocess.run(['python3.5', 'AI_Runner.py', '8', '8', '2', 'l', '/home/daniel/cs171/CheckerAI/Tools/Sample_AIs/Average_AI/main.py', '/home/daniel/cs171/CheckerAI/src/checkers-python/main.py'])
    end = time.time()
    time_list.append(end-start)


print("Average seconds: ", sum(time_list) / len(time_list))
for i in range(1, len(time_list)+1):
    print("Iter %d: %f\n" % (i, time_list[i-1]))
