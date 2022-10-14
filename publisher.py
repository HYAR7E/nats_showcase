from yachalk import chalk
import asyncio
from nats.aio.client import Client as NATSClient
from nats.errors import NoRespondersError, TimeoutError

messages = [
  {"subject": "pfx.api.0041.12.name", "data": b"New Site"}, # Update name
  {"subject": "pfx.api.0041.12.admin", "data": b"Luis"}, # Update admin
  {"subject": "pfx.asset_mgmt.0041.12.admin", "data": b"Neldo"}, # Update service
  {"subject": "pfx.site_metrics.0041.10.admin", "data": b"None"}, # Fail ACC
  {"subject": "pfx.site_metrics.0041.12.acn", "data": b"0001"}, # Update ACN
  {"subject": "pfx.site_metrics.0041.12.name", "data": b"New Site"}, # Fail ACN
  {"subject": "pfx.site_metrics.0001.12.name", "data": b"Site #0001"}, # Update name
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
      print(chalk.red_bright("ⅹ Subject not found"))
    except TimeoutError:
      print(chalk.red_bright("⏰ Subject didn't respond"))
    else:
      print(chalk.cyan_bright("✔", response.data))
    await nc.flush()
    input()

  # Close connection
  await nc.flush()
  await nc.close()


if __name__ == "__main__":
  asyncio.run(main())
