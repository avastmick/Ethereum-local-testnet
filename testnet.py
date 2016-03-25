#!/usr/bin/env python

import sys
import platform
import os
import json

#######################################################################################
#
# Sets up a local private Ethereum testnet with a number of pre-configured nodes
# 
# See https://github.com/avastmick/ethereum-local-testnet/wiki
# 
# NOTE: Changes should only be required to this script if run in standalone mode
#   - i.e. outside the repo structure
# 
# This script does not insist that the repo structure is present, 
#   so it should be fully portable
#   
# However, the conf directory will be checked to see if it is being run within the repo;
#    if run from the repo the JSON file will be used to config,
#    please make any changes required to that file, rather than changing values in this
#    script
# 
########################################################################################

# The config directory - as a global
confDir = "./conf/"

'''
The @TestnetConf object encapsulates the data in the testnet-config.json file.
  This will be loaded at process start through the init() function, below.

The following values will be be present in the file. 
    The defaults here will be overwritten if the file exists,
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
        networkID = "9191"
        nodeIdentity = "private_"
        verbosity = 5
        ethPort = "3080"
        rpcPort = "890"
        nodeCount = 5
        defaultDataDir = ""
        nonDefaultRootDir = ""
        staticNodes = "/static-nodes.json"
        password = "testpwd"
        genesis_block = ""
    def __init__(self, ipAddress, networkID, nodeIdentity, verbosity, ethPort, rpcPort, nodeCount, defaultDataDir, nonDefaultRootDir, staticNodes, password, genesis_block):
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
        self.genesis_block = genesis_block
    def __str__(self): 
        objStr = "Testnet Config: ipAddress: %s networkID: %s nodeIdentity: %s verbosity: %s ethPort: %s rpcPort: %s nodeCount: %s defaultDataDir: %s nonDefaultRootDir: %s staticNodes: %s password: %s genesis_block: %s" % (self.ipAddress, self.networkID, self.nodeIdentity, self.verbosity, self.ethPort, self.rpcPort, self.nodeCount, self.defaultDataDir, self.nonDefaultRootDir, self.staticNodes, self.password, self.genesis_block)
        return objStr
# Util - serializes the testnet-config JSON file in the @TestnetConf object
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
                            obj['password'],
                            obj['genesis_block'])
    return obj
testnetConf = ""
# Util - gets the platform OS name (ostype)
def getPlatformName():
    ostype = platform.system()
    return ostype

# Sets up the configuration items if they don't exist or if the script is being used portably
def getGenesisBlock():
    # Chck whether genesis_block is configured, else set up the genesis block file from default
    if testnetConf.genesis_block == "":
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
        return genesis_block
    else:
        return testnetConf.genesis_block

# Initialises the @TestnetConf object, either through the JSON file, or via the in-build defaults
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
    # Set the default data dir and non-default data dirs according to OS platform 
    ostype = getPlatformName()
    if ostype == "Darwin":
        testnetConf.defaultDataDir = os.path.expanduser("~/Library/Ethereum/geth.ipc")
        testnetConf.nonDefaultRootDir = "/tmp/"+testnetConf.networkID
    elif ostype == "Linux":
        testnetConf.defaultDataDir = os.path.expanduser("~/.ethereum/geth.ipc")
        testnetConf.nonDefaultRootDir = "/tmp/"+testnetConf.networkID
    elif ostype == "Windows":
        testnetConf.defaultDataDir = os.path.expanduser("\\~\\AppData\\Roaming\\Ethereum")
        testnetConf.nonDefaultRootDir = os.path.expanduser("\\~\\AppData\\Local\\Temp\\")+testnetConf.networkID
    else: # This is not supported
        print "Sorry, check the Ethereum docs for your Operating system"
        exit()
    # Bit of debug
    if testnetConf.verbosity > 4:
        print(testnetConf)

# Instructions to the user on how to install Ethereum for their platform / OS
def installSteps(): 
    ostype = getPlatformName()
    if ostype == "Darwin":
        print "     You\'re on a Mac, you can install using:"
        print "         brew tap ethereum/ethereum &&"
        print "         brew install ethereum"
    elif ostype == "Linux":
        print "     You\'re on a Linux variant, you can install using:"
        print "         sudo add-apt-repository ppa:ethereum/ethereum-qt &&"
        print "         sudo add-apt-repository ppa:ethereum/ethereum &&"
        print "         sudo add-apt-repository ppa:ethereum/ethereum-dev &&"
        print "         sudo apt-get update &&"
        print "         sudo apt-get install cpp-ethereum &&"
        print "         sudo apt-get install ethereum"
    elif ostype == "Windows":
        print "     You\'re on Windows, but it is not yet supported. I\'m working on it though."
    else: # This is not supported
        print "     Sorry, check the Ethereum docs for your Operating system"

# Checks whether Ethereum (Geth) is installed
def checkEthereum():
    print "Checking whether Ethereum (Geth) is installed..."
    retcode =  os.system("geth --help >/dev/null 2>&1")
    if retcode != 0: 
        print " ...no current installation of Ethereum:"
        installSteps()
        print "     Exiting."
        exit()
    else:
        print " ...already installed Ethereum, nice! Proceeding..."
    
def create():
    print "Creating..."    
def addAcc():
    print "Adding account..."    
def unlockAcc():
    print "Unlock account..."    
def start(nodeID):
    print "Starting..."    
def startAll():
    print "Starting all..."    
def stop(nodeID):
    print "Stopping..."    
def stopAll():
    print "Stopping all..."    
def attach():
    print "Attaching..."    
def mine(stopStart, nodeID, cores):
    print "Mining..."   
def clean(nodeID):
    print "Cleaning node ID: "+nodeID
def cleanAll():
    print "Cleaning all..."
# Help / Usage - just prints out to console
def usage():
    print "     python testnet.py [param]"
    print "     params:"
    print "         --create [node_num]: Creates a new testnet cluster of given size"
    print "         --addacc [node_id] : Creates a account on the node. The first account is the coinbase account."
    print "         --unlockacc [node_id] [account_no] : Unlocks the account given"
    print "         --start [node_id] : Starts the local test node"
    print "         --startall : Starts all the configured local test nodes"
    print "         --stop [node_id] : Stops a given local test node"
    print "         --stopall : Stops all the running local test nodes"
    print "         --attach [node_id] : attaches to a running node"
    print "         --mine [stop|start] [node_id] [cores] : starts the miner at a given node"
    print "         --minestop [node_id] [cores] : stops the miner at a given node"
    print "         --clean [node_id] : Removes the designated node data, removes it from cluster"
    print "         --cleanall : Cleans the whole shebang. All nodes, back to the user account"
    print "         --help -h : This message"
    exit()

# Handles the commandline input
def handleInput():
    # Take any arguments put in
    args = sys.argv
    if len(args) > 1:
        if args[1] == "--create":
            create()
        elif args[1] == "--addacc":
            addAcc()
        elif args[1] == "--unlockacc":
            unlockAcc()
        elif args[1] == "--start":
            if len(args) == 3:
                start(args[2])
            else:
                print "Correct usage: python testnet.py --start [nodeID - the node you want to start]."
        elif args[1] == "--startall":
            startAll()
        elif args[1] == "--stop":
            if len(args) == 3:
                stop(args[2])
            else:
                print "Correct usage: python testnet.py --stop [nodeID - the node you want to stop]."
        elif args[1] == "--stopall":
            stopAll()
        elif args[1] == "--attach":
            attach()
        elif args[1] == "--mine":
            if len(args) == 5:
                mine(args[2], args[3], args[4])
            else:
                print "Correct usage: python testnet.py --mine [start or stop] [nodeID] [the number of cores to be used]."
        elif args[1] == "--clean":
            if len(args) == 3:
                clean(args[2])
            else:
                print "Correct usage: python testnet.py --clean [nodeID - the node you want to remove]."
        elif args[1] == "--cleanall":
            cleanAll()
        elif args[1] == "--help":
            usage()
        else:
            print "Check usage:"
            usage()
    else:
        print "Check usage:"
        usage()

############################################################################################
# Starts the script off
###########################################################################################
handleInput()