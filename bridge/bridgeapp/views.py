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

    def get(self, request, category_id, category_slug):  # category_slug needed for UI
        # assigns list of category object id's to category variable
        category = Category.objects.get(id=category_id)
        # assigns threads filtered by category and ordered by date to threads variable
        threads = Thread.objects.filter(categories=category).order_by('-date')
        # assigns ThreadForm from forms.py to form variable
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
        # assigns category_id parameter to id variable and category_slug parameter to slug variable
        id, slug = category_id, category_slug
        # if statement tests whether the form is valid, and if not valid the form will not post
        if form.is_valid():
            # assigns cleaned form data (via built-in Django method) to the data variable
            data = form.cleaned_data
            # assigns the data entered in form by user to question and cat_ids variables
            question, cat_ids = data['body'], data['category_ids']
            # tests whether user has selected at least 1 category and prevents form submission if not true
            if cat_ids:
                # assigns newly created Thread object containing user-entered data to thread variable
                thread = Thread.objects.create(body=question)
                # loops through category ids selected by user and adds selected categories as foreign key to the current thread
                for cat_id in cat_ids:
                    category = Category.objects.get(id=cat_id)
                    thread.categories.add(category)
                # assigns the first item in the cat_ids list to id variable and assigns the slugified cat_ids type attribute to slug variable
                id, slug = cat_ids[0], slugify(
                    Category.objects.get(id=cat_ids[0]).type)
        # redirects to view for first selected Category
        return redirect('category', category_id=id, category_slug=slug)


class BridgeThreadView(View):
    """Get Response table from database and display responses associated with Thread selected"""

    def get(self, request, thread_id, resp_id):
        # assigns the selected thread_id object to thread variable
        thread = Thread.objects.get(id=thread_id)
        # assigns Response objects filtered by selected thread to responses variable
        responses = Response.objects.filter(thread=thread)
        # assigns ResponseForm from forms.py to form variable with the initial value of the text of the selected response
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
                # references selected resp_id and defaults to 0 if none selected
                'id': resp_id if resp_id else 0,
            },
        )

    def post(self, request, thread_id, resp_id):
        """Autopopulate Response Form and allow for Create, Update or Delete of ID"""
        # assigns POST request from ResponseForm to form variable
        form = ResponseForm(request.POST)
        # tests whether form is valid (via built-in Django method)
        if form.is_valid():
            # assigns cleaned form data (via built-in Django method) to the resp_text variable
            resp_text = form.cleaned_data['body']
            # tests if user selects create button and creates a new Response object with entered text if so
            if 'create' in request.POST:
                Response.objects.create(body=resp_text, thread_id=thread_id)
            # tests if user selects update button and updates the selected Response object with entered text if so
            elif 'update' in request.POST:
                Response.objects.filter(id=resp_id).update(body=resp_text)
            # tests if user selects remove button and deletes the selected Response object if so
            elif 'remove' in request.POST:
                Response.objects.filter(id=resp_id).delete()
        # redirects to thread view page
        return redirect('thread', thread_id, 0)
