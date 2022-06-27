# Capstone 1
## [Minimalistic Ethereum Block Explorer](https://www.mebe.herokuapp.com)

Ethereum is a leading force in the crypto-currency space today. It has the most active developers and arguably the most economic activity of all blockchains. However, there is still much work to be done on providing a user-friendly interface when it comes to interacting with the blockchain or gathering information from it. A block explorer like [Etherscan.io]([https](https://etherscan.io/)) shows a ton of information that can be hard to understand at times, especially for the average person.

MEBE is an app that simplifies the information displayed by a typical block explorer like Etherscan.io. Currently the app covers the basics:


* Displays general network stats
  * Total ETH Supply
  * Totaly ETH2 Supply
  * Last ETH Price
  * Base Network Fee
  * Safe gas fee + Est. time to confirmation
  * Proposed gas fee + Est. time to confirmation
  * Fast gas fee + Est. time to confirmation
* Search for basic Block / Transaction / Wallet info
* Allows for user login to create a watchlist of wallet addresses


## Tech Stack
* Flask / SqlAlchemy backend
* Javascript / Jinja front-end
* PSQL Database to store eth network stats + user profiles + wallet watchlists


## APIs used
* Etherscan.io API
* Web3 python library + Infura Web Socket


## Features To Be Included
* Wallet Watchlist Totals
  * Add a section that calculates total ETH between all wallets on the watchlist
* Wallet Groups
  * User can chose to group wallets together to get group totals
* Token List
  * List tokens each wallet address holds + totals
* Wallet Transaction Dropdown
  * Dropdown for each wallet that shows Eth transactions + token transactions
* Defi Page
  * Page that shows stats for the top Decentralized Finace Protocols (Uniswap, Aave, Curve, etc.)

## ToDo
#### Work to be done on existing app
* ReWrite DB setup
* Beautify the app (currently basic bootstrap)
