# Fresh Install to create a local testnet

## Node 1

Set up user and su:
````
sudo useradd -d /home/testnet -m -s /bin/bash testnet
sudo passwd testnet
[new password]
su - testnet
````
Set up configuration
````
mkdir genesis &&
mkdir conf
````
Then:
````
vi genesis/genesis_block.json
````
Paste in:
````
{
    "nonce": "0x0000000000000042",
    "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "difficulty": "0x4000",
    "alloc": {},
    "coinbase": "0x0000000000000000000000000000000000000000",
    "timestamp": "0x00",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "extraData": "Custom Ethereum Genesis Block for initiating a local test net",
    "gasLimit": "0xffffffff"
}
````
Then:
````
echo 'testpwd-01' > conf/testnet-pwd
````
Then:
````
echo 'geth --genesis ./genesis/genesis_block.json --networkid 1973 --port 30801 --rpcport 8901 --nodiscover --maxpeers 0' > 1_create_local_testnet && chmod u+x 1_create_local_testnet
````
Then create the base account and coinbase:
````
echo 'geth --networkid 1973 --port 30801 --rpcport 8901 --password ./conf/testnet-pwd account new' > 2_create_local_coinbase && chmod u+x 2_create_local_coinbase
````
Then: unlock the account
````
echo 'geth --password ../../conf/testnet-pwd --unlock 0  --networkid 1973 --port 30801 --rpcport 8901 --rpccorsdomain localhost' > 3_unlock_local_account && chmod u+x 3_unlock_local_account
````

Then: start the console and pipe the logs for tailing in other terminal:
````
echo 'geth --networkid 1973 --port 30801 -rpc --rpcport 8901 --rpcapi "db,eth,net,web3" console 2>> eth.log' > start_local_console && chmod u+x start_local_console
````
Then: add mining
````
echo 'geth --mine -rpccorsdomain "*" --ipcapi "admin,eth,miner" --rpcapi "db,eth,net,web3" --networkid 1973 --port 30801 --rpcport 8901 -maxpeers 0 --minerthreads 1 console 2>> eth.log' > mine_local_testnet && chmod u+x mine_local_testnet
````

Then: create a clean script
````
echo 'rm -rf .ethereum && rm -rf .ethash && rm eth.log' > clean_local && chmod u+x clean_local
````
