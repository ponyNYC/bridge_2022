from django.urls import path, re_path
from .views import BridgeHomeView, BridgeCategoryView, BridgeThreadView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # main page accessed @ /bridge
    path('', BridgeHomeView.as_view(), name='home'),
    # aggregated thread for a single category page
    path('categories/<int:category_id>/<str:category_slug>',
         BridgeCategoryView.as_view(), name='category'),
    # individual question thread page
    path('threads/<int:thread_id>/<int:resp_id>',
         BridgeThreadView.as_view(), name='thread'),
    # adds static files to url paths so they can be accessed and/or displayed
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
