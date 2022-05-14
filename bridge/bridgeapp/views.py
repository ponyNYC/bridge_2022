from django.shortcuts import render, redirect
from django.views import View
from .models import Category, Thread, Response
from .forms import NewThreadForm
from datetime import date

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

class BridgeCategoryView(View):
    def get(self, request):
       categories = Category.objects.all()

       return render(
           request=request,
           template_name='categories.html',
           context={
               'categories': categories,
           },
       )

class BridgeThreadView(View):
    def get(self, request):
       categories = Category.objects.all()

       return render(
           request=request,
           template_name='thread.html',
           context={
               'categories': categories,
           },
       )

class BridgeResponseView(View):
    def get(self, request):
       categories = Category.objects.all()

       return render(
           request=request,
           template_name='categories.html',
           context={
               'categories': categories,
           },
       )

class BridgeCreateView(View):
    """Handles the new_thread.html page"""
    def get(self, request):
        """Display page and present NewThreadForm"""
        categories = Category.objects.all()
        form = NewThreadForm()
        year = date.today().year

        return render(
           request=request,
           template_name='new_thread.html',
           context={
               'categories': categories,
               'thread_form': form,
               'year': year,
           },
       )

    def post(self, request):
        """Get form data and create new thread"""
        form = NewThreadForm(request.POST)
        id = 0
        if form.is_valid():
            question = form.cleaned_data['body']
            cat_ids = form.cleaned_data['category_ids']
            thread = Thread.objects.create(body=question)
            for cat_id in cat_ids:
                category = Category.objects.get(id=cat_id)
                thread.categories.add(category)
            id = cat_ids[0]
        # Redirect to the todo homepage
        return redirect('categories', id)

class BridgeUpdateView(View):
    def get(self, request):
       categories = Category.objects.all()

       return render(
           request=request,
           template_name='categories.html',
           context={
               'categories': categories,
           },
       )
