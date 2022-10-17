import json
import asyncio
from nats.aio.client import Client as NATSClient

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
  async def handle_message(msg):
    global counter
    counter = counter + 1
    _, service, acn, acc, field = msg.subject.split(".")
    if acn == site["acn"] and acc == site["acc"]:
      data = msg.data.decode("utf-8")
      site.update({
        "last_modifier": service,
        field: data})
    print(f"#{counter} site", site)

  # Get unread messages
  print("---- jetstream ")
  psub = await js.pull_subscribe("pfx.*.0041.12.*", durable="asset-mgmt")
  while True:
    try:
      unread_msgs = await psub.fetch()
    except:
      break
    for unread_msg in unread_msgs:
      await handle_message(unread_msg)
      await unread_msg.ack()
  await js.purge_stream("error_backup")

  # Subscribe
  print("---- subscription ")
  await js.subscribe("pfx.*.0041.12.*", cb=handle_message)
  # pfx.<service>.<acn>.<acc>.<field>
  # pfx.api.0041.12.name


if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.run_forever()
  loop.close()
