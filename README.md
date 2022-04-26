# Capstone One: 
## Simplified Ethereum Block Explorer

Ethereum is a leading force in the crypto-currency space today. It has the most active developers and arguably the most economic activity of all blockchains. However, there is still much work to be done on providing a user-friendly interface when it comes to interacting with the blockchain or gathering information from it. A block explorer like [Etherscan.io]([https](https://etherscan.io/)) shows a ton of information that can be hard to understand at times, especially for the average person.

1. The goal of this capstone is to emulate an ethereum block explorer like Etherscan, but with the average user in mind. Strip away all the insane detail, timestamps, conversions, etc. and leave only the easily digestable information for the user. This project will look to create a minimalistic front-end for the ethereum blockchain. It will have:
   * Main page with some general ethereum statistics as well as a search bar to enter a Block#/TransactionHash/Wallet Address.
     * Block# - Shows basic info of the block 
     * TransactionHash - Shows basic info of the transaction
     * Wallet Address - Shows basic info of the wallet
   * User Page: User will have the option to login and store a list of wallets they own/want to watch. Wallets can be grouped by the user to show total value
   * New to Eth Page: Shows some basic info / links to sites that give greate beginner knowledge to get the user started.

2. The demographic of users I'm targeting with this capstone are your basic ethereum users. People who have just started learning about crypto and Ethereum specificly but feel overwhelemed by some of the currently existing blockchain explorers available. I'll also hope to get people who are curious about Ethereum but have yet to take the plunge.

3. I have multiple different APIs the backend will be calling to. I'll also be using a PostgreSQL database to help keep within the free.99 call limits. The front-end will query/pull data on Users from the DB as well as some statisical data. The backend will handle passing requests on Block#/TransactionHash/Wallet Address info and filter the information given back to ensure only what is needed is passed on to the user.

4. API Used:
   * [Etherscan.io](https://docs.etherscan.io/getting-started/creating-an-account)
     * General Limits: 5 calls/seccond - 100k calls/day
     * Free community endpoints only
   * [Web3py](https://web3py.readthedocs.io/en/latest/quickstart.html)
     * [Connect to Infura HTTP node](https://docs.infura.io/infura/)
     * used to help conversions from/to hex as well as from/to Wei (Base Eth Unit)
     * can also be used to get additional info not accessible from Etherscan API for free

## Database Schema

![database schema](https://github.com/KKlob/Capstone1/tree/main/imgs/db_schema.PNG "Database Schema for Minimalistic Block Explorer")