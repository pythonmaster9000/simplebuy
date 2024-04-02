from swaps import raydium, solutils
import json
from solana.rpc.api import Client, Pubkey
from solders.keypair import Keypair
from solana.rpc.commitment import Commitment
import base58
import time

lamps = 1000000000

rpc = "https://raydium-raydium-5ad5.mainnet.rpcpool.com/"
rpc_headers = {'authority': 'raydium-raydium-5ad5.mainnet.rpcpool.com', 'accept': '*/*',
               'accept-language': 'en-US,en;q=0.9', 'cache-control': 'no-cache',
               'content-type': 'application/json', 'dnt': '1', 'origin': 'https://raydium.io',
               'pragma': 'no-cache', 'referer': 'https://raydium.io/',
               'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
               'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty',
               'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site',
               'solana-client': 'js/0.0.0-development',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                             'like Gecko) Chrome/120.0.0.0 Safari/537.36', }
with open('config.json', 'r') as file:
    config = json.load(file)
    private_key = config.get('private_key', 'no private key')


client = Client(rpc, commitment=Commitment(
        "confirmed"), timeout=30, extra_headers=rpc_headers)
our_keypair = Keypair.from_bytes(base58.b58decode(private_key))


def buy(coin_address: str, sol_amount: float):
    swapper = raydium.RaySwap(client, coin_address, sol_amount, our_keypair)
    while True:
        result = swapper.buy()
        if result:
            return result


def sell(coin_address: str):
    swapper = raydium.RaySwap(client, coin_address, 0.0, our_keypair)
    print(swapper.sell())


def check_balance(coin_address: str):
    swapper = raydium.RaySwap(client, coin_address, 0.0, our_keypair)
    return swapper.check_balance()


def check_price(coin_address: str):
    swapper = raydium.RaySwap(client, coin_address, 0.0, our_keypair)
    return swapper.check_price()


if __name__ == "__main__":
    while True:
        res = input('b/s/p (buy, sell, check price) ')
        if res.lower() == 'b':
            coin = input('coin ')
            amount = float(input('sol '))
            print(buy(coin, amount))
            print('congrats you got a shitcoin!')
        if res.lower() == 's':
            coin = input('coin to sell ')
            sell(coin)
        if res.lower() == 'p':
            coin = input('coin to check price ')
            # coin = 'EokVz9yWqGj8jGobr8VZqf5tVJKjS1fU9AUZHq4Gjmum'
            res_bal = check_balance(coin)
            res_price = check_price(coin)
            print(res_price[0], 'price per token')
            real_balance = res_bal / res_price[1]
            print('token value', real_balance * res_price[0])
