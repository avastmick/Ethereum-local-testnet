#!/bin/bash

# Sets up a local Ethereum testnet on Mac OS X
# Creates accounts
# Mines transactions
# Allows testing on a set of node

# Need to do these in forked processes

# Create a data location for the new blockchain (datadir)
cd ~/GitHub/Ethereum-local-testnet/hostmachine/macosx/bin

# Create the blockchain
geth --genesis ../../genesis/genesis_block.json --datadir ../../data --networkid 9876 --port "8545" --nodiscover --maxpeers 0

# Initialises some base accounts TODO Create 5 accounts
geth --datadir ../../data --networkid 9876 --port "8545" --password ../../conf/testnet-pwd account new

# If all good to here, start up a miner to create blocks on the new blockchain
geth --mine -rpccorsdomain "*" --ipcapi "admin,eth,miner" --rpcapi "eth,web3" --networkid 9876 --port "8545" --datadir ../../data -maxpeers 5 --minerthreads 1 console
