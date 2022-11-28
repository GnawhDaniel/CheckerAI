import time
import subprocess

ITER = 2
k = 2
AI = "Poor_AI"

time_dict = {
    "1_7": [],
    "2_7": [],
    "1_8": [],
    "2_8": []
}

for size in [7, 8]:
    print(f"Board Size: {size} x {size} k={k}")
    for mode in [1, 2]:
        if mode == 1:
            print(f"  1: StudentAI vs. 2: {AI}")
        else:
            print("  1. {AI} AI vs 2. StudentAI")
        for i in range(ITER):
            start = time.time()
            if (mode == 1):
                subprocess.run(['python3.5', 'AI_Runner.py', f"{size}", f"{size}", f"{k}", 'l', '/home/hwang/cs171/CheckerAI/src/checkers-cpp/main', f'/home/hwang/cs171/CheckerAI/Tools/Sample_AIs/{AI}/main.py'])
            elif (mode == 2):
                subprocess.run(['python3.5', 'AI_Runner.py', f"{size}", f"{size}", f"{k}", 'l', f'/home/hwang/cs171/CheckerAI/Tools/Sample_AIs/{AI}/main.py', '/home/hwang/cs171/CheckerAI/src/checkers-cpp/main'])
            end = time.time()

            time_dict[f"{mode}_{size}"].append(end-start)
        
        for t in time_dict[f"{mode}_{size}"]:
            print(f"    {t:.2f} seconds.")
        print("    Avg:", round(sum(time_dict[f"{mode}_{size}"])/ITER, 2), "seconds.")

        
        






