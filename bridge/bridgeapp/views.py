from django.shortcuts import render, redirect
from django.views import View
from django.utils.text import slugify
from .models import Category, Thread, Response
from .forms import InputForm, ThreadForm
# from bridgeapp.forms import NewThreadForm
from datetime import date

CATEGORIES = Category.objects.all()
CUR_YEAR = date.today().year
# class BridgeCategoryView(View):
class BridgeHomeView(View):
    def get(self, request):

        return render(
           request=request,
        #    template_name='categories.html',
           template_name='home.html',
           context={
               'categories': CATEGORIES,
               'year': CUR_YEAR,
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
class BridgeCategoryView(View):
    # def get(self, request, category_slug):
    def get(self, request, category_id, category_slug):
        category = Category.objects.get(id=category_id)
        # chosen_category = Category.objects.get(slug=category_slug)
        # chosen_slug = Category.objects.get(slug=category_slug)
        threads = Thread.objects.filter(categories=category).order_by('-date')
        form = ThreadForm(initial={'body': 'What do you want to ask?'})

        return render(
            request=request,
            template_name='category.html',
            context={
                'categories': CATEGORIES,
                'year': CUR_YEAR,
                # 'chosen_category': chosen_category,
                'category': category,
                'threads': threads,
                # 'type': category_type,
                # 'slug': chosen_slug,
                'thread_form': form,
            },
        )

    def post(self, request, category_id, category_slug):
        """Get form data and create new thread"""
        form = ThreadForm(request.POST)
        id, slug = category_id, category_slug
        if form.is_valid():
            data = form.cleaned_data
            question, cat_ids = data['body'], data['category_ids']
            if cat_ids:
                thread = Thread.objects.create(body=question)
                for cat_id in cat_ids:
                    category = Category.objects.get(id=cat_id)
                    thread.categories.add(category)
                id, slug = cat_ids[0], slugify(Category.objects.get(id=cat_ids[0]).type)
        return redirect('category', category_id=id, category_slug=slug)

# class BridgeResponseView(View):
class BridgeThreadView(View):
    def get(self, request, thread_id, resp_id):
        # categories = Category.objects.get(type=category_id)
        # thread_object = Thread.objects.get(id=thread_id)
        # print("Here in BridgeResponseView!")
        # print(thread_object)
        # response_form=ResponseForm()
        thread = Thread.objects.get(id=thread_id)
        responses = Response.objects.filter(thread=thread)
        form = InputForm(initial={'body': 'Write a response to the question.' if not resp_id else Response.objects.get(id=resp_id).body})

        return render(
           request=request,
           template_name='thread.html',
           context={
               'categories': CATEGORIES,
               'year': CUR_YEAR,
               'responses' : responses,
               'response_form' : form,
                # 'id' : thread_id,
               'thread' : thread,
               'id': resp_id if resp_id else 0,
           },
       )

    def post(self, request, thread_id, resp_id):
        # response_form = InputForm(request.POST)
        # # print('In the post function')
        # if response_form.is_valid():
        #     response_body = response_form.cleaned_data['body']
        #     Response.objects.create(body=response_body, thread_id=thread_id)

        # return redirect('response', thread_id)
        form = InputForm(request.POST)
        if form.is_valid():
            resp_text = form.cleaned_data['body']
            if 'create' in request.POST:
                Response.objects.create(body=resp_text, thread_id=thread_id)
            elif 'update' in request.POST:
                Response.objects.filter(id=resp_id).update(body=resp_text)
            elif 'remove' in request.POST:
                Response.objects.filter(id=resp_id).delete()

        return redirect('thread', thread_id, 0)

# class BridgeCreateView(View):
#     """Handles the new_thread.html page"""
#     def get(self, request):
#         """Display page and present NewThreadForm"""
#         categories = Category.objects.all()
#         form = ThreadForm()

#         return render(
#            request=request,
#            template_name='new_thread.html',
#            context={
#                'categories': categories,
#                'thread_form': form,
#            },
#        )

#     def post(self, request):
#         """Get form data and create new thread"""
#         form = ThreadForm(request.POST)
#         id, slug = 0, None
#         if form.is_valid():
#             data = form.cleaned_data
#             question, cat_ids = data['body'], data['category_ids']
#             thread = Thread.objects.create(body=question)
#             for cat_id in cat_ids:
#                 category = Category.objects.get(id=cat_id)
#                 thread.categories.add(category)
#             id, slug = cat_ids[0], slugify(Category.objects.get(id=cat_ids[0]).type)
#         return redirect('category', category_id=id, category_slug=slug)

# class BridgeUpdateView(View):
#     def get(self, request, response_id):
#         # thread_object = Thread.objects.get(id=thread_id)
#         # responses = Response.objects.filter(thread=thread_object)
#         response_obj = Response.objects.get(id=response_id)
#         form = InputForm(initial={'body': response_obj.body})
#         # thread_id = response_obj.thread_id

#         return render(
#            request=request,
#            template_name='update.html',
#            context={
#                'form' : form,
#                'response_obj' : response_obj,
#                'id' : response_id,
#            },
#        )
#     def post(self, request, response_id):
#         response_obj2 = Response.objects.get(id=response_id)
#         thread_id = response_obj2.thread_id

#         if 'save' in request.POST:
#             form = InputForm(request.POST)
#             if form.is_valid():
#                 response_body = form.cleaned_data['body']
#                 response_obj2.body=response_body
#                 response_obj2.save()
#         elif 'delete' in request.POST:
#             response_obj2.delete()

#         return redirect('response', thread_id)
