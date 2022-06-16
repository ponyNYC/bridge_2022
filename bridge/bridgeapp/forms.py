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
            'rows': '3',
            'cols': '50',
            'autofocus': True,
            'placeholder': 'Write a response here...'
        }))


class ThreadForm(forms.Form):
    """Form to generate threads (questions)"""

    # required <textarea> field using placeholder as label
    body = forms.CharField(
        required=True,
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'cols': '50',
            'autofocus': True,
            'placeholder': 'Type a new question here then assign categories below...'
        }))

    # required multi-select checkboxes for assigning categories to thread
    category_ids = forms.MultipleChoiceField(
        required=True,
        label='Applicable categories (deselect as needed)',
        # default to all boxes checked
        widget=forms.CheckboxSelectMultiple( attrs={'checked': True}),
        # categories as labels (none to work around migration issue)
        choices=[(f"{category.id}", f"{category.type}") for category in Category.objects.all()] if 'bridgeapp_category' in connection.introspection.table_names() else [],
    )
