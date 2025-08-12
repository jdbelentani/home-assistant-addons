# Use Home Assistant base image for the detected architecture
ARG BUILD_FROM=ghcr.io/home-assistant/{arch}-addon-base:17.1.0
FROM $BUILD_FROM

# Python + pip
RUN apk add --no-cache python3 py3-pip

# Copy rootfs into container filesystem
COPY rootfs/ /

# Python dependencies for the agent
RUN pip3 install --no-cache-dir -r /opt/agent/requirements.txt

# Entrypoint
CMD [ "/run.sh" ]
