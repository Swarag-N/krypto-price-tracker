from django.db.models import fields
from rest_framework import serializers
from Alerts.models import AlertModel;

class AlertSerializers(serializers.ModelSerializer):

    class Meta:
        model = AlertModel
        exclude = ('user', )
    
    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user;
        return super().create(validated_data)