from django.shortcuts import render, redirect
from django.views import View
from bridgeapp.models import Category, Thread, Response
from bridgeapp.forms import ResponseForm
from bridgeapp.forms import NewThreadForm
from datetime import date

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

# class BridgeThreadView(View):
#     def get(self, request, category_id):
#         categories = Category.objects.get(type=category_id)
#         print(categories)
#         threads = Thread.objects.filter(categories=categories).order_by('date')
#         print("Here in BridgeThreadView!")

#         return render(
#            request=request,
#            template_name='thread.html',
#            context={
#                'categories': categories,
#                'threads' : threads,
#            },
#        ) 
class BridgeThreadView(View):
    def get(self, request, category_slug):
        chosen_category = Category.objects.get(slug=category_slug)
        chosen_slug = Category.objects.get(slug=category_slug)

        threads = Thread.objects.filter(categories=chosen_category).order_by('-date')

        return render(
            request=request,
            template_name='thread.html',
            context={
                'chosen_category': chosen_category,
                'threads': threads,
                # 'type': category_type,
                'slug': chosen_slug,
            },
        ) 

class BridgeResponseView(View):
    def get(self, request, thread_id):
        # categories = Category.objects.get(type=category_id)
        thread_object = Thread.objects.get(id=thread_id)
        print("Here in BridgeResponseView!")
        print(thread_object)
        responses = Response.objects.filter(thread=thread_object)
        response_form=ResponseForm()

        return render(
           request=request,
           template_name='response.html',
           context={
               'responses' : responses,
               'response_form' : response_form,
               'id' : thread_id,
           },
       ) 
    def post(self, request, thread_id):
        response_form=ResponseForm(request.POST)
        print('In the post function')
        if response_form.is_valid():
            response_body = response_form.cleaned_data['body']
            Response.objects.create(body=response_body, thread_id=thread_id)

        return redirect('response', thread_id)


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
        return redirect('categories', id)

class BridgeUpdateView(View):
    def get(self, request, response_id):
        # thread_object = Thread.objects.get(id=thread_id)
        # responses = Response.objects.filter(thread=thread_object)
        response_obj = Response.objects.get(id=response_id)       
        form = ResponseForm(initial={'body': response_obj.body})
        # thread_id = response_obj.thread_id

        return render(
           request=request,
           template_name='update.html',
           context={
               'form' : form,
               'response_obj' : response_obj,
               'id' : response_id,
           },
       ) 
    def post(self, request, response_id):
        response_obj = Response.objects.filter(id=response_id)
        response_obj2 = Response.objects.get(id=response_id)
        thread_id = response_obj2.thread_id

        if 'save' in request.POST:
            form = ResponseForm(request.POST)
            if form.is_valid():
                response_body = form.cleaned_data['body']
                response_obj.update(body=response_body)
        elif 'delete' in request.POST:
            response_obj.delete()

        return redirect('response', thread_id)
