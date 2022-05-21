from django.urls import path, re_path
from .views import BridgeHomeView, BridgeCategoryView, BridgeThreadView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', BridgeHomeView.as_view(), name='home'),
    path('categories/<int:category_id>/<str:category_slug>',
         BridgeCategoryView.as_view(), name='category'),
    path('threads/<int:thread_id>/<int:resp_id>',
         BridgeThreadView.as_view(), name='thread'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
