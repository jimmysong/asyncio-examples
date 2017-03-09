import json
import requests
import sys
import threading
import time


STATS = {}


def get_website_status(url, lock):
    response = requests.get(url)
    status = response.status_code
    if status != 200:
        print(url)
    lock.acquire()
    if not STATS.get(status):
        STATS[status] = 0
    STATS[status] += 1
    lock.release()


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        websites = f.read().splitlines()
    t0 = time.time()
    threads = []
    lock = threading.Lock()
    for website in websites:
        t = threading.Thread(target=get_website_status, args=(website, lock))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    t1 = time.time()
    print(json.dumps(STATS))
    print("getting website statuses took {0:.1f} seconds".format(t1-t0))
