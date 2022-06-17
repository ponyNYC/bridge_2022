from django.urls import path, re_path
from .views import BridgeHomeView, BridgeCategoryView, BridgeThreadView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # home page
    path('', BridgeHomeView.as_view(), name='home'),
    # single category page
    path('categories/<int:category_id>/<str:category_slug>',
         BridgeCategoryView.as_view(), name='category'),
    # single thread page
    path('threads/<int:thread_id>/<int:resp_id>',
         BridgeThreadView.as_view(), name='thread'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # add static assets
