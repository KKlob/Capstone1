import json
from tracemalloc import start
from typing import Dict
import requests
from datetime import datetime
from web3 import Web3
import codecs
import aiohttp
import asyncio
from secret_keys import API_SECRET_KEY


w3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/e6e6ec7525d74b8ca50f79f1e2e0e986'))

def detectSearch(term):
    """Detects if term is a block# / Tx hash / wallet address / invalid
    Returns {"term": "block/tx/address/invalid"}
    or
    Returns {"invalid": "Reason for invalid here. To be flashed to user"}
    """
    try:
        blockNum = int(term)
        return {"term": "block"}

    except ValueError:
        if (w3.isAddress(term)):
            return {"term": "address"}
        elif (len(term) > 42 and term.rfind("0x") == 0):
            return {"term": "tx"}
        else:
            return {"invalid": "Search Term is not a block#, Tx hash, or wallet address"}

def getAddressInfo(term):
    """Handles the async calls for getting Eth Balance, list of 'Normal' Txs, and list of 'Internal' txs. Returns Dict of results"""

    base_url = "https://api.etherscan.io/api?module=account&action={}"

    endBlock = int(w3.eth.get_block_number())
    startBlock = 0

    # reqs is a dict of all the terms for each request to Etherscan API
    reqs = {"balance": f"&address={term}&tag=latest&apikey={API_SECRET_KEY}",
            "txlist": f"&address={term}&startBlock={startBlock}&endblock={endBlock}&page=1&offset=10&sort=dsc&apikey={API_SECRET_KEY}",
            "txlistinternal": f"&address={term}&startblock={startBlock}&endblock={endBlock}&page=1&offset=10&sort=dsc&apikey={API_SECRET_KEY}"}

    # titles will help organize the results to return
    titles = ['eth_balance', 'eth_txs', 'token_txs']

    # We want to pass the address as part of results
    results = {"address": term}

    def get_tasks(session):
        tasks = []
        for action in reqs.keys():
            tasks.append(asyncio.create_task(session.get(base_url.format(action) + reqs[action])))
        return tasks

    async def get_address_info():
        async with aiohttp.ClientSession() as session:
            tasks = get_tasks(session)
            responses = await asyncio.gather(*tasks)
            for index, resp in enumerate(responses):
               results[titles[index]] = await resp.json()

    asyncio.run(get_address_info())
    return results

def getSearchResult(cat, term):
    """Builds correct get request to Web3/Infura API based on cat (category: block/tx/address
    If error, print it and return None
    """
    try:
        if (cat is "block"):
            resp = w3.eth.get_block(int(term))
            return resp

        elif (cat is "tx"):
            resp = w3.eth.get_transaction(term)
            return resp

        elif (cat is "address"):
            resp = getAddressInfo(term)
            return resp

    except requests.exceptions.RequestException as error:
            return {"error": error}

def cleanUpResp(cat, resp):
    """Cleans up data for our front end"""
    if (cat is "block"):
        cleanResp = {"category": cat}
        cleanResp["number"] = resp.number
        cleanResp["timestamp"] = datetime.fromtimestamp(resp.timestamp)
        cleanResp["miner"] = resp.miner
        cleanResp["difficulty"] = resp.difficulty
        cleanResp["transactions"] = len(resp.transactions)
        cleanResp["es_link"] = f"etherscan.io/block/{resp.number}"

    elif (cat is "tx"):
        cleanResp = {"category": cat}
        cleanResp["hash"] = w3.toHex(resp.hash)
        cleanResp["blockNumber"] = resp.blockNumber
        cleanResp["from"] = resp["from"]
        cleanResp["to"] = resp.to
        cleanResp["value"] = float(w3.fromWei(resp.value, 'ether'))
        cleanResp["es_link"] = f"etherscan.io/tx/{cleanResp['hash']}"

    elif (cat is "address"):
        cleanResp = {"category": cat}
        cleanResp["eth_balance"] = float(w3.fromWei(int(resp["eth_balance"]["result"]), 'ether'))
        cleanResp["address"] = resp["address"]
        cleanResp["eth_txs"] = resp["eth_txs"]["result"]
        cleanResp["token_txs"] = resp["token_txs"]["result"]
        cleanResp["es_link"] = f"etherscan.io/address/{resp['address']}"

    return cleanResp

def handleSearch(term):
    """Main Handler for search. Keeps app.py clean"""
    check = detectSearch(term)
    if ("term" in check):
        resp = getSearchResult(check["term"], term)
        if "error" not in resp:
            cleanResp = cleanUpResp(check["term"], resp)
            return cleanResp
        else:
            return resp
        
    elif ("invalid" in check):
        return check