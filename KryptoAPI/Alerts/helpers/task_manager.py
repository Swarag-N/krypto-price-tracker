
from Alerts.models import AlertModel,KryptoCoin

def send_updates():
    """
    This function will send mail to all the users who have an alert to a coin
    """
    coins = KryptoCoin.objects.all()
    data = []
    for coin in coins:
        alert_instances_dropped = get_price_dropped_alerts(coin)
        alert_instances_risen = get_price_risen_alerts(coin)
        
        data.extend(mail_context(alert_instances_dropped,coin));
        data.extend(mail_context(alert_instances_risen,coin));
    print(data)
    return data


def mail_context(alert_queryset, coin):
    """
    This function will return the mail context for the alert
    """
    mailContext = []

    for i in alert_queryset:
        temp = {}
        temp['recepinet']=i.user.email
        i.status = AlertModel.STATUS_SLEEP;
        i.save()
        msg  = ''
        subj = ''
        if(i.check==AlertModel.CHECK_LOWERLIMIT):
            subj = 'Price Dropped ' + coin.name;
            msg = "Price has dropped below" + str(i.price) +"do check. Now it is " + str(coin.cur_usd);
        else:
            subj = 'Price Risen ' + coin.name;
            msg = "Price has risen from" + str(i.price) +"do check. Mow it is " + str(coin.cur_usd);
        temp['body'] = msg
        temp['subj'] = subj
        print(temp.get(subj))
        mailContext.append(temp)
    return mailContext


def get_price_dropped_alerts(coin):
    """
    This function will return the alert instances which are in the status of LISTEN and check is LOWERLIMIT
    """
    alert_instances_dropped = AlertModel.objects.filter(
        status = AlertModel.STATUS_LISTEN,
        check = AlertModel.CHECK_LOWERLIMIT,
        coin=coin,
        price__gte = coin.cur_usd);
    return alert_instances_dropped;


def get_price_risen_alerts(coin):
    """
    This function will return the alert instances which are in the status of LISTEN and check is UPPERLIMIT
    """
    alert_instances_risen = AlertModel.objects.filter(
        status = AlertModel.STATUS_LISTEN,
        check = AlertModel.CHECK_UPPERLIMIT,
        coin=coin,
        price__lte = coin.cur_usd);
    return alert_instances_risen;


