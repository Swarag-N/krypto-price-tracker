import requests
from Alerts.models import AlertModel

def get_bitcoin_price():
    prices = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false').json()
    return prices[0]['current_price']


def send_updates(btc_price):
    price_risen = []
    price_dropped = []

    alert_instances_dropped = get_price_dropped_alerts(btc_price)
    alert_instances_risen = get_price_risen_alerts(btc_price)

    

def get_price_dropped_alerts(btc_price):
    # SET TRigger to done before returning 
    # alert_instances_dropped = AlertModel.objects.filter(
    #     status = AlertModel.STATUS_LISTEN,
    #     check = AlertModel.CHECK_LOWERLIMIT,
    #     price__lte = btc_price).values('id');
    
    # val = AlertModel.objects.filter(pk__in=alert_instances_dropped).update(status = AlertModel.STATUS_TRIGGER)
    alert_instances_dropped = AlertModel.objects.filter(
        status = AlertModel.STATUS_LISTEN,
        check = AlertModel.CHECK_LOWERLIMIT,
        price__gte = btc_price);
    return alert_instances_dropped


def get_price_risen_alerts(btc_price):
    alert_instances_risen = AlertModel.objects.filter(
        status = AlertModel.STATUS_LISTEN,
        check = AlertModel.CHECK_UPPERLIMIT,
        price__lte = btc_price);
    return alert_instances_risen
