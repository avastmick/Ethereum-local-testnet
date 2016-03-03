// General cmds to run in the Geth interactive console

// List accounts
eth.accounts

// To test RPC
curl -X POST --data '{"jsonrpc":"2.0", "method":"eth_accounts", "params":"[]","id_":1}' http://localhost:8901


// Ether held by default account (accounts[0])
web3.fromWei(eth.getBalance(eth.coinbase), "ether")

// Unlock accounts
//personal.unlockAccount(address, password)

personal.unlockAccount("6ecb7876d6b473e2267043d5324f4d0a0fc5c51c", "testpassword1")
personal.unlockAccount("4ca216f32c4523a2f88e6a6b5688492c46b7adff", "testpassword1")
