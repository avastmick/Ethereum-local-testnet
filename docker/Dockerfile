FROM avastmick/development-base

MAINTAINER avastmick <avastmick.outlook.com>

WORKDIR /usr/local/repos/

# Install Geth and clone this repo and run testnet create
RUN apt-get update && \
    apt-get upgrade -q -y && \
    apt-get dist-upgrade -q -y && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 923F6CA9 && \
    echo "deb http://ppa.launchpad.net/ethereum/ethereum/ubuntu xenial main" | tee -a /etc/apt/sources.list.d/ethereum.list && \
    apt-get update && \
    apt-get install -q -y geth && \
    apt-get update && \
    apt-get install -q -y git && \
    apt-get clean

    # Now clone the ethereum-local-testnet repo
RUN git clone https://github.com/avastmick/ethereum-local-testnet.git && \
    # And run testnet
    cd ethereum-local-testnet
