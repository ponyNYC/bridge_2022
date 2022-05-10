import re
from django.shortcuts import render
from django.views import View
from bridgeapp.models import Category, Thread, Response

class BridgeHomeView(View):
    def get(self, request):
       categories = Category.objects.all()

       return render(
           request=request,
           template_name='bridge.html',
           context={
               'categories': categories,
           },
       ) 
# Create your views here.
