# Dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    tor \
    privoxy \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install scrapy

COPY privoxy_config /etc/privoxy/config

#COPY torrc /etc/tor/torrc

WORKDIR /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
