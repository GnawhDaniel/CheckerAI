import time
import subprocess

ITER = 5
time_list = []
for i in range(ITER):
    start = time.time()
    subprocess.run(['python3.5', 'AI_Runner.py', '8', '8', '3', 'l', '/home/hwang/cs171/CheckerAI/src/checkers-cpp/main', '/home/hwang/cs171/CheckerAI/Tools/Sample_AIs/Random_AI/main.py'])
    end = time.time()
    time_list.append(end-start)


print("Average seconds: ", sum(time_list) / len(time_list))
for i in range(1, len(time_list)+1):
    print("Iter %d: %f\n" % (i, time_list[i-1]))
