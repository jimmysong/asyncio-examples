import aiohttp
import asyncio
import json
import sys
import time


async def get_statuses(websites):
    async with aiohttp.ClientSession() as session:
        statuses = {}
        tasks = [get_website_status(website, session) for website in websites]
        for status in await asyncio.gather(*tasks):
            if not statuses.get(status):
                statuses[status] = 0
            statuses[status] += 1
        print(json.dumps(statuses))


async def get_website_status(url, session):
    async with session.get(url) as response:
        return response.status


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        websites = [url for url in f.read().split('\n') if url != ""]
    t0 = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_statuses(websites))
    t1 = time.time()
    print("getting website statuses took {} seconds".format(t1-t0))
