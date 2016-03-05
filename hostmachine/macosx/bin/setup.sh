#!/bin/bash

# Sets up a local Ethereum testnet - this should be good for any unix install
# 1. TODO Checks to see if Ethereum is installed (if not then install)
# 2. TODO Creates a conf file for the genesis.json and password files
# 3. Creates a set of scripts that allows the creation and teardown of a single Node
# 4. TODO Creates a script to duplicatethe initial node and create a cluster
# Help
function usage {
    echo Usage:
    echo testnet [param]
    echo params:
    echo --create : Creates a new testnet node
    echo --addacc : Creates a account on the node. The first account is the coinbase account.
    echo --unlockacc [account_no] : Unlocks the account given
    echo --clean : Cleans the installation back to base account
    echo --help -h : This message
}
# Create
function create {
    echo creating local testnet...
    geth --genesis ./genesis/genesis_block.json --networkid 1973 --port 30801 --rpcport 8901 --nodiscover 2>> eth.log &;
    echo Done. See eth.log for details
}
# Add account
function addacc {
    echo Adding account...
    geth --networkid 1973 --port 30801 --rpcport 8901 --password ./conf/testnet-pwd account new
}
# Unlock account
# TODO Need to get this working when Geth is already running
function unlockacc {
    if [ -z "$2" ]; then
        echo No account passed in exiting;
        exit
    else
        echo unlocking $2
        
    fi
}
# Clean
function clean {
    if [[ $OSTYPE == darwin* ]]; then # Is MacOS
    # Just echo for now as this will blow away my live node
    echo Would delete for Mac
        # echo "rm -rf ~/Library/Ethereum && rm -rf .ethash && rm eth.log"
    else # Is Linux
        echo Would delete for Linux
        # echo "rm -rf .ethereum && rm -rf .ethash && rm eth.log"
    fi
}
if [ -z "$1" ]; then
    usage
    exit
fi
if [[ "$1" == "--create" ]]; then
    create;
elif [[ "$1" == "--addacc" ]]; then
    addacc;
elif [[ "$1" == "--unlockacc" ]]; then
    unlockacc;
elif [[ "$1" == "--clean" ]]; then
    clean;
elif [[ "$1" == "--help" ]]; then
    usage;
elif [[ "$1" == "-h" ]]; then
    usage;
else
        echo Unknown command.
        usage;
fi
