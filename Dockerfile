FROM python:3.7-slim AS build

RUN apt-get update
RUN apt-get install netcat -y
RUN pip install nats-py yachalk faker
WORKDIR /root/app
COPY . .
RUN chmod +x boot_api.sh boot_asset_mgmt.sh boot_site_metrics.sh

FROM build as api
CMD ./boot_api.sh

FROM build as asset_mgmt
CMD ./boot_asset_mgmt.sh

FROM build as site_metrics
CMD ./boot_site_metrics.sh
