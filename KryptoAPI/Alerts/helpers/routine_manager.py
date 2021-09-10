from .requests_manager import get_coin_price,get_coins_price
from Alerts.models import KryptoCoin

GECKO_CODE = 'gecko_code'
# Update all coin values
# Check with Alerts
# Send Mails
def updateCoinValues():
    """
    Update Price Values of all coins 
    """
    coin_instances =  KryptoCoin.objects.all();
    q = ""
    for coin in coin_instances:
        q+=coin.gecko_code+","
    data = get_coins_price(q[:-1])

    for coin in coin_instances:
        coin.cur_usd = data.get(coin.gecko_code).get('usd')
    
    KryptoCoin.objects.bulk_update(coin_instances, ['cur_usd'])
