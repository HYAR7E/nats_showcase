import asyncio
from nats.aio.client import Client as NATSClient
from nats.aio.msg import Msg

site = {
  "acn": "0041",
  "acc": "12",
  "name": "Generic Site #12",
  "admin": "Neldo",
  "last_modifier": ""
}
print("site", site)

async def main():
  nc = NATSClient()
  await nc.connect("nats://0.0.0.0:4222")

  # Handle message fn
  async def handle_message(msg: Msg):
    _, service, acn, acc, field = msg.subject.split(".")
    if acn == site["acn"] and acc == site["acc"]:
      data = msg.data.decode("utf-8")
      site.update({
        "last_modifier": service,
        field: data})
    print("site", site)

  # Subscribe
  await nc.subscribe("pfx.*.0041.12.*", cb=handle_message)
  # pfx.<service>.<acn>.<acc>.<field>
  # pfx.api.0041.12.name


if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.run_forever()
  loop.close()
