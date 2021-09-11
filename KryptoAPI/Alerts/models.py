from django.db import models
# from django.contrib.auth.models import User
from Authentication.models import User

# Create your models here.

class KryptoCoin(models.Model):
    """
    KryptoCoin model
    """
    name = models.CharField(max_length=20)
    gecko_code = models.CharField(max_length=10,unique=True)
    cur_usd = models.IntegerField();

    def __str__(self) -> str:
        return self.name + " "+self.gecko_code

class AlertModel(models.Model):
    """
    Alert model
    """
    # COIN_BITCOIN = 'BTC'
    # COIN_ETHERURM = 'ETH'

    STATUS_SLEEP = 0;
    STATUS_LISTEN = 1;
    STATUS_TRIGGER = 2;
    
    CHECK_UPPERLIMIT = 'U'
    CHECK_LOWERLIMIT = 'L'

    # AVAILABLE_COINS = (
    #     (COIN_BITCOIN,'Bitcoin'),
    #     (COIN_ETHERURM,'Etherurm')) 
    
    STATUS_TYPE = (
        (STATUS_LISTEN,'listening for changes'),
        (STATUS_TRIGGER,'sending notification'),
        (STATUS_SLEEP,'deactivated'))
    
    CHECK_TYPE = (
        (CHECK_UPPERLIMIT,'check if price go above'),
        (CHECK_LOWERLIMIT,'check if price drops bellow')
    )
    user = models.ForeignKey(User, related_name='user_alert', on_delete=models.CASCADE)
    coin = models.ForeignKey(KryptoCoin, related_name='coin_alert', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_TYPE)
    check = models.CharField(max_length=1,choices=CHECK_TYPE)
    price = models.IntegerField()


    def __str__(self) -> str:
        return self.user.email+" "+str(self.price)+" "+self.coin.name




    
