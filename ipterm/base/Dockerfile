# docker base image for basic networking tools

FROM debian:bullseye-slim

ARG TARGETARCH

COPY ${TARGETARCH:-amd64}/* /usr/local/bin/

RUN set -e -x \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get -y upgrade \
    && apt-get -y --no-install-recommends install \
        curl ca-certificates \
#
# install mtools (msend & mreceive)
#
    && chmod 755 /usr/local/bin/msend /usr/local/bin/mreceive \
#
# install remaining tools
#
    && apt-get -y --no-install-recommends install \
        dumb-init iperf3 knot-host mtr-tiny openssh-client socat tcpdump \
        net-tools iproute2 ifupdown iputils-ping \
        telnet traceroute procps nano vim-tiny \
    && ln -s /usr/bin/khost /usr/local/bin/host \
    && rm -rf /var/lib/apt/lists/*
