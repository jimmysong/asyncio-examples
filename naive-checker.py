import json
import requests
import sys
import time


def website_statuses(websites):
    statuses = {}
    for website in websites:
        response = requests.get(website)
        status = response.status_code
        if not statuses.get(status):
            statuses[status] = 0
        statuses[status] += 1
    return statuses


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        websites = f.read().splitlines()
    t0 = time.time()
    print(json.dumps(website_statuses(websites)))
    t1 = time.time()
    print("getting website statuses took {0:.1f} seconds".format(t1-t0))
