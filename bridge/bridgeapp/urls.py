from django.urls import path, re_path
from .views import BridgeHomeView, BridgeCategoryView, BridgeThreadView
# from .views import BridgeHomeView, BridgeCategoryView, BridgeThreadView, BridgeCreateView, BridgeUpdateView
from django.conf import settings
from django.conf.urls.static import static
# from django.template.defaultfilters import slugify

urlpatterns = [
    # path('', BridgeCategoryView.as_view(), name='categories'),
    # path('categories/<str:category_slug>', BridgeThreadView.as_view(), name='threads'),
    # path('categories/thread/<int:thread_id>', BridgeResponseView.as_view(), name='response'),
    # path('updateresponse/<int:response_id>', BridgeUpdateView.as_view(), name='update'),
    # path('thread/new', BridgeCreateView.as_view(), name='new_thread'),
    path('', BridgeHomeView.as_view(), name='home'),
    path('categories/<int:category_id>/<str:category_slug>', BridgeCategoryView.as_view(), name='category'),
    path('threads/<int:thread_id>/<int:resp_id>', BridgeThreadView.as_view(), name='thread'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
