# Setup streaming for pfx_site
nats stream add pfx_site \
  --subjects "pfx.*.*.site" \
  --storage file \
  --replicas 1 \
  --retention limits \
  --discard old \
  --max-msgs=-1 \
  --max-msgs-per-subject=-1 \
  --max-msg-size=-1 \
  --ack \
  --max-bytes=-1 \
  --max-age=1y \
  --dupe-window="0s" \
  --no-allow-rollup \
  --no-deny-delete \
  --no-deny-purge \
  -s $NATS_HOST;
