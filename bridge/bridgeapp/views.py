from django.shortcuts import render, redirect
from django.views import View
from django.utils.text import slugify
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from .models import Category, Thread, Response
from .forms import ResponseForm, ThreadForm, NewUserForm
from datetime import date

# globals (categories, current year) for all views
CATEGORIES = Category.objects.all()
CUR_YEAR = date.today().year


class BridgeHomeView(View):
    """View for home page"""

    def get(self, request):
        """GET home page"""
        # render with categories and current year
        return render(
            request=request,
            template_name='home.html',
            context={
                'categories': CATEGORIES,
                'year': CUR_YEAR,
                'user': request.user,
            },
        )


class BridgeCategoryView(View):
    """View for single category page"""

    def get(self, request, category_id, category_slug): # slug for URL
        """GET single category page"""
        # get all users
        users = User.objects.all()
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
                'user': request.user,
                'users': users,
                'category': category,
                'threads': threads,
                'thread_form': form,
            },
        )

    def post(self, request, category_id, category_slug):
        """POST thread in single category page"""
         # get POST data from ThreaForm
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
                thread = Thread.objects.create(user=request.user, body=question)
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
        # get all users
        users = User.objects.all()
        # get requested thread from DB
        thread = Thread.objects.get(id=thread_id)
        # get all responses to thread in desc chronological order
        responses = Response.objects.filter(thread=thread).order_by('-date')
        # get ResponseForm for POST action & prepopulate if updating
        form = ResponseForm(initial={'body': Response.objects.get(id=resp_id).body if resp_id else ''})
        # render with thread, responses, ResponseForm & response_id
        return render(
            request=request,
            template_name='thread.html',
            context={
                'categories': CATEGORIES,
                'year': CUR_YEAR,
                'user': request.user,
                'users': users,
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
                Response.objects.create(user=request.user, body=resp_text, thread_id=thread_id)
            # update existing response if POST action is 'update'
            elif 'update' in request.POST:
                # response being updated
                response = Response.objects.get(id=resp_id)
                # only allow author to update response
                if response.user_id == request.user.id:
                    if resp_text != response.body:
                        Response.objects.filter(id=resp_id).update(body=resp_text)
                    else:
                        messages.error(request, 'You\'ve made no changes. Try again.')
                else:
                    messages.error(request, 'You don\'t have permission to edit the response.')
            # remove existing response if POST action is 'remove'
            elif 'remove' in request.POST:
                # response being updated
                response = Response.objects.get(id=resp_id)
                # only allow author to delete response
                if response.user_id == request.user.id:
                    Response.objects.filter(id=resp_id).delete()
                else:
                    messages.error(request, "You don't have permission to remove the response.")

        # redirect to single thread page
        return redirect('thread', thread_id, 0)


class BridgeAuthenticateView(View):
    """View for register/login page"""

    def get(self, request):
        """GET register/login page"""
        # get custom NewUserForm and built-in AuthenticationForm
        register_form = NewUserForm()
        login_form = AuthenticationForm()
        # render page with register/login forms
        return render(
            request=request,
            template_name='login.html',
            context={
                'year': CUR_YEAR,
                'user': request.user,
                'register_form': register_form,
                'login_form': login_form,
            }
        )

    def post(self, request):
        """POST user sign-up/login"""
        # handles registration
        if 'register' in request.POST:
            # get registration info
            form = NewUserForm(request.POST)
            # create and login user on valid form info
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, f"Hi, {user.username}" )
                return redirect(settings.LOGIN_REDIRECT_URL)
            # flash message on invalid form info
            else:
                messages.error(request, "Invalid information. Please try again.")
        # handles login
        elif 'login' in request.POST:
            # get login credential
            form = AuthenticationForm(request, data=request.POST)
            # check for valid form info
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                # login only on valid credential
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Hi, {username}." )
                    return redirect(settings.LOGIN_REDIRECT_URL)
                # flash message on invalid credential
                else:
                    messages.error(request, "Invalid username or password.")
            # flash message on invliad form info
            else:
                messages.error(request, "Invalid username or password.")
        # render login.html again on failed registration/login
        register_form = NewUserForm()
        login_form = AuthenticationForm()
        return render(
            request=request,
            template_name='login.html',
            context={
                'year': CUR_YEAR,
                'user': request.user,
                'register_form': register_form,
                'login_form': login_form,
            }
        )


class BridgeLogOutView(View):
    """Templateless view for logout button"""
    def get(self, request):
        user = request.user
        # log out and redirect to login page at once
        logout(request)
        messages.success(request, f"Bye, {user.username}.")
        return redirect(settings.LOGOUT_REDIRECT_URL)
