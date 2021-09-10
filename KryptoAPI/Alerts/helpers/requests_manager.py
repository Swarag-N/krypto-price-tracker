import requests

def get_bitcoin_price():
    # https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd
    data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
    prices = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false').json()
    print(data)
    return prices[0]['current_price']

def get_coin_price(coin='bitcoin',curr='usd'):
    data = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={curr}').json();
    return data.get(coin).get(curr)
