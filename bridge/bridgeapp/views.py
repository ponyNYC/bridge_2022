from django.shortcuts import render, redirect
from django.views import View
from django.utils.text import slugify
from .models import Category, Thread, Response
from .forms import ResponseForm, ThreadForm
from datetime import date

# Set global variable for all items in Category table
CATEGORIES = Category.objects.all()
# Set global variable for today's date
CUR_YEAR = date.today().year


class BridgeHomeView(View):
    """Home URL view - Display 3 category options"""
    def get(self, request):

        return render(
            request=request,
            template_name='home.html',
            context={
                'categories': CATEGORIES,
                'year': CUR_YEAR,
            },
        )


class BridgeCategoryView(View):
    """Get Thread table from database and display threads associated with Category selected on Home Page"""
    def get(self, request, category_id, category_slug):  #category_slug needed for UI
        category = Category.objects.get(id=category_id)
        threads = Thread.objects.filter(categories=category).order_by('-date')
        form = ThreadForm()

        return render(
            request=request,
            template_name='category.html',
            context={
                'categories': CATEGORIES,
                'year': CUR_YEAR,
                'category': category,
                'threads': threads,
                'thread_form': form,
            },
        )

    def post(self, request, category_id, category_slug):
        """Create new thread & select applicable categories- Many to many relationship between categories and threads"""
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
                id, slug = cat_ids[0], slugify(
                    Category.objects.get(id=cat_ids[0]).type)

        return redirect('category', category_id=id, category_slug=slug)  #redirects to first selected Category


class BridgeThreadView(View):
    """Get Response table from database and display responses associated with Thread selected"""
    def get(self, request, thread_id, resp_id):
        thread = Thread.objects.get(id=thread_id)
        responses = Response.objects.filter(thread=thread)
        form = ResponseForm(initial={'body': Response.objects.get(
            id=resp_id).body if resp_id else ''})

        return render(
            request=request,
            template_name='thread.html',
            context={
                'categories': CATEGORIES,
                'year': CUR_YEAR,
                'responses': responses,
                'response_form': form,
                'thread': thread,
                'id': resp_id if resp_id else 0,
            },
        )

    def post(self, request, thread_id, resp_id):
        """Autopopulate Response Form and allow for Create, Update or Delete of ID"""
        form = ResponseForm(request.POST)
        if form.is_valid():
            resp_text = form.cleaned_data['body']
            if 'create' in request.POST:
                Response.objects.create(body=resp_text, thread_id=thread_id)
            elif 'update' in request.POST:
                Response.objects.filter(id=resp_id).update(body=resp_text)
            elif 'remove' in request.POST:
                Response.objects.filter(id=resp_id).delete()

        return redirect('thread', thread_id, 0)
