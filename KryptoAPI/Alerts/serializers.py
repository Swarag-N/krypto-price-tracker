from django.db.models import fields
from rest_framework import serializers
from Alerts.models import AlertModel,KryptoCoin

class AlertSerializers(serializers.ModelSerializer):

    class Meta:
        model = AlertModel
        exclude = ('user', )
        depth = 1
    
    # def create(self, validated_data):
    #     validated_data['user'] = self.context.get('request').user;
    #     return super().create(validated_data)
class AlertTestSerializers(serializers.ModelSerializer):
    class Meta:
        model = AlertModel
        fields = '__all__'

class KryptoCoinSerializers(serializers.ModelSerializer):
    class Meta:
        model = KryptoCoin
        fields = '__all__'