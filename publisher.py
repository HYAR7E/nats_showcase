from yachalk import chalk
import asyncio
from nats.aio.client import Client as NATSClient
from nats.errors import NoRespondersError

messages = [
  {"subject": "pfx.api.avg", "data": b"[1, 2, 3, 4, 5]"},
  {"subject": "pfx.api.avg", "data": b"[9, 18, 15, 23, 8]"},
  {"subject": "pfx.api.sum", "data": b"[1, 2, 3, 4, 5]"},
  {"subject": "pfx.api.sum", "data": b"[9, 18, 15, 23, 8]"},
]


async def main():
  nc = NATSClient()
  await nc.connect("nats://0.0.0.0:4222")

  # Publish messages
  for message in messages:
    print("Send", chalk.green(message["subject"]), chalk.yellow(message["data"]))
    try:
      response = await nc.request(message["subject"], message["data"])
    except NoRespondersError:
      print(chalk.red_bright("ⅹ No response"))
    else:
      print(chalk.cyan_bright("✔", response.data))
    await nc.flush()
    input()

  # Close connection
  await nc.flush()
  await nc.close()


if __name__ == "__main__":
  asyncio.run(main())
