import imp
from django.urls import path
from bridgeapp.views import BridgeHomeView, BridgeCategoryView, BridgeThreadView, BridgeResponseView, BridgeCreateView, BridgeUpdateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', BridgeHomeView.as_view(), name='bridge'),
    path('categories/', BridgeCategoryView.as_view(), name='categories'),
    path('thread/', BridgeThreadView.as_view(), name='thread'),
    path('response/', BridgeResponseView.as_view(), name='response'),
    path('createthread/', BridgeCreateView.as_view(), name='create'),
    path('updateresponse/', BridgeUpdateView.as_view(), name='update'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

print(str(urlpatterns))