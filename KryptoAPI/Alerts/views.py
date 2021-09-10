from Alerts.serializers import AlertSerializers,AlertTestSerializers
from Alerts.models import AlertModel
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from pprint import pprint as p
from Alerts.helpers.db_handler import send_updates;
from Alerts.helpers.requests_manager import get_bitcoin_price,get_coin_price
from django.core.exceptions import ObjectDoesNotExist

from Alerts.tasks import send_email_task


class AlertView(APIView):
    # permission_classes = [IsAuthenticated]

    # TODO Testing
    @api_view(['GET'])
    # @permission_classes([IsAuthenticated])
    def listAlertsALL(self):
        alerts = AlertModel.objects.all();
        data = send_updates(get_coin_price());
        for i in data:
            print(i.get('recepinet'),i.get('body'))
            # send_email_task.delay(i.get('recepinet'),i.get('body'))
        serializer = AlertSerializers(alerts,many=True)

        return Response(serializer.data);
    

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def listAlerts(self):
        user = self.user;
        alerts = AlertModel.objects.filter(user=user)
        serializer = AlertSerializers(alerts,many=True)
        return Response(serializer.data);
    
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def addAlert(request):
        try:
            data = request.data;
            data['user'] = request.user;
            serializer = AlertSerializers()
            instance = serializer.create(data);
            return Response({'status':200,'status':True})
        except Exception as e:
            return Response(e)
    
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def alert(self,id):
        try:
            user = self.user;
            alert_instance = AlertModel.objects.get(id=id);
            if(alert_instance.user != user):
                raise Exception("Not Authorized")
            serializer = AlertSerializers(alert_instance)
            return Response(serializer.data);
        except ObjectDoesNotExist:
            return Response(data={"status":404, "error":"not found", "message":"Alert not found"})
        except Exception as e:
            return Response(e)
    
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    def deleteAlert(request,id):
        try:
            alert_instance = AlertModel.objects.get(id=id).delete();
            return Response({'status':200,'status':True})
        except ObjectDoesNotExist:
            return Response(data={"status":404, "error":"not found", "message":"Alert not found"})
        except Exception as e:
            return Response(e)

    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def activate(request,id):
        try:
            user = request.user;
            alert_instance = AlertModel.objects.get(id=id);
            if(alert_instance.user != user):
                raise Exception("Not Authorized")
            alert_instance.status = AlertModel.STATUS_LISTEN;
            alert_instance.save()
            serializer = AlertSerializers(alert_instance)
            return Response(serializer.data);
        except ObjectDoesNotExist:
            return Response(data={"status":404, "error":"not found", "message":"Alert not found"})
        except Exception as e:
            return Response(e)
    
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def deactivate(request,id):
        try:
            user = request.user;
            alert_instance = AlertModel.objects.get(id=id);
            if(alert_instance.user != user):
                raise Exception("Not Authorized")
            alert_instance.status = AlertModel.STATUS_SLEEP;
            alert_instance.save()
            serializer = AlertSerializers(alert_instance)
            return Response(serializer.data);
        except ObjectDoesNotExist:
            return Response(data={"status":404, "error":"not found", "message":"Alert not found"})
        except Exception as e:
            return Response(e)

# class AlertList(viewsets.ModelViewSet):
class AlertList(generics.ListAPIView):
    queryset = AlertModel.objects.all()
    serializer_class = AlertTestSerializers
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'check']
    # permission_classes = [IsAuthenticated]