FROM avastmick/development-base

MAINTAINER avastmick <avastmick.outlook.com>

WORKDIR /usr/local/repos/

# Expose the default node (~/.ethereum) to allow external connection by Mist
EXPOSE 30801

# Install:
#  - Geth
#  - Git
#  - net-tools - to enable debugging of network issues if required
RUN apt-get update && \
    apt-get upgrade -q -y && \
    apt-get dist-upgrade -q -y && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 923F6CA9 && \
    echo "deb http://ppa.launchpad.net/ethereum/ethereum/ubuntu xenial main" | tee -a /etc/apt/sources.list.d/ethereum.list && \
    apt-get update && \
    apt-get install -q -y net-tools git geth && \
    apt-get clean

    # Now clone the ethereum-local-testnet repo
RUN git clone https://github.com/avastmick/ethereum-local-testnet.git && \
    # And run testnet
    cd ethereum-local-testnet
