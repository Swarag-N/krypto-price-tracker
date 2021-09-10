import requests

def get_bitcoin_price():
    prices = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false').json()
    return prices[0]['current_price']
