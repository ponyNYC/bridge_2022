import imp
from django.urls import path
from bridgeapp.views import BridgeHomeView, BridgeCategoryView, BridgeThreadView, BridgeResponseView, BridgeCreateView, BridgeUpdateView
from django.conf import settings
from django.conf.urls.static import static
from django.template.defaultfilters import slugify

urlpatterns = [
    path('', BridgeCategoryView.as_view(), name='categories'),
    path('categories/thread/<int:thread_id>', BridgeResponseView.as_view(), name='response'),
    path('updateresponse/<int:response_id>', BridgeUpdateView.as_view(), name='update'),
    path('threads/<str:category_slug>', BridgeThreadView.as_view(), name='threads'),
    path('threads/new', BridgeCreateView.as_view(), name='new_thread'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
