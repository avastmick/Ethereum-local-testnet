// A set of commands that allow automated / easy admin of the testnet

// Unlock accounts
function unlockAllAccounts() { var i=0; eth.accounts.forEach( function(e){ personal.unlockAccount(eth.accounts[i], "testpwd-01"); console.log("  Unlocked eth.accounts["+i+"]: "+eth.accounts[i]); i++; } )};
console.log("Added function: unlockAllAccounts()");

// Checking balances
function checkAllBalances() { var i =0; eth.accounts.forEach( function(e){ console.log("  eth.accounts["+i+"]: " +  e + " \tbalance: " + web3.fromWei(eth.getBalance(e), "ether") + " ether"); i++; })};
console.log("Added function: checkAllBalances()");
