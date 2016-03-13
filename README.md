# Ethereum local testnet

The code snippets, scripts and code allows for the education and learning of how to configure Ethereum nodes using Geth.

## Goals
Usability. While most of the developer tools are available and can get you going, they require a good deal of configuration, understanding and look-up to get things going.

The intent is to enable users to quickly set up a clustered node set that allows a clean and repeatable development environment with which a more robust and controllable testing regime than can be possibly achieved using the public testnet (Morden) or manually using the existing tools or utils.

Finally, the goal is to get a configuration that will allow the various Ethereum UI applications, such as Mist to use a private network, so easy maniputation of transactions, contracts, gas etc. can be done simply and through the offical tools.

## Warnings and Disclaimers
Three warnings:

1. Use at your own risk!
2. Don't use the configurations here to connect to the live Ethereum (Frontier / Homestead) network.
3. Change the password for initialising the blockchain if you are distributing wider than local, private usage.

## Set-up and prerequisites

* Ethereum is installed
* Commands currently use Geth CLI only

# Start-point

I suggest follow the manual steps in the [Install](Install.md) page if you are new to Ethereum and just setting out.
If you want to just stop manual configurations and need to bootstrap your development environment for quickly getting going clone the repo and run the ``testnet`` bash script.

# Next steps

I'll add something more flexible than a blunt instrument bash script, using python and later rust (cos I can).

I hope it gets you to where you want to go faster than manual configuration.

# Thanks
Just thanks to the Ethereum Foundation for all this happening and all the documentation.

To [Tasha at π Tech Lab](http://carl.pro/#/about) for the initial [instructions on how to get a private test net up](http://tech.lab.carl.pro/kb/ethereum/testnet_setup).
