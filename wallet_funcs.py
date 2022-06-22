from multiprocessing.sharedctypes import Value
from sqlalchemy import BigInteger
#from secret_keys import API_SECRET_KEY
import requests
from eth_stat_funcs import API_SECRET_KEY, w3
import os

API_SECRET_KEY = os.environ.get('ES_API_KEY')

def get_eth_bal(address):
    """Handles fetching data, scrubing data, and returning either float eth_bal"""
    wei_bal = get_address_data(address)
    eth_bal = scrub_data(wei_bal)
    return eth_bal

def get_address_data(addr):
    """fetches raw addr data"""
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={addr}&tag=latest&apikey={API_SECRET_KEY}"

    resp = requests.get(url)
    return resp.json()['result']

def scrub_data(wei_bal):
    """Takes in array of raw_data, returns single clean dict."""
    try:
        wei = int(wei_bal)
    except ValueError as err:
        return 0
    eth = float(w3.fromWei(wei, 'ether'))
    return eth

def update_balances(wallet_arr):
    """Takes in array of wallet slqa objects, updates balances for each"""
    addr_arr = [wallet.wallet_address for wallet in wallet_arr]
    address_str = ",".join(addr_arr)
    url = f"https://api.etherscan.io/api?module=account&action=balancemulti&address={address_str}&tag=latest&apikey={API_SECRET_KEY}"

    resp = requests.get(url)
    data = resp.json()['result']

    def convert_bal(addr_arr):
        """Converts balance for each wallet in array"""
        for wallet in addr_arr:
            bal = wallet['balance']
            wallet['balance'] = float(w3.fromWei(int(bal), 'ether'))
        return addr_arr

    convert_data = convert_bal(data)
    return data