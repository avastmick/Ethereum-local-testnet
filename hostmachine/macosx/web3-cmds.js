// General cmds to run in the Geth interactive console

// List accounts
eth.Accounts

// Ether held by default account (accounts[0])
web3.fromWei(eth.getBalance(eth.coinbase), "ether")
