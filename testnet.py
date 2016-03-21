#!/usr/bin/python
import subprocess
import glob
import os

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

# Help / Usage
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
#}


# Instructions to install Ethereum
def installSteps(): 
    # Need to add look-up for Windows
    
    p = subprocess.Popen(
        "echo $OSTYPE",
        shell=True, stdout=subprocess.PIPE
    )

    retCode = p.wait()
    ostype = p.stdout.read()

    print "****** Your\'re using : "+ostype
    if ostype == "darwin*":
        print "You\'re on a Mac, you can install using:"
        print "brew tap ethereum/ethereum &&"
        print "brew install ethereum"
    elif ostype == "linux-gnu":
        print "You\'re on a Ubuntu variant, you can install using:"
        print "  sudo add-apt-repository ppa:ethereum/ethereum-qt &&"
        print "  sudo add-apt-repository ppa:ethereum/ethereum &&"
        print "  sudo add-apt-repository ppa:ethereum/ethereum-dev &&"
        print "  sudo apt-get update &&"
        print "  sudo apt-get install cpp-ethereum &&"
        print "  sudo apt-get install ethereum"
    else: # This is not supported
        print "Sorry, check the Ethereum docs for your Operating system"


usage()
installSteps()