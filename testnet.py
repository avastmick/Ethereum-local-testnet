#!/usr/bin/python

import platform
import os
import json

#######################################################################################
#   REMOVE ON DONE
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

# NOTE: Changes should only be required to this script if run in standalone mode (i.e. outside the repo structure)
# 
# This script does not expect that the repo structure is present, so it should be fully portable
# However, the conf directory will be checked to see if it is being run within the repo and if so some steps will be skipped
# As a global
confDir = "./conf/"

'''
The @TestnetConf object encapsulates the data in the testnet-config.json file.
  This will be loaded at process start through the init() function, below.

The following values will be be present in the file. The defaults here will be overwritten if the file exists,
  the file doesn't exist, these values will be written out to a new file (allowing true cleaning):
  ipAddress - the IP address used for the nodes (defaults to localhost - 127.0.0.1)
  networkID - the ID of the private network created
  nodeIdentity - the identity that is displayed for the network
  verbosity - the logging level (defaulting to 5)
  ethPort - the root of the port number, i.e. if it were 3080, the default node would listen on 30800
  rpcPort - the root of the rpc port number
  nodeCount - the (default) number of nodes to be in the cluster
  defaultDataDir - the location of the default node, i.e on Linux this would be $HOME/.ethereum
  nonDefaultRootDir - the location of where the other nodes are deployed, usually in a $tmp location
  confDir - the path to the config (defaults to /conf)
  staticNodes = "/static-nodes.json", the JSON file that will store the node enode URLs
  password - a default password to use (default "testpwd")
'''
class TestnetConf:
    def __init__():
        ipAddress = "127.0.0.1"
        networkID = 9191
        nodeIdentity = "private_"
        verbosity = "5"
        ethPort = "3080"
        rpcPort = "890"
        nodeCount = 5
        defaultDataDir = ""
        nonDefaultRootDir = ""
        staticNodes = "/static-nodes.json"
        password = "testpwd"
    def __init__(self, ipAddress, networkID, nodeIdentity, verbosity, ethPort, rpcPort, nodeCount, defaultDataDir, nonDefaultRootDir, staticNodes, password):
        self.ipAddress = ipAddress
        self.networkID = networkID
        self.nodeIdentity = nodeIdentity
        self.verbosity = verbosity
        self.ethPort = ethPort
        self.rpcPort = rpcPort
        self.nodeCount = nodeCount
        self.defaultDataDir = defaultDataDir
        self.nonDefaultRootDir = nonDefaultRootDir
        self.staticNodes = staticNodes
        self.password = password
# Enable the decoding of testnet-config JSON files
def config_decoder(obj):
    if '__type__' in obj and obj['__type__'] == 'TestnetConf':
        return TestnetConf( obj['ipAddress'], 
                            obj['networkID'], 
                            obj['nodeIdentity'], 
                            obj['verbosity'], 
                            obj['ethPort'], 
                            obj['rpcPort'], 
                            obj['nodeCount'],
                            obj['defaultDataDir'], 
                            obj['nonDefaultRootDir'], 
                            obj['staticNodes'], 
                            obj['password'])
    return obj
testnetConf = ""
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
    # TODO: Move this out to a conf file
     genesis_block = ('{ '
            '"nonce": "0x0000000000000042", '
            '"mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000", '
            '"difficulty": "0x4000", '
            '"alloc": {}, '
            '"coinbase": "0x0000000000000000000000000000000000000000", '
            '"timestamp": "0x00", '
            '"parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000", '
            '"extraData": "Custom Ethereum Genesis Block for initiating a local test net", '
            '"gasLimit": "0xffffffff" }')
    # file = open(testnetConf, "w") # Created a file
    # # TODO: Push this to a formatting function
    # file.write("hello world in the new file")
    # file.write("and another line")
    # file.close()


# This for a JSON file containing the data required to run
# See the @TestnetConf object for the items to be found in this file
# If it doesn't exist, the defaults are loaded
def init(): 
    # the default location for the config JSON file will be in './conf'
    testnetConfFile = confDir+"testnet-config.json"
    print "Checking config..."
    if os.path.isfile(testnetConfFile): # Suck in the file and load into the @TestnetConf obj
        with open(testnetConfFile) as testnet_config:
            testnetConf = json.load(testnet_config, object_hook=config_decoder)
        print "     ...initialised from json file, good to go."
    else: 
        print "     ...no configuration file found, using script defaults."
        testnetConf = TestnetConf() # Portable - use the defaults

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
    print os.popen("geth --help").read()
    # if hash geth >/dev/null 2>&1 : 
    #     print "No current installation of Ethereum"
    installSteps()
    # else
    #     print "Already installed Ethereum, nice! Proceeding..."
    

usage()
checkEthereum()
init()