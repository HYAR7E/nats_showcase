import asyncio
import datetime as dt
import json
import os
from time import sleep

from nats.aio.client import Client as NATSClient
from nats.aio.msg import Msg
from yachalk import chalk

# Subject: pfx.<acn>.<acc>.site
# Data: { name: str, updated_at: datetime }
now_str = lambda: dt.datetime.now().strftime("%Y-%m-%d %H:%M")
sites = [
  {
    "acn": "0039",
    "acc": "10",
    "updated_at": now_str(),
    "name": "Generic Site #10",
  },
  {
    "acn": "0039",
    "acc": "12",
    "updated_at": now_str(),
    "name": "Generic Site #12",
  },
  {
    "acn": "0041",
    "acc": "10",
    "updated_at": now_str(),
    "name": "Specific Site #10",
  },
  {
    "acn": "0041",
    "acc": "12",
    "updated_at": now_str(),
    "name": "Specific Site #12",
  },
]
counter = 0
NATS_HOST = os.environ.get("NATS_HOST", "0.0.0.0")
NATS_PORT = os.environ.get("NATS_PORT", "4222")


def find_site(acn:str, acc:str):
  for site in sites:
    if site["acn"] == acn and site["acc"] == acc:
      return site
  return None

async def main():
  nc = NATSClient()
  await nc.connect(f"nats://{NATS_HOST}:{NATS_PORT}")
  js = nc.jetstream()

  # Handle message fn
  async def handle_message(msg: Msg):
    global counter
    counter = counter + 1
    _, acn, acc, _ = msg.subject.split(".")
    site = find_site(acn, acc)
    if site:
      data = json.loads(msg.data.decode("utf-8"))
      site.update({
        "name": data["name"],
        "updated_at": now_str()})
      print(f"#{counter}", chalk.green(site))
      await msg.ack()

  # Get unread messages
  async def get_stream_msgs():
    psub = await js.pull_subscribe("pfx.*.*.site", durable="site_metrics")
    try:
      print(chalk.yellow("Loading next batch"))
      unread_msgs = await psub.fetch(5)
    except:
      pass
    else:
      for unread_msg in unread_msgs:
        await handle_message(unread_msg)

  # Sleeps 20s every 10 messages
  i = 0
  while True:
    i = i + 1
    await get_stream_msgs()
    if i % 6 == 0:
      print(chalk.red("Restarting..."))
      sleep(20)
      print(chalk.green("Successfully restarted"))
    else:
      sleep(2)

if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.run_forever()
  loop.close()
