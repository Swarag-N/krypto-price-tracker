
from Alerts.models import AlertModel


def send_updates(btc_price):

    alert_instances_dropped = get_price_dropped_alerts(btc_price)
    alert_instances_risen = get_price_risen_alerts(btc_price)
    
    data = mail_context(alert_instances_dropped,btc_price);
    data.extend(mail_context(alert_instances_risen,btc_price));

    return data


def mail_context(alert_queryset, cur_price):
    mailContext = []

    for i in alert_queryset:
        temp = {}
        temp['recepinet']=i.user.email
        msg  = ''
        if(i.check==AlertModel.CHECK_LOWERLIMIT):
            msg = "Price has dropped below" + str(i.price) +"do check. Now it is " + str(cur_price);
        else:
            msg = "Price has risen from" + str(i.price) +"do check. Mow it is " + str(cur_price);
        temp['body'] = msg
        mailContext.append(temp)
    return mailContext


def get_price_dropped_alerts(btc_price):
    # TODO Set Trigger to done before returning
    alert_instances_dropped = AlertModel.objects.filter(
        status = AlertModel.STATUS_LISTEN,
        check = AlertModel.CHECK_LOWERLIMIT,
        price__gte = btc_price);
    return alert_instances_dropped;


def get_price_risen_alerts(btc_price):
    # TODO Set Trigger to done before returning
    alert_instances_risen = AlertModel.objects.filter(
        status = AlertModel.STATUS_LISTEN,
        check = AlertModel.CHECK_UPPERLIMIT,
        price__lte = btc_price);
    return alert_instances_risen;
