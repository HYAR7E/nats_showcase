import json
import asyncio
from nats.aio.client import Client as NATSClient
from nats.aio.msg import Msg

async def main():
  nc = NATSClient()
  await nc.connect("nats://0.0.0.0:4222")

  # Handlers
  async def handle_msg_avg(msg: Msg):
    data: dict = json.loads(msg.data.decode("utf-8"))
    print("data", data)
    average = sum(data) / len(data)
    await msg.respond(bytes(str(average), "utf-8"))

  async def handle_msg_sum(msg: Msg):
    data: dict = json.loads(msg.data.decode("utf-8"))
    print("data", data)
    total = sum(data)
    await msg.respond(bytes(str(total), "utf-8"))

  # Subscribe
  await nc.subscribe("pfx.api.avg", cb=handle_msg_avg)
  await nc.subscribe("pfx.api.sum", cb=handle_msg_sum)


if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.run_forever()
  loop.close()
