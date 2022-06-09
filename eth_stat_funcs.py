import asyncio
from web3 import Web3
import aiohttp
import json
from secret_keys import API_SECRET_KEY

w3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/e6e6ec7525d74b8ca50f79f1e2e0e986'))

def update_db_eth_stats():
    """Handles all steps to update the eth stats stored in db"""
    raw_stats = get_eth_stats()
    clean_stats = clean_eth_stats(raw_stats)
    return clean_stats


def get_eth_stats():
    """Run multiple async requests to Etherscan API for necessary Eth stats

    Returns a list 
    """

    #db_stats = Eth_Stats.query.first()

    # Perform all requests to Etherscan api to collect information async, then collect all responses before handling updating db

    url = 'https://api.etherscan.io/api?module={}&action={}&apikey={}'
    
    reqs = {'stats': ['ethsupply', 'ethsupply2', 'ethprice'], 'gastracker': ['gasoracle']}

    titles = ['ethsupply', 'ethsupply2', 'ethprice', 'gastracker']

    results = []

    def get_tasks(session):
        tasks = []
        for module in reqs.keys():
            for action in reqs[module]:
                tasks.append(asyncio.create_task(session.get(url.format(module, action, API_SECRET_KEY))))
        return tasks

    async def get_stats():
        async with aiohttp.ClientSession() as session:
            tasks = get_tasks(session)
            responses = await asyncio.gather(*tasks)
            for index, resp in enumerate(responses):
                results.append({titles[index]: await resp.json()})

    asyncio.run(get_stats())
    return results

def clean_eth_stats(raw_stats):
    """Etherscan gives more data than necessary for this app. This function will clean up the data and return it as a dictionary"""

    clean_stats = {}
    gastracker = {}

    for stat in raw_stats:
        if 'ethsupply' in stat.keys():
            clean_stats['total_supply'] = str(stat['ethsupply']['result'])
        elif 'ethsupply2' in stat.keys():
            clean_stats['total_supply_eth2'] = str(float(stat['ethsupply2']['result']['EthSupply']) + float(stat['ethsupply2']['result']['Eth2Staking']) - float(stat['ethsupply2']['result']['BurntFees']))
        elif 'ethprice' in stat.keys():
            clean_stats['last_price'] = float(stat['ethprice']['result']['ethusd'])
        elif 'gastracker' in stat.keys():
            gastracker['result'] = stat['gastracker']['result']
            gas_data = clean_gas_data(gastracker)
            clean_stats['safe_gas'] = gas_data['safe']
            clean_stats['prop_gas'] = gas_data['prop']
            clean_stats['fast_gas'] = gas_data['fast']
            clean_stats['base_fee'] = gas_data['base']

    return clean_stats

def clean_gas_data(gas_data):
    """Gas Tracker Data only gives back prices in gwei. In order to calc estimated conf times, we need to do some extra work.
    
    Uses Web3py to convert gwei to wei, then calls Etherscan api to calc estimated conf time.

    Stores gwei, wei, and conf time as a string via json.dumps()
    Format: {"gwei": "20", "wei": "20000000000", "est_conf": "9227"}
    """
    s_gwei = int(gas_data['result']['SafeGasPrice'])
    s_wei = w3.toWei(s_gwei, 'gwei')
    s_conf = 0

    p_gwei = int(gas_data['result']['ProposeGasPrice'])
    p_wei = w3.toWei(p_gwei, 'gwei')
    p_conf = 0

    f_gwei = int(gas_data['result']['FastGasPrice'])
    f_wei = w3.toWei(f_gwei, 'gwei')
    f_conf = 0

    base_fee = float(gas_data['result']['suggestBaseFee'])

    conf_dict = {'s_wei': s_wei, 'p_wei': p_wei, 'f_wei': f_wei}

    titles = ['s_est_conf', 'p_est_conf', 'f_est_conf']

    results = []

    def get_tasks(session):
        url = 'https://api.etherscan.io/api?module={}&action={}&gasprice={}&apikey={}'
        tasks = []
        for item in conf_dict.keys():
            tasks.append(asyncio.create_task(session.get(url.format('gastracker', 'gasestimate', conf_dict[item], API_SECRET_KEY))))
        return tasks

    async def get_estimates():
        async with aiohttp.ClientSession() as session:
            tasks = get_tasks(session)
            responses = await asyncio.gather(*tasks)
            for index, resp in enumerate(responses):
                results.append({titles[index]: await resp.json()})

    asyncio.run(get_estimates())
    for item in results:
        if 's_est_conf' in item.keys():
            s_conf = int(item['s_est_conf']['result'])
        elif 'p_est_conf' in item.keys():
            p_conf = int(item['p_est_conf']['result'])
        elif 'f_est_conf' in item.keys():
            f_conf = int(item['f_est_conf']['result'])

    safe = {'gwei': s_gwei, 'wei': s_wei, 'est_conf': s_conf}
    prop = {'gwei': p_gwei, 'wei': p_wei, 'est_conf': p_conf}
    fast = {'gwei': f_gwei, 'wei': f_wei, 'est_conf': f_conf}

    gas_data = {}
    gas_data['safe'] = json.dumps(safe)
    gas_data['prop'] = json.dumps(prop)
    gas_data['fast'] = json.dumps(fast)
    gas_data['base'] = base_fee
    
    return gas_data