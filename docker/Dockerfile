FROM avastmick/development

MAINTAINER avastmick <avastmick.outlook.com>

ENV ETH_HOME /usr/local/repos

ARG user=eth
ARG group=eth
ARG uid=1000
ARG gid=1000

# add a viable user, instead of root as some tools don't play well with root
RUN groupadd -g ${gid} ${group} \
    && useradd -d "$ETH_HOME" -u ${uid} -g ${gid} -m -s /bin/bash ${user} \
    && adduser ${user} sudo \
    && echo ${user}:temp | chpasswd \
    && chage -d 0 ${user}

# Install:
#  - Geth
#  - Python
#  - net-tools - to enable debugging of network issues if required
RUN apt-get update && \
    apt-get upgrade -q -y && \
    apt-get dist-upgrade -q -y && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 923F6CA9 && \
    echo "deb http://ppa.launchpad.net/ethereum/ethereum/ubuntu xenial main" | tee -a /etc/apt/sources.list.d/ethereum.list && \
    apt-get update && \
    apt-get install -q -y geth \
                          net-tools \
                          python python-dev python-pip python-setuptools \
                          python3 python3-dev python3-pip python3-setuptools \
                          virtualenvwrapper \
                          && \
    apt-get clean

RUN pip3 install --upgrade setuptools pip wheel django

# The following is a potential target for the in Docker viewing of the local testnet, but would prefer a Python version
# web3.py
#

# Add a python eth-lightwallet...???

# Run up a webserver to enable external access to lightwallet
# Need a lightweigh webserver

    # Now clone the ethereum-local-testnet repo
RUN git clone https://github.com/avastmick/ethereum-local-testnet.git && \
    # And run testnet
    cd ethereum-local-testnet

# Expose the default node (~/.ethereum) ports to allow external connection by Mist
EXPOSE 30801 8901 8089

# Set up to run in $HOME as the new $user
WORKDIR ${ETH_HOME}
USER ${user}
