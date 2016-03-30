#!/usr/bin/env python

import sys
import platform
import os
import json
import multiprocessing
import subprocess
import re
import shutil

'''
Sets up a local private Ethereum testnet with a number of pre-configured nodes

 See https://github.com/avastmick/ethereum-local-testnet/wiki

 NOTE: Changes should only be required to this script if run in standalone mode
   - i.e. outside the repo structure

 This script does not insist that the repo structure is present,
   so it should be fully portable

 However, the conf directory will be checked to see if it is being run;
    within the repo if run from the repo the JSON file will be used to config,
    please make any changes required to that file, rather than changing
    values in this script
'''

'''
The @TestnetConf object encapsulates the data in the testnet-config.json file.
  This will be loaded at process start through the init() function, below.
The following values will be be present in the file.
    The defaults here will be overwritten if the file exists:
  ipAddress - the IP address used for the nodes (defaults to 127.0.0.1)
  networkID - the ID of the private network created
  nodeIdentity - the identity that is displayed for the network
  verbosity - the logging level (defaulting to 5)
  ethPort - root port number, i.e. if it were 3080, the default node is 30800
  rpcPort - the root of the rpc port number
  nodeCount - the (default) number of nodes to be in the cluster
  defaultDataDir - i.e on Linux this would be $HOME/.ethereum
  nonDefaultRootDir - the location of the other nodes , usually in $tmp
  confDir - the path to the config (defaults to /conf)
  staticNodes = "/static-nodes.json", the JSON file that will store enode URLs
  password - a default password to use (default "testpwd")
'''


class TestnetConf:

    def __init__(self, *args, **conf_params):
        if conf_params:  # Typically this will be loading from a JSON file
            self.ipAddress = conf_params['ipAddress']
            self.networkID = conf_params['networkID']
            self.nodeIdentity = conf_params['nodeIdentity']
            self.verbosity = conf_params['verbosity']
            self.ethPort = conf_params['ethPort']
            self.rpcPort = conf_params['rpcPort']
            self.nodeCount = conf_params['nodeCount']
            self.defaultDataDir = conf_params['defaultDataDir']
            self.nonDefaultRootDir = conf_params['nonDefaultRootDir']
            self.staticNodes = conf_params['staticNodes']
            self.password = conf_params['password']
            self.genesis_block = conf_params['genesis_block']
            self.enode_lookup = conf_params['enode_lookup']
        else:  # Set defaults to allow portable usage
            self.ipAddress = "127.0.0.1"
            self.networkID = "9191"
            self.nodeIdentity = "private_"
            self.verbosity = 5
            self.ethPort = "3080"
            self.rpcPort = "890"
            self.nodeCount = 5
            self.defaultDataDir = ""
            self.nonDefaultRootDir = ""
            self.staticNodes = "/static-nodes.json"
            self.password = "testpwd"
            self.genesis_block = ('{ '
                                  '"nonce": "0x0000000000000042", '
                                  '"mixhash": "0x00000000000000000000000000'
                                  '00000000000000000000000000000000000000", '
                                  '"difficulty": "0x4000", '
                                  '"alloc": {}, '
                                  '"coinbase": "0x00000000000000000000000000'
                                  '00000000000000", '
                                  '"timestamp": "0x00", '
                                  '"parentHash": "0x000000000000000000000000'
                                  '0000000000000000000000000000000000000000", '
                                  '"extraData": "Custom Ethereum Genesis Block'
                                  ' for initiating a local test net", '
                                  '"gasLimit": "0xffffffff" }')
            self.enode_lookup = "console.log(admin.nodeInfo.enode); exit();"

    def __str__(self):
        objStr = "Testnet Config: ipAddress: %s networkID: %s nodeIdentity: " \
                 " %s verbosity: %s ethPort: %s rpcPort: %s nodeCount: %s " \
                 "defaultDataDir: %s nonDefaultRootDir: %s staticNodes: %s " \
                 "password: %s genesis_block: %s" % \
                 (self.ipAddress, self.networkID, self.nodeIdentity,
                  self.verbosity, self.ethPort, self.rpcPort, self.nodeCount,
                  self.defaultDataDir, self.nonDefaultRootDir,
                  self.staticNodes, self.password, self.genesis_block)
        return objStr

confDir = "conf"  # The config directory - as a global
testnetConf = TestnetConf()  # TestnetConf object


def DEBUG():  # Util - Checks the verbosity 
    if testnetConf.verbosity > 4:
        return True
    else:
        return False


def getPlatformName():  # Util - gets the platform OS name (ostype)
    ostype = platform.system()
    return ostype


def genesisBlock():  # Check whether genesis_block.json exists.
    if os.path.isfile(os.path.join(confDir, "testnet-config.json")):
        if DEBUG():
            print "Node genesis block exists."
    else:
        if DEBUG():
            print "Wrote new genesis block file to: " + \
                    os.path.join(confDir, "testnet-config.json")
        genesis_block = open(os.path.join(confDir, "testnet-config.json"), "w")
        genesis_block.write(testnetConf.genesis_block)
        genesis_block.close


def enodeURLJS():  # Checks whether the enode lookup JS exists
    if os.path.isfile(os.path.join(confDir, "enode_lookup.js")):
        if DEBUG():
            print "Enode lookup JS file exists."
    else:
        if DEBUG():
            print "Wrote new Enode lookup JS file to: " + \
                    os.path.join(confDir, "enode_lookup.js")
        enode_lookup = open(os.path.join(confDir, "enode_lookup.js"), "w")
        enode_lookup.write(testnetConf.enode_lookup)
        enode_lookup.close


def writePIDFile(node_id, PID):  # Writes PID to file.
    pathToPID = ""
    if node_id > 0:  # Then this is NOT the default node
            pathToPID = os.path.join(testnetConf.nonDefaultRootDir,
                                     str(node_id))
    else:  # This is the default
            pathToPID = testnetConf.defaultDataDir

    if os.path.isfile(os.path.join(pathToPID, "pid_file")):
        print "PID file exists! Check whether process is running" + \
              " for process id: " + str(PID) + \
              ". Exiting."
        exit()
    else:  # No PID continue
        if DEBUG():
            print "Wrote PID, " + str(PID) + ", to file: " + \
                    os.path.join(pathToPID, "pid_file")
        pid_file = open(os.path.join(pathToPID, "pid_file"), "w")
        pid_file.write(str(PID))
        pid_file.close


def init():  # Initialises config, via the JSON file, or  in-build defaults
    # First check whether Ethereum is installed
    checkEthereum()
    # Set the testnetConf to global
    global testnetConf
    # the default location for the config JSON file will be in './conf'
    testnetConfFile = os.path.join(confDir, "testnet-config.json")
    print "Checking config..."
    if os.path.isfile(testnetConfFile):
        with open(testnetConfFile) as testnet_config:
            json_conf = json.load(testnet_config)
            testnetConf = TestnetConf(**json_conf)
        print "     ...initialised from json file, good to go."
    else:
        print "     ...no configuration file found, using script defaults."
        testnetConf = TestnetConf()  # Portable - use the defaults
    # Set the default data dir and non-default data dirs according to OS
    ostype = getPlatformName()
    if ostype == "Darwin":
        testnetConf.defaultDataDir = \
            os.path.expanduser("~/Library/Ethereum")
        testnetConf.nonDefaultRootDir = "/tmp/"+testnetConf.networkID
    elif ostype == "Linux":
        testnetConf.defaultDataDir = os.path.expanduser("~/.ethereum")
        testnetConf.nonDefaultRootDir = "/tmp/"+testnetConf.networkID
    elif ostype == "Windows":
        testnetConf.defaultDataDir = \
            os.path.expanduser("\\~\\AppData\\Roaming\\Ethereum")
        testnetConf.nonDefaultRootDir = \
            os.path.expanduser("\\~\\AppData\\Local\\Temp\\") + \
            testnetConf.networkID
    else:  # This is not supported
        print "Sorry, check the Ethereum docs for your Operating system"
        exit()
    # Check the genesis_block file
    genesisBlock()
    # Check the enode lookup Javascript
    enodeURLJS()
    if DEBUG():
        print(testnetConf)


def installSteps():  # Instructions on how to install Ethereum for specific OS
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
        print "     You\'re on Windows, but it is not yet supported."
    else:  # This is not supported
        print "     Sorry, check the Ethereum docs for your Operating system"


def checkEthereum():  # Checks whether Ethereum (Geth) is installed
    print "Checking whether Ethereum (Geth) is installed..."
    retcode = os.system("geth --help >/dev/null 2>&1")
    if retcode != 0:
        print " ...no current installation of Ethereum:"
        installSteps()
        print "     Exiting."
        exit()
    else:
        print " ...already installed Ethereum, nice! Proceeding..."


def writeStaticNodes(enodes):  # Writes to the static nodes file
    if DEBUG():
        print "Writing enode to static nodes file: " + enodes
    if os.path.isfile(os.path.join(confDir, testnetConf.staticNodes)):
        if DEBUG():
            print "Static nodes file exists, overwriting."
    else:
        if DEBUG():
            print "Writing new static nodes file to: " + \
                    os.path.join(confDir, testnetConf.staticNodes)
    staticNodes = \
        open(os.path.join(confDir, testnetConf.staticNodes), "w")
    staticNodes.write(enodes)
    staticNodes.close


def create():  # Creates a clustered set of nodes
    print "Creating..."
    init()  # Should be all set up at this point
    global enodes
    for node_id in range(0, testnetConf.nodeCount):
        ethCmd = "geth " \
                 "--genesis " + os.path.join(confDir, "genesis_block.json") + \
                 " --nodiscover" \
                 " --verbosity " + str(testnetConf.verbosity)

        if node_id > 0:  # Then this is not the default node
            ethCmd += " --datadir " + \
                        os.path.join(testnetConf.nonDefaultRootDir, str(node_id))

        ethCmd += \
            " --networkid "+testnetConf.networkID + \
            " --identity "+testnetConf.nodeIdentity+str(node_id) + \
            " --port "+testnetConf.ethPort+str(node_id) + \
            " --rpcport "+testnetConf.rpcPort+str(node_id) +  \
            " js " + os.path.join(confDir, "enode_lookup.js")

        # Call the command and handle the response
        print "Creating nodeID: " + str(node_id)
        proc = subprocess.Popen(ethCmd,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )
        stdout_value, stderr_value = proc.communicate()
        # Check the output
        retcode = proc.returncode
        if retcode == 0:  # All is good, process the ennode URL and add to file
            # TODO: TRIM trailing whitespace / carriage returns...
            enodeURL = re.sub(r'\[\:\:\]', testnetConf.ipAddress, stdout_value)
            enodeURL = enodeURL.strip()
            if DEBUG():
                print 'Enode URL:', enodeURL
        else:
            print 'Create failed with the following errors:', repr(stderr_value)
            exit()
        # Construct the enodeURL string to write to the static nodes file
        if node_id == 0:
            enodes = "[ \n"
        enodes += '"' + enodeURL + '"'
        if node_id == (testnetConf.nodeCount - 1):  # final node to write
            enodes += " \n]"
        else:
            enodes += ",\n"

        # Write this to the static nodes file
        writeStaticNodes(enodes)

        print "Setting coinbase to node"
        addAcc(node_id)

    # Now start them up, each will copy over the static nodes file to data dir
    for i in range(0, testnetConf.nodeCount):
        start(i)


def addAcc(node_id):  # Adds an account to a node TODO
    print "Adding account: TODO check passwd file..."
    # Need to check passwd file is in conf, or write new one
    # TODO:

    ethCmd = "geth " \
             " --networkid "+testnetConf.networkID + \
             " --identity "+testnetConf.nodeIdentity+str(node_id) + \
             " --port "+testnetConf.ethPort+str(node_id) + \
             " --rpcport "+testnetConf.rpcPort+str(node_id) + \
             " --verbosity " + str(testnetConf.verbosity) + \
             " --password " + os.path.join(confDir, "testnet-pwd")
    if node_id > 0:  # Then this is not the default node
            ethCmd += " --datadir " + \
                    os.path.join(testnetConf.nonDefaultRootDir, str(node_id))
    ethCmd += " account new"
    proc = subprocess.Popen(ethCmd,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            )
    stdout_value, stderr_value = proc.communicate()
    # Check the output
    retcode = proc.returncode
    if retcode == 0:
        print "Added new account for node ID: " + str(node_id) + \
                ", " + stdout_value
    else:
        print 'Adding account failed with the following errors:', repr(stderr_value)
        exit()


def unlockAcc():  # Unlocks a specified account
    print "Unlock account... TODO"


def getlines(fd):
    line = bytearray()
    c = None
    while True:
        c = fd.read(1)
        if c is None:
            return
        line += c
        if c == '\n':
            yield str(line)
            del line[:]  # Handler to manage STDERR output, for debugging


def startEthAsSub(cmd):  # Spawns a subprocess
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         shell=True)
    for line in getlines(p.stdout):
        if DEBUG():
            print line
        if "IPC endpoint opened" in line:
            print "STARTUP OK"
            break
    else:
        print "STARTUP FAILED"


def start(node_id):  # Starts up a specified node
    print "Starting... " + str(node_id)
    ethCmd = "geth " \
             " --networkid "+testnetConf.networkID + \
             " --identity "+testnetConf.nodeIdentity+str(node_id) + \
             " --port "+testnetConf.ethPort+str(node_id) + \
             " --rpcport "+testnetConf.rpcPort+str(node_id) + \
             " --verbosity " + str(testnetConf.verbosity) + \
             " --nodiscover"
    if node_id > 0:  # Then this is not the default node
            ethCmd += " --datadir " + \
                    os.path.join(testnetConf.nonDefaultRootDir, str(node_id))
            shutil.copy(os.path.join(confDir, testnetConf.staticNodes),
                        os.path.join(testnetConf.nonDefaultRootDir,
                                     str(node_id)))
    else:  # This is the default, cp the static_nodes file to default
        shutil.copy(os.path.join(confDir, testnetConf.staticNodes),
                    testnetConf.defaultDataDir)
    # Start up...
    p = multiprocessing.Process(target=startEthAsSub, args=(ethCmd,))
    p.start()
    p.join()
    print "Node, " + str(node_id) + ", started with PID: "+str(p.pid)
    # Write PID to root of data_dir
    writePIDFile(node_id, p.pid)


def startAll():  # Starts all nodes in the cluster
    print "Starting all..."


def stop(nodeID):  # Stops a specified node
    print "Stopping..."
    # os.kill(proc.pid, signal.SIGUSR1)
    # os.remove() will remove a file (for PID)


def stopAll():  # Stops all nodes in the cluster
    print "Stopping all..."


def attach(nodeID):  # Runs geth --attach against a given node
    print "Attaching..."


def mine(stopStart, nodeID, cores):  # Starts a miner at a node
    # See https://gist.github.com/makevoid/701d516182e38658f5d0 for loading
    # Javascript that will start mining if transactions are found...
    print "Mining..."


def clean(nodeID):  # Removes the data for a given node
    print "Cleaning node ID: "+nodeID
    # os.remove() will remove a file.


def cleanAll():  # Removes all node data in the cluster
    print "Cleaning all..."
    # os.rmdir() will remove an empty directory.
    # shutil.rmtree() will delete a directory and all its contents.


def usage():  # Help / Usage - just prints out to console
    print "     python testnet.py [param]"
    print "     params:"
    print "         --create [node_num]: Creates a new testnet cluster."
    print "         --addacc [node_id] : Creates a account on the node."
    print "         --unlockacc [node_id] [account_no] : Unlocks account given"
    print "         --start [node_id] : Starts the local test node"
    print "         --startall : Starts all the configured local test nodes"
    print "         --stop [node_id] : Stops a given local test node"
    print "         --stopall : Stops all the running local test nodes"
    print "         --attach [node_id] : attaches to a running node"
    print "         --mine [stop|start] [node_id] [cores] : starts the miner"
    print "         --clean [node_id] : Removes the node from the cluster"
    print "         --cleanall : Cleans all nodes from cluseter"
    print "         --help -h : This message"
    exit()


def handleInput():  # Handles the commandline input
    # Take any arguments put in
    args = sys.argv
    if len(args) > 1:
        if args[1] == "--create":
            create()
        elif args[1] == "--addacc":
            if len(args) == 3:
                addacc(args[2])
            else:
                print "Correct usage: python testnet.py --addacc [nodeID]."
        elif args[1] == "--unlockacc":
            unlockAcc()
        elif args[1] == "--start":
            if len(args) == 3:
                start(args[2])
            else:
                print "Correct usage: python testnet.py --start [nodeID]."
        elif args[1] == "--startall":
            startAll()
        elif args[1] == "--stop":
            if len(args) == 3:
                stop(args[2])
            else:
                print "Correct usage: python testnet.py --stop [nodeID]."
        elif args[1] == "--stopall":
            stopAll()
        elif args[1] == "--attach":
            if len(args) == 3:
                attach(args[2])
            else:
                print "Correct usage: python testnet.py --attach [nodeID]."
        elif args[1] == "--mine":
            if len(args) == 5:
                mine(args[2], args[3], args[4])
            else:
                print "Correct usage: python testnet.py --mine [start or stop]"
                " [nodeID] [the number of cores to be used]."
        elif args[1] == "--clean":
            if len(args) == 3:
                clean(args[2])
            else:
                print "Correct usage: python testnet.py --clean [nodeID]."
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

###############################################################################
# Starts the script off
###############################################################################
handleInput()
