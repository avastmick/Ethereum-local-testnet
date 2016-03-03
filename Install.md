# Fresh Install to create a local testnet

## Node 1 - An Ubuntu guest VM (server)

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
echo 'geth --genesis ./genesis/genesis_block.json --networkid 1973 --port 30801 --rpcport 8901 --nodiscover' > create_local_testnet && chmod u+x create_local_testnet
````
Then create the base account and coinbase:
````
echo 'geth --networkid 1973 --port 30801 --rpcport 8901 --password ./conf/testnet-pwd account new' > create_local_coinbase && chmod u+x create_local_coinbase
````
Then: unlock the account
````
echo 'geth --password ./conf/testnet-pwd --unlock 0  --networkid 1973 --port 30801 --rpcport 8901' > unlock_local_account && chmod u+x unlock_local_account
````

Then: start the console and pipe the logs for tailing in other terminal:
````
echo 'geth --networkid 1973 --port 30801 --rpc --rpcaddr "192.168.99.100" --rpcport 8901 --rpcapi "admin,db,eth,net,web3" --rpccorsdomain "http://192.168.99.100:8901" --nodiscover console 2>> eth.log' > start_local_console && chmod u+x start_local_console
````
Then: add mining
````
echo 'geth --mine --rpccorsdomain "http://localhost:8901" --ipcapi "admin,eth,miner" --rpcapi "db,eth,net,web3" --networkid 1973 --port 30801 --rpcport 8901 --nodiscover --minerthreads 1 console 2>> eth.log' > mine_local_testnet && chmod u+x mine_local_testnet
````

Then: create a clean script
````
echo 'rm -rf .ethereum && rm -rf .ethash && rm eth.log' > clean_local && chmod u+x clean_local
````
Finally, to make this easier, ensure that SSH is enabled on guest and port forwarding is set-up for all required ports. Then everything can be driven from the host machine and use the nicer tools there:
````
// Set up SSH port forwarding IF USING NAT - though that will only allow local guest usage of node CLI / RPC
VBoxManage modifyvm "[THE NAME OF THE GUEST]" --natpf1 "ssh,tcp,,[SOMEUNUSED PORT],,22"
````
