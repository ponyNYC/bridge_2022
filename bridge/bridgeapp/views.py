from django.shortcuts import render, redirect
from django.views import View
from django.utils.text import slugify
from .models import Category, Thread, Response
from .forms import ResponseForm, ThreadForm
from datetime import date
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
# globals (categories, current year) for all views
CATEGORIES = Category.objects.all()
CUR_YEAR = date.today().year


class BridgeHomeView(View):
    """View for home page"""

    def get(self, request):
        """GET home page"""
        # render with categories and current year
        # login_form = AuthenticationForm()
        # form = UserCreationForm()
        return render(
            request=request,
            template_name='home.html',
            context={
                'categories': CATEGORIES,
                'year': CUR_YEAR,
                # 'login_form': login_form,
                # 'form': form
            },
        )

    # def post(self, request):
    #     if request.POST.get('submit') == 'sign_in':
    #         login_form = AuthenticationForm(request.POST)
    #         user = authenticate(login_form.username, login_form.password)
    #         login(request, user)
    #         return redirect('home')

    #     else:
    #         form = UserCreationForm(request.POST)
    #         if form.is_valid():
    #             form.save()
    #             username = form.cleaned_data['username']
    #             password = form.cleaned_data['password1']
    #             user = authenticate(username=username, password=password)
    #             login(request, user)
    #             return redirect('home')


class BridgeCategoryView(View):
    """View for single category page"""

    def get(self, request, category_id, category_slug):  # slug for URL
        """GET single category page"""
        # get requested category from DB
        category = Category.objects.get(id=category_id)
        # get all threads under category in desc chronological order
        threads = Thread.objects.filter(categories=category).order_by('-date')
        # get ThreadForm for POST action
        form = ThreadForm()
        # render with category, threads & ThreadForm
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
        """POST thread in single category page"""
        # get POST data from ThreadForm
        form = ThreadForm(request.POST)
        # assign URL parameters to id, slug
        id, slug = category_id, category_slug
        # check if form data is valid
        if form.is_valid():
            # clean out valid data as 'data'
            data = form.cleaned_data
            # assign body, category_ids values in data to question, cat_ids
            question, cat_ids = data['body'], data['category_ids']
            # check if user selected > 1 category
            if cat_ids:
                # create a new thread
                thread = Thread.objects.create(body=question)
                # assign all categories selected by user to new thread
                for cat_id in cat_ids:
                    category = Category.objects.get(id=cat_id)
                    thread.categories.add(category)
                # aassign values of first category to id & slug for redirection
                id, slug = cat_ids[0], slugify(
                    Category.objects.get(id=cat_ids[0]).type)
        # redirect to single category page
        return redirect('category', category_id=id, category_slug=slug)


class BridgeThreadView(View):
    """View for single thread page"""

    def get(self, request, thread_id, resp_id):
        """GET single thread page"""
        # get requested thread from DB
        thread = Thread.objects.get(id=thread_id)
        # get all responses to thread in desc chronological order
        responses = Response.objects.filter(thread=thread).order_by('-date')
        # get ResponseForm for POST action & prepopulate if updating
        form = ResponseForm(initial={'body': Response.objects.get(
            id=resp_id).body if resp_id else ''})
        # render with thread, responses, ResponseForm & response_id
        return render(
            request=request,
            template_name='thread.html',
            context={
                'categories': CATEGORIES,
                'year': CUR_YEAR,
                'responses': responses,
                'response_form': form,
                'thread': thread,
                # resp_id defaults to 0 ('*/responses')
                'id': resp_id if resp_id else 0,
            },
        )

    def post(self, request, thread_id, resp_id):
        """POST response in single thread page"""
        # get POST data from ResponseForm
        form = ResponseForm(request.POST)
        # check if form data is valid
        if form.is_valid():
            # clean out valid data as 'resp_text'
            resp_text = form.cleaned_data['body']
            # create new response if POST action is 'create'
            if 'create' in request.POST:
                Response.objects.create(body=resp_text, thread_id=thread_id)
            # update existing response if POST action is 'update'
            elif 'update' in request.POST:
                Response.objects.filter(id=resp_id).update(body=resp_text)
            # remove existing response if POST action is 'remove'
            elif 'remove' in request.POST:
                Response.objects.filter(id=resp_id).delete()
        # redirect to single thread page
        return redirect('thread', thread_id, 0)


class BridgeAuthenticationView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        form = UserCreationForm()

        context = {'login_form': login_form, 'form': form}
        return render(request, 'registration/authentication.html', context)

    def post(self, request):
        if request.POST.get('submit') == 'sign_in':
            login_form = AuthenticationForm(request.POST)
            user = authenticate(login_form.username, login_form.password)
            login(request, user)
            return redirect('home')

        else:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('home')


def logout(request):
    logout(request)
