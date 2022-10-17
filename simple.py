import asyncio
from nats.aio.client import Client as NATSClient
from nats.aio.msg import Msg
from time import sleep

site = {
  "acn": "0041",
  "acc": "12",
  "name": "Generic Site #12",
  "admin": "Neldo",
  "last_modifier": ""
}
print("site", site)
counter = 0

async def main():
  nc = NATSClient()
  await nc.connect("nats://0.0.0.0:4222")
  js = nc.jetstream()

  # Handle message fn
  async def handle_message(msg: Msg):
    global counter
    counter = counter + 1
    _, service, acn, acc, field = msg.subject.split(".")
    if acn == site["acn"] and acc == site["acc"]:
      data = msg.data.decode("utf-8")
      site.update({
        "last_modifier": service,
        field: data})
    print(f"#{counter} site", site)
    await msg.ack()

  # Get unread messages
  async def get_stream_msgs():
    psub = await js.pull_subscribe("pfx.*.0041.12.*", durable="asset-mgmt")
    try:
      unread_msgs = await psub.fetch(1000)
    except:
      pass
    else:
      for unread_msg in unread_msgs:
        await handle_message(unread_msg)

  while True:
    sleep(2)
    await get_stream_msgs()

if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.run_forever()
  loop.close()
