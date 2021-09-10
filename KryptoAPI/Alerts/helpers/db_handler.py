
from Alerts.models import AlertModel,KryptoCoin

def send_updates(coin_price):

    alert_instances_dropped = get_price_dropped_alerts(coin_price)
    alert_instances_risen = get_price_risen_alerts(coin_price)
    
    data = mail_context(alert_instances_dropped,coin_price);
    data.extend(mail_context(alert_instances_risen,coin_price));

    return data


def mail_context(alert_queryset, cur_price):
    mailContext = []

    for i in alert_queryset:
        temp = {}
        temp['recepinet']=i.user.email
        i.status = AlertModel.STATUS_SLEEP;
        i.save()
        msg  = ''
        if(i.check==AlertModel.CHECK_LOWERLIMIT):
            msg = "Price has dropped below" + str(i.price) +"do check. Now it is " + str(cur_price);
        else:
            msg = "Price has risen from" + str(i.price) +"do check. Mow it is " + str(cur_price);
        temp['body'] = msg
        mailContext.append(temp)
    return mailContext


def get_price_dropped_alerts(coin_price,coin):
    alert_instances_dropped = AlertModel.objects.filter(
        status = AlertModel.STATUS_LISTEN,
        check = AlertModel.CHECK_LOWERLIMIT,
        price__gte = coin_price);
    return alert_instances_dropped;


def get_price_risen_alerts(coin_price,coin):
    alert_instances_risen = AlertModel.objects.filter(
        status = AlertModel.STATUS_LISTEN,
        check = AlertModel.CHECK_UPPERLIMIT,
        price__lte = coin_price);
    return alert_instances_risen;


