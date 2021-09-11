from Alerts.serializers import AlertSerializers,AlertTestSerializers
from Alerts.models import AlertModel,KryptoCoin
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework  import status
from django_filters.rest_framework import DjangoFilterBackend

from pprint import pprint as p
from Alerts.helpers.task_manager import send_updates;
from Alerts.helpers.requests_manager import get_bitcoin_price,get_coin_price
from django.core.exceptions import ObjectDoesNotExist


class AlertView(APIView):
    # permission_classes = [IsAuthenticated]

    @api_view(['GET'])
    # @permission_classes([IsAuthenticated])
    def listAlertsALL(self):
        alerts = AlertModel.objects.all();
        send_updates();
        serializer = AlertSerializers(alerts,many=True)

        return Response(serializer.data);
    

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def listAlerts(self):
        user = self.user;
        alerts = AlertModel.objects.filter(user=user)
        serializer = AlertSerializers(alerts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK);
    
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def addAlert(request):
        """
        Add Alert
        """
        try:
            data = request.data;
            data['user'] = request.user;
            coin = data.get('coin');
            if(not coin):
                raise Exception('Coin is required');
            
            coin = KryptoCoin.objects.get(pk=coin);
            data['coin'] = coin;
            serializer = AlertSerializers()
            instance = serializer.create(data);
            return Response({'status':True},status=status.HTTP_201_CREATED);
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def alert(self,id):
        try:
            user = self.user;
            alert_instance = AlertModel.objects.get(id=id);
            if(alert_instance.user != user):
                raise Exception("Not Authorized")
            serializer = AlertSerializers(alert_instance)
            return Response(serializer.data,status=status.HTTP_200_OK);
        except ObjectDoesNotExist:
            return Response(data={"status":404, "error":"not found", "message":"Alert not found"},status=status.HTTP_404_NOT_FOUND);
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    def deleteAlert(request,id):
        try:
            alert_instance = AlertModel.objects.get(id=id).delete();
            return Response({'status':200,'status':True},status=status.HTTP_200_OK);
        except ObjectDoesNotExist:
            return Response(data={"status":404, "error":"not found", "message":"Alert not found"},status=status.HTTP_404_NOT_FOUND);
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def activate(request,id):
        """
        Activate Alert
        """
        try:
            user = request.user;
            alert_instance = AlertModel.objects.get(id=id);
            if(alert_instance.user != user):
                raise Exception("Not Authorized")
            alert_instance.status = AlertModel.STATUS_LISTEN;
            alert_instance.save()
            serializer = AlertSerializers(alert_instance)
            return Response(serializer.data,status=status.HTTP_200_OK);
        except ObjectDoesNotExist:
            return Response(data={"status":404, "error":"not found", "message":"Alert not found"},status=status.HTTP_404_NOT_FOUND);
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def deactivate(request,id):
        """
        Deactivate Alert
        """
        try:
            user = request.user;
            alert_instance = AlertModel.objects.get(id=id);
            if(alert_instance.user != user):
                raise Exception("Not Authorized")
            alert_instance.status = AlertModel.STATUS_SLEEP;
            alert_instance.save()
            serializer = AlertSerializers(alert_instance)
            return Response(serializer.data,status=status.HTTP_200_OK);
        except ObjectDoesNotExist:
            return Response(data={"status":404, "error":"not found", "message":"Alert not found"},status=status.HTTP_404_NOT_FOUND);
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class AlertList(viewsets.ModelViewSet):
class AlertList(generics.ListCreateAPIView):
    """
    List all alerts (Testing).
    """
    queryset = AlertModel.objects.all()
    serializer_class = AlertTestSerializers
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'check']
    # permission_classes = [IsAuthenticated]