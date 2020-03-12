import asyncio
import logging
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
from time import time, sleep
import concurrent.futures

#logging.basicConfig(level=logging.DEBUG)

async def cb2(future):
    print(future.result())

def task1(data):
    print(f"{data} - TASK blocking sleep for {3} seconds")
    for i in range(3):
        print(f"{data}" * (3 - i))
        sleep(1)
    return f"done-{data}"

async def add_success_cb(future, callback):
    result = await future
    await callback(future) 

async def listening(pool):
    nc = NATS()
    print("Obj done")
    loop = asyncio.get_running_loop()
    await nc.connect("localhost:4222", loop=loop)
    print("connected")

    async def help_request(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print(f"Received a message on '{subject} {reply}': {data}")
        future = loop.run_in_executor(pool, task1, data)
        new_task = add_success_cb(future, cb2)
        result = asyncio.create_task(new_task)
        print(result)
        #future.add_done_callback(cb2)
    await nc.subscribe("trial", cb=help_request)


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        loop.run_until_complete(listening(pool))
        loop.run_forever()
        loop.close()
        
