import json
from typing import Dict
import requests
from datetime import datetime
from web3 import Web3
import codecs


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

def getSearchResult(cat, term):
    """Builds correct get request to Web3/Infura API based on cat (category: block/tx/address
    If error, print it and return None
    """

    if (cat is "block"):
        try:
            resp = w3.eth.get_block(int(term))
            return resp
        except requests.exceptions.RequestException as error:
            return {"error": error}

def cleanUpResp(resp):
    """Cleans up data for our front end"""
    cleanResp = {}
    cleanResp["number"] = resp.number
    cleanResp["timestamp"] = datetime.fromtimestamp(resp.timestamp)
    cleanResp["miner"] = resp.miner
    cleanResp["difficulty"] = resp.difficulty
    cleanResp["transactions"] = len(resp.transactions)

    return cleanResp

def handleSearch(term):
    """Main Handler for search. Keeps app.py clean"""
    check = detectSearch(term)
    if ("term" in check):
        resp = getSearchResult(check["term"], term)
        if "error" not in resp:
            cleanResp = cleanUpResp(resp)
            return cleanResp
        else:
            return resp
        
    elif ("invalid" in check):
        return check