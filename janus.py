import asyncio
import random
import time

import janus

async def main():
    loop = asyncio.get_running_loop()
    queue = janus.Queue(loop=loop)  1
    future = loop.run_in_executor(None, data_source, queue)
    while (data := await queue.async_q.get()) is not None:  2
        print(f'Got {data} off queue')  3
    print('Done.')

def data_source(queue):
    for i in range(10):
        r = random.randint(0, 4)
        time.sleep(r)  4
        queue.sync_q.put(r)  5
    queue.sync_q.put(None)

asyncio.run(main())
