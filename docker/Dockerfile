FROM ubuntu:wily
MAINTAINER avastmick

ENV DEBIAN_FRONTEND noninteractive

# Usual update / upgrade
RUN apt-get update
RUN apt-get upgrade -q -y
RUN apt-get dist-upgrade -q -y

# Install Ethereum
RUN apt-get install -q -y software-properties-common
RUN add-apt-repository ppa:ethereum/ethereum
RUN add-apt-repository ppa:ethereum/ethereum-dev
RUN apt-get update
RUN apt-get install -q -y geth

EXPOSE 8545
EXPOSE 30303

# Just going to slam this into bash until I work out how to pre-configure in Docker file
ENTRYPOINT ["/usr/bin/bash"]
