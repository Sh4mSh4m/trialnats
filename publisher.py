import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

async def publish(loop):
    nc = NATS()
    
    await nc.connect("localhost:4222", loop=loop)

    await nc.publish("trial", b'T1')
    await asyncio.sleep(0.5)
    await nc.publish("trial", b'T2')
    await asyncio.sleep(0.5)
    await nc.publish("trial", b'T3')

    await nc.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(publish(loop))
    loop.close()

