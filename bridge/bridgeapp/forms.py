from django import forms
from django.db import connection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category, Thread, Response


class ResponseForm(forms.ModelForm):
    """ModelForm using bridge_response table"""

    class Meta:
        model = Response
        fields = ['body']
        labels = {'body': ''}
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': '6',
                'placeholder': 'Write a new response here.'
            })
        }


class ThreadForm(forms.ModelForm):
    """ModelForm using bridge_thread table"""
    category_ids = forms.MultipleChoiceField(
        required=True,
        label='',
        widget=forms.CheckboxSelectMultiple(),
        choices=[(f"{category.id}", f"{category.type}") for category in Category.objects.all()] if 'bridgeapp_category' in connection.introspection.table_names() else []
        )

    class Meta:
        model = Thread
        fields = ['body', 'category_ids']
        labels = {'body': ''}
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': '6',
                'placeholder': 'Submission without checking at least one category to which this question relates will not be accepted.'
            })
        }


class NewUserForm(UserCreationForm):
    """Custom user creation form"""
    email = forms.EmailField(required=True)

    class Meta:
        """use User model and add email field"""
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


    def save(self, commit=True):
        """Save email with username and password"""
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit: user.save()
        return user
