#!/bin/bash

# Sets up a local Ethereum testnet on Mac OS X
# Creates accounts
# Mines transactions
# Allows testing on a set of node

# Assumption: clean install - i.e. no default blockchain
# Check location of work, should be in a localised datadir
#

# Need to do these in forked processes

# Create a data location for the new blockchain (datadir)
cd ~/GitHub/Ethereum-local-testnet/hostmachine/macosx/bin

# Create a memorable networkid:
#   1973
# && set it so noone can discover it
# Assumption that we are going to cluster this:
#   TCP Port: 30801
# Iterating RPC port
#   RPC Port: 8901

# Note that the datadir IS IMPORTANT, otherwise the command iterates of the default blockchain

# Create the base blockchain
geth --genesis ../../genesis/genesis_block.json --datadir ../../data --networkid 1973 --port 30801 --rpcport 8901 --nodiscover --maxpeers 0

# Initialises the base account and coinbase and unlock
geth --datadir ../../data --networkid 1973 --port 30801 --rpcport 8901 --password ../../conf/testnet-pwd account new
geth --password ../../conf/testnet-pwd --unlock 0 --datadir ../../data --networkid 1973 --port 30801 --rpcport 8901 --rpccorsdomain localhost
# Create 5 accounts (to line up with contract tests)... just iterate over the same pwd (its only a closed testnet...)

# If all good to here, start up a miner to create blocks on the new blockchain
# geth --mine -rpccorsdomain "*" --ipcapi "admin,eth,miner" --rpcapi "eth,web3" --networkid 1973 --port 30801 --rpcport 8901 --datadir ../../data -maxpeers 5 --minerthreads 1 console
# Or just attach to console and then run > miner.start(1)

# Run the console:
# Make sure that the rpc server is started and the APIs enabled!
geth --datadir ../../data --networkid 1973 --port 30801 -rpc --rpcport 8901 --rpcapi "db,eth,net,web3" console 2>> eth.log

# Attach to running console
#geth --datadir ../../data --networkid 1973 --port 30801 --rpcport 8901 attach
