#!/usr/bin/python

import platform

#######################################################################################
#   Refactor this to enable cross-platform usage (i.e. adding Windows support)
#   Step 1: Get running as is, then
#   Step 2: Add module / function to write a JSON file to config to hold settings 
#           for the given OS / environment
#       - This will be created the first time the program is run
#       - This will be loaded on any start up / run
#       - The functions then can be abstracted properly away from the variable and
#           put into a function / macro that will get the right value from the
#           JSON file 
#######################################################################################

# Help / Usage - just prints out to console
def usage():
    print "Usage:"
    print "   testnet [param]"
    print "params:"
    print    "--create [node_num]: Creates a new testnet cluster of given size"
    print    "--addacc [node_id] : Creates a account on the node. The first account is the coinbase account."
    print    "--unlockacc [node_id] [account_no] : Unlocks the account given"
    print    "--start [node_id] : Starts the local test node"
    print    "--startall : Starts all the configured local test nodes"
    print    "--stop [node_id] : Stops a given local test node"
    print    "stopall : Stops all the running local test nodes"
    print    "--attach [node_id] : attaches to a running node"
    print    "--minestart [node_id] [cores] : starts the miner at a given node"
    print    "--minestop [node_id] [cores] : stops the miner at a given node"
    print    "--clean [node_id] : Removes the designated node data, removes it from cluster"
    print    "--cleanall : Cleans the whole shebang. All nodes, back to the user account"
    print    "--help -h : This message"

# Sets up the configuration items if they don't exist or if the script is being used portably
def configure():
    # Set up the genesis block file
    genesis_block = ('{ '
            '"nonce": "0x0000000000000042",'
            '"mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",'
            '"difficulty": "0x4000",'
            '"alloc": {},'
            '"coinbase": "0x0000000000000000000000000000000000000000",'
            '"timestamp": "0x00",'
            '"parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",'
            '"extraData": "Custom Ethereum Genesis Block for initiating a local test net",'
            '"gasLimit": "0xffffffff" }')

## This sets up a JSON file containing the data required to run
# The following will be written:
#   idAddress - the IP address used for the nodes (defaults to localhost - 127.0.0.1)
#   networkID - the ID of the private network created
#   identity - the identity that is displayed for the network
#   verbosity - the logging level
#   ethPort - the root of the port number, i.e. if it were 3080, the default node would listen on 30800
#   rpcPort - the root of the rpc port number
#   nodeCount - the (default) number of nodes to be in the cluster
#   defaultDataDir - the location of the default node, i.e on Linux this would be $HOME/.ethereum
#   nonDefaultRootDir - the location of where the other nodes are deployed, usually in a $tmp location
#   confDir - the path to the config (defaults to /conf)
#   staticNodes = "/static-nodes.json", the JSON file that will store the node enode URLs
#   password - a default password to use
def init(): 
    # 
    print "TODO Inititialising"

# Gets the platform OS name (ostype)
def getPlatformName():
    ostype = platform.system()
    return ostype

# Instructions to install Ethereum
def installSteps(): 
    ostype = getPlatformName()
    if ostype == "Darwin":
        print "You\'re on a Mac, you can install using:"
        print "brew tap ethereum/ethereum &&"
        print "brew install ethereum"
    elif ostype == "Linux":
        print "You\'re on a Linux variant, you can install using:"
        print "  sudo add-apt-repository ppa:ethereum/ethereum-qt &&"
        print "  sudo add-apt-repository ppa:ethereum/ethereum &&"
        print "  sudo add-apt-repository ppa:ethereum/ethereum-dev &&"
        print "  sudo apt-get update &&"
        print "  sudo apt-get install cpp-ethereum &&"
        print "  sudo apt-get install ethereum"
    elif ostype == "Windows":
        print "You\'re on Windows, but it is not yet supported. I\'m working on it though."
    else: # This is not supported
        print "Sorry, check the Ethereum docs for your Operating system"

# Checks whether Ethereum (Geth) is installed
def checkEthereum():
    print "Sorry not yet implemented"
    # if hash geth >/dev/null 2>&1 : 
    #     print "No current installation of Ethereum"
    installSteps()
    # else
    #     print "Already installed Ethereum, nice! Proceeding..."
    

usage()
checkEthereum()