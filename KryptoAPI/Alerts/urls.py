from django.urls import path

from Alerts.views import AlertList,AlertView

urlpatterns = [
    path('viewset/', AlertList.as_view()),
    path('test/',AlertView.listAlertsALL,name="Testing Alerts"),

    path('create/',AlertView.addAlert,name="Add Alerts"),
    path('list',AlertView.listAlerts,name="list TOD Pagination and FIlter"),

    path('<id>/view',AlertView.alert,name="view alert"),

    path('<id>/activate',AlertView.activate,name="Activate"),
    path('<id>/deactivate',AlertView.deactivate,name="deactivate"),
    
    path('<id>/delete',AlertView.deleteAlert,name="Delete Alert"),
]