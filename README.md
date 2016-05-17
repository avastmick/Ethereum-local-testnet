# Ethereum Local, Private Testnet

A single, easy-to-use script that pre-configures a local, private testnet  using Geth.

To use:
````
$ git clone https://github.com/avastmick/ethereum-local-testnet.git
$ cd ethereum-local-testnet
$ ./testnet --create
````
This creates a cluster of nodes with one at the default Geth location to allow the attaching of the Ethereum UI tools, such as Mist.

** Warning: Do this in a clean user account that is *not* used for the live network.**

## Goals
1. Usability. While most of the developer tools are available and can get you going, they require a good deal of configuration, understanding and look-up to get things going.
2. Speed. To enable users to quickly set up a clustered node set that allows a clean and repeatable development environment with which a more robust, controllable and realistic testing regime than can be possibly achieved using the public testnet (Morden) or manually using the existing tools or utils.
3. Tools. To configurure a cluster that will allow the various Ethereum UI applications, such as Mist to use a private network, so easy maniputation of transactions, contracts, gas etc. can be done simply and through the offical tools.
4. Learning. I've learnt a huge amount just getting this going. It started as a set of diparate scripts that I'd created to allow repeatable action; then I stitched these together to speed things up; finally I wanted to blow everything away to ensure nothing locally was causing errors etc. in good test practise.
5. A continuous integration environment to speed up and make safe contract development.

Eventually, this will grow to enable a typical 3-stage development cycle:
1. Code development with local testing cycle against a local testnet (this);
2. Promotion to UAT and testing at scale on the public testnet (Morden);
3. Production - release onto the live network (1)

## Warnings and Disclaimers
Three warnings:

1. Use at your own risk!
2. Don't use the configurations here to connect to the live Ethereum (Frontier / Homestead) network.
3. Change the password for initialising the blockchain if you are distributing wider than local, private usage - i.e. you are using this to create a private network across wider area networks.

## Set-up and prerequisites

* Ethereum is installed
* Commands currently use Geth CLI only

# Start-point

Simply install Geth and follow the above.

If you start it up, you can then start the [Ethereum Wallet](https://github.com/ethereum/mist) app and it will automagically attach to the testnet. If you mine (``miner.start(1)``) on the default node you will see your "Coin Base" account accruing Ether!

Or, run the [Docker](https://hub.docker.com/r/avastmick/ethereum-local-testnet), which gives you an interactive shell, just run ``./testnet --create`` from there and do your thing on the Geth CLI.

To better understand, I suggest follow the manual steps in the [Install](Install.md) page if you are new to Ethereum and just setting out. This collates the disparate scripts I wrote to manage the various configuration commands.

If you want to just stop manual configurations and need to bootstrap your development environment for quickly getting going clone the repo and run the ``testnet`` bash script. The script should be fully portable on any unix based system with the bash shell available.

## OR, use the Docker image

If you use docker locally (and you should it's great) you can simply run up a working environment thus:

```
docker run -p 8088:8089 -p 30801:30801 -p 8901:8901 --name local-testnet -i -t avastmick/ethereum-local-testnet /bin/bash
```
This maps some ports to enable host interaction and will expose the web app when done.

Your Docker host will pull down the latest image at [avastmick/ethereum-local-testnet](https://hub.docker.com/r/avastmick/ethereum-local-testnet/) and then start a suitably configured container.

I'll look to have two images available:
- ``latest`` that will run off the n+1 version of Geth and
- ``stable`` that runs off the current public version.

These will map to the ``development`` and ``master`` branches in this repo.

### Not got Docker?

Installation is straightforward enough... on [Linux](https://docs.docker.com/engine/installation/linux/ubuntulinux/)...

```
$ curl -sSL https://get.docker.com/ | sh
$ # Add your user to docker group so you can avoid using root (sudo)
$ sudo usermod -aG docker [your_user]
$ _sudo reboot_
$ _sudo service docker start_
$ # Verify this works:
$ docker run hello-world
$ # Drink a beer
````
If you insist on using Windows or OSX, then there are more hoops to jump through. These are getting better, but still more work.


I hope it gets you to where you want to go faster than manual configuration.

# Thanks
Just thanks to the [Ethereum Foundation](https://ethereum.org/foundation) for the brains and all the documentation that the community generates that gets people going in a non-trivial domain.

To [Tasha at π Tech Lab](http://carl.pro/#/about) for the initial [instructions on how to get a private test net up](http://tech.lab.carl.pro/kb/ethereum/testnet_setup).

To [ΞTHΞЯSPHΞЯΞ] (https://github.com/ethersphere) for the initial [eth-utils](https://github.com/ethersphere/eth-utils) tools that I came upon late and used to help me solve some issues.
