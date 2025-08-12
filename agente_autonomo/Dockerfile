FROM ghcr.io/hassio-addons/base:latest

# Python + pip for the agent
RUN apk add --no-cache python3 py3-pip && mkdir -p /opt/agent

# Copy rootfs into container filesystem
COPY rootfs/ /

# Install Python deps
RUN pip install --no-cache-dir -r /opt/agent/requirements.txt

# Entrypoint
CMD [ "/run.sh" ]
