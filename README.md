# Capstone One: 
## Minimalistic Ethereum Block Explorer

Ethereum is a leading force in the crypto-currency space today. It has the most active developers and arguably the most economic activity of all blockchains. However, there is still much work to be done on providing a user-friendly interface when it comes to interacting with the blockchain or gathering information from it. A block explorer like [Etherscan.io]([https](https://etherscan.io/)) shows a ton of information that can be hard to understand at times, especially for the average person.

1. The goal of this capstone is to emulate an ethereum block explorer like Etherscan, but with the average user in mind. Strip away all the insane detail, timestamps, conversions, etc. and leave only the easily digestable information for the user. This project will look to create a minimalistic front-end for the ethereum blockchain. It will have:
   * Main page with some general ethereum statistics as well as a search bar to enter a Block#/TransactionHash/Wallet Address.
     * Block# - Shows basic info of the block 
     * TransactionHash - Shows basic info of the transaction
     * Wallet Address - Shows basic info of the wallet
   * User Page: User will have the option to login and store a list of wallets they own/want to watch. Wallets can be grouped by the user to show total value
     * Will show each group separately as well as detail of each wallet's contents in each group
     * Will allow a user to filter results based on:
       * group name
       * amount of eth/token
       * if group/wallet has token
       * total amount of group / wallet
   * Eth Education Page: Shows some basic info / links to sites that give greate beginner knowledge to get the user started.

2. The demographic of users I'm targeting with this capstone are your basic ethereum users. People who have just started learning about crypto and Ethereum specificly but feel overwhelemed by some of the currently existing blockchain explorers available. I'll also hope to get people who are curious about Ethereum but have yet to take the plunge.

3. I'll be using Etherscan.io's API for most all data necessary to show the user. The Web3py/Infura SDK will be used primarily to help encode/decode hex values as well as get some information not accessible from Etherscan's API. I'll also be using a PostgreSQL database to help keep within the free.99 call limits. The front-end will query/pull data on Users from the DB as well as some statisical data. The backend will handle passing requests on Block#/TransactionHash/Wallet Address info and filter the information given back to ensure only what is needed is passed on to the user.

4. API Used:
   * [Etherscan.io](https://docs.etherscan.io/getting-started/creating-an-account)
     * General Limits: 5 calls/seccond - 100k calls/day
     * Free community endpoints only
   * [Web3py](https://web3py.readthedocs.io/en/latest/quickstart.html)
     * [Connect to Infura HTTP node](https://docs.infura.io/infura/)
     * used to help conversions from/to hex as well as from/to Wei (Base Eth Unit)
     * can also be used to get additional info not accessible from Etherscan API for free

## Database Schema

<img src="https://github.com/KKlob/Capstone1/blob/main/imgs/db_schema.PNG" alt="Database Schema" height="500" width="500"/>

* Users
  * id - Primary Key, autoincrement
  * username - unique non-nullable
  * password - hashed+salted non-nullable

* Wallet_Groups
  * id - Primary Key, autoincrement
  * group_name - String
  * owner - ForeignKey -> Users.username

* Wallets
  * id - Primary Key, autoincrement
  * wallet_address - String
  * eth_total - Float
  * tokens - String
    * using json.dumps() Format: {"tokens": [{"name": "Maker", "symbol": "MKR", "total": 1 }, {etc}]}
    * easily store all tokens associated with a wallet / easily update token list
  * group_id - Int ForeignKey -> Wallet_Groups.id
  * owner - Int ForeignKey -> Users.username

* Eth_Stats
  * total_supply - Float
  * total_supply_eth2 - Float
  * last_price - Float
  * safe_gas - String
  * prop_gas - String
  * fast_gas - String
    * safe_gas, prop_gas, and fast_gas using json.dumps() Format: {"gwei": "20", "wei": "20000000000", "est_conf": "9227"}
      * gwei - commonly used value for gas pricing in Eth
      * wei - smallest base value for Eth
      * est_conf - estimated confirmation time in secconds
  * base_fee - Float


## Potential Issues

1. Rate limits
    * Need to write logic for backend to ensure rate limits are not reached. All front-end requests look to the database when applicable.

2. Sensitive Information
    * Only a user's password for their account is truly sensative. No real names / identifying info will be needed. All wallet_groups will only be viewable by the user that owns them.

## Additional Information

1. User Flow
    * A user will be brought to the Main page and has the option to:
      * search for a block# / Transaction Hash / Wallet Address
      * Login
        * redirects to user's wallet groups page on successful login
        * loggout redirects to main page
      * Go to Eth Education Page


2. CRUD requirements
    * Fulfilled via user login + wallet groups
    * Fulfilled via cacheing data in db

3. Beyond CRUD
    * Filter methods for user's wallet groups
    * Gas price estimates converted to be understood easily

4. Stretch Goals
    * Naming system for wallets
      * hex code for wallet is abstracted away
      * can search for wallet via name instead of hex code
    * Defi / Cefi Page
      * shows info on various DeFi services (Uniswap, Aave, Curve, etc.)
      * shows info on various CeFi services (Coinbase, Gemini, etc.)
    * Crypto Converter
      * easy-to-use calculator for converting Fiat / Eth / Tokens
    * Filter a wallet's transactions
      * filter via amount/token/timestamp
