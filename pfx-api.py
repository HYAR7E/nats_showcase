import asyncio
import json
import os
from time import sleep

from faker import Faker
from faker.providers import DynamicProvider
from yachalk import chalk

from nats.aio.client import Client as NATSClient

NATS_HOST = os.environ.get("NATS_HOST", "0.0.0.0")
NATS_PORT = os.environ.get("NATS_PORT", "4222")
fake = Faker()
# Subject: pfx.<acn>.<acc>.site
# Data: { name: str, updated_at: datetime }
# Payload: { name: str, admin: str }
acn_provider = DynamicProvider(provider_name="acn", elements=["0039", "0041"])
acc_provider = DynamicProvider(provider_name="acc", elements=["10", "12"])
fake.add_provider(acn_provider)
fake.add_provider(acc_provider)

async def main():
  nc = NATSClient()
  await nc.connect(f"nats://{NATS_HOST}:{NATS_PORT}")
  js = nc.jetstream()

  # Publish messages
  while True:
    subject = f"pfx.{fake.acn()}.{fake.acc()}.site"
    data = {"name": fake.company()}
    bytes_data = bytes(json.dumps(data), encoding="utf-8")
    ack = await js.publish(subject, bytes_data)
    print(f"#{ack.seq} Send", chalk.green(subject), chalk.yellow(data))
    sleep(2)


if __name__ == "__main__":
  asyncio.run(main())
