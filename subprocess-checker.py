import json
import math
import subprocess
import sys
import time


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        websites = f.read().splitlines()
    number_of_processes = int(sys.argv[2])
    per_process = math.ceil(len(websites) / number_of_processes)
    # split up the work based on number of processes
    for i in range(number_of_processes):
        sites = websites[i * per_process:(i + 1) * per_process]
        with open("/tmp/list-{}.txt".format(i), 'w') as f:
            f.write("\n".join(sites))
    t0 = time.time()
    processes = []
    for i in range(number_of_processes):
        p = subprocess.Popen(
            ["python3", "naive-checker.py", "/tmp/list-{}.txt".format(i)],
            stdout=subprocess.PIPE)
        processes.append(p)
    # gather the results
    combined = {}
    for process in processes:
        result = process.communicate()[0]
        stats, _, _ = result.decode().split("\n")
        for key, value in json.loads(stats).items():
            if not combined.get(key):
                combined[key] = 0
            combined[key] += value
    print(combined)
    t1 = time.time()
    print("getting website statuses took {0:.1f} seconds".format(t1-t0))
