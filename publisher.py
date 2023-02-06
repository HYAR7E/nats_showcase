from time import sleep
from yachalk import chalk
import asyncio
from nats.aio.client import Client as NATSClient

messages = [
  {"subject": "pfx.api.0041.12.name", "data": b"New Site"},
  {"subject": "pfx.api.0041.12.admin", "data": b"Luis"},
  {"subject": "pfx.api.0041.12.name", "data": b"My Site"},
  {"subject": "pfx.asset_mgmt.0041.12.admin", "data": b"Neldo"},
  {"subject": "pfx.site_metrics.0041.10.admin", "data": b"None"},
]


async def main():
  nc = NATSClient()
  await nc.connect("nats://0.0.0.0:4222")

  # Publish messages
  inx = 0
  length = len(messages)
  while True:
    message = messages[inx % length]
    await nc.publish(message["subject"], message["data"])
    await nc.flush()
    print("Send", chalk.green(message["subject"]), chalk.yellow(message["data"]))
    sleep(2)
    inx += 1

  # Close connection
  await nc.flush()
  await nc.close()


if __name__ == "__main__":
  asyncio.run(main())
