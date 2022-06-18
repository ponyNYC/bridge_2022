from django import forms
from django.db import connection
from .models import Category

class ResponseForm(forms.Form):
    """Form to create/update responses to threads"""
    # required <textarea> field using placeholder as label
    body = forms.CharField(
        required=True,
        label='',
        widget=forms.Textarea(attrs={
            'rows': '6',
            'autofocus': True,
            'placeholder': 'Write a new response here.'
        }))


class ThreadForm(forms.Form):
    """Form to generate threads (questions)"""

    # required <textarea> field using placeholder as label
    body = forms.CharField(
        required=True,
        label='',
        widget=forms.Textarea(attrs={
            'rows': '6',
            'autofocus': True,
            'placeholder': 'Submission without checking at least one category to which this question relates will not be accepted.'
        }))

    # required multi-select checkboxes for assigning categories to thread
    category_ids = forms.MultipleChoiceField(
        required=True,
        label='',
        widget=forms.CheckboxSelectMultiple(),
        # categories as labels (none to work around migration issue)
        choices=[(f"{category.id}", f"{category.type}") for category in Category.objects.all()] if 'bridgeapp_category' in connection.introspection.table_names() else [],
    )
