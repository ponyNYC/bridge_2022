import imp
from django.urls import path
from .views import BridgeHomeView

urlpatterns = [
    path('', BridgeHomeView.as_view(), name='bridge'),
]