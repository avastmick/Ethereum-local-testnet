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

## Warnings and Disclaimers
Three warnings:

1. Use at your own risk!
2. Don't use the configurations here to connect to the live Ethereum (Frontier / Homestead) network.
3. Change the password for initialising the blockchain if you are distributing wider than local, private usage.

## Set-up and prerequisites

* Ethereum is installed
* Commands currently use Geth CLI only

# Start-point

I suggest follow the manual steps in the [Install](Install.md) page if you are new to Ethereum and just setting out. This collates the disparate scripts I wrote to manage the various configuration commands.

If you want to just stop manual configurations and need to bootstrap your development environment for quickly getting going clone the repo and run the ``testnet`` bash script. The script should be fully portable on any unix based system with the bash shell available.

# Next steps

1. I'll add something more flexible than a blunt instrument bash script, using python and later rust (cos I can);
2. Get it work with other client, firstly ``eth`` the CPP client, then [Ethcore](https://github.com/ethcore/parity) ``parity``;
3. A simple UI to manage;
4. Fix the various functional gaps and issues

I hope it gets you to where you want to go faster than manual configuration.

# Thanks
Just thanks to the [Ethereum Foundation](https://ethereum.org/foundation) for the brains and all the documentation that the community generates that gets people going in a non-trivial domain.

To [Tasha at π Tech Lab](http://carl.pro/#/about) for the initial [instructions on how to get a private test net up](http://tech.lab.carl.pro/kb/ethereum/testnet_setup).

To [ΞTHΞЯSPHΞЯΞ] (https://github.com/ethersphere) for the initial [eth-utils](https://github.com/ethersphere/eth-utils) tools that I came upon late and used to help me solve some issues.
