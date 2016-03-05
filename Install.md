# Create a local testnet

## Node 1 - An Ubuntu guest VM (server)

### Set-up Ethereum
Ensure that Ethereum is installed, including the Solidity compiler:
````
sudo add-apt-repository ppa:ethereum/ethereum-qt &&
sudo add-apt-repository ppa:ethereum/ethereum &&
sudo add-apt-repository ppa:ethereum/ethereum-dev &&
sudo apt-get update &&
sudo apt-get install cpp-ethereum
````

### Set up user and su:
````
sudo useradd -d /home/testnet -m -s /bin/bash testnet
sudo passwd testnet
[new password]
su - testnet
````


## Configure installation of testnet
Set up configuration
````
mkdir genesis &&
mkdir conf
````
Then create a genesis block file:
````
echo '{
    "nonce": "0x0000000000000042",
    "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "difficulty": "0x4000",
    "alloc": {},
    "coinbase": "0x0000000000000000000000000000000000000000",
    "timestamp": "0x00",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "extraData": "Custom Ethereum Genesis Block for initiating a local test net",
    "gasLimit": "0xffffffff"
}' > tmp.json
````
Then create a test password file to create accounts

*DON'T DO THIS WHEN CREATING A NODE THAT WILL ATTACH TO A PUBLIC NETWORK!!*:
````
echo 'testpwd-01' > conf/testnet-pwd
````
## Create scripts to do the creation of the testnet
### Create the local testnet
````
echo 'geth --genesis ./genesis/genesis_block.json --networkid 1973 --port 30801 --rpcport 8901 --nodiscover 2>> eth.log &' > create_local_testnet && chmod u+x create_local_testnet
````
### Create the base account coinbase:
````
echo 'geth --networkid 1973 --port 30801 --rpcport 8901 --password ./conf/testnet-pwd account new' > create_local_coinbase && chmod u+x create_local_coinbase
````
### Create a script to unlock the accounts
````
echo 'geth --password ./conf/testnet-pwd --unlock 0  --networkid 1973 --port 30801 --rpcport 8901' > unlock_local_account && chmod u+x unlock_local_account
````

### Script to start the console and pipe the logs for tailing in another terminal:
````
echo 'geth --networkid 1973 --port 30801 --rpc --rpcaddr "192.168.99.100" --rpcport 8901 --rpcapi "admin,db,eth,net,web3" --rpccorsdomain "http://192.168.99.100:8901" --nodiscover console 2>> eth.log' > start_local_console && chmod u+x start_local_console
````
### Script to mine the blockchain
*Though this can be easily done in the console:*
````
> miner.start(1);
admin.sleepBlocks(1);
miner.stop();
````
echo 'geth --mine --rpccorsdomain "http://localhost:8901" --ipcapi "admin,eth,miner" --rpcapi "db,eth,net,web3" --networkid 1973 --port 30801 --rpcport 8901 --nodiscover --minerthreads 1 2>> eth.log' > mine_local_testnet && chmod u+x mine_local_testnet
````

### Finally create a clean script to start over
````
echo 'rm -rf .ethereum && rm -rf .ethash && rm eth.log' > clean_local && chmod u+x clean_local
````
