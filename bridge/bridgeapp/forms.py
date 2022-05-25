from django import forms
from bridgeapp.models import Category

CAT_CHOICES = [(f"{category.id}", f"{category.type}")
               for category in Category.objects.all()]


class ResponseForm(forms.Form):
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
    body = forms.CharField(
        required=True,
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'cols': '50',
            'autofocus': True,
            'placeholder': 'Type a new question here then assign categories below...'
        }))

    category_ids = forms.MultipleChoiceField(
        required=True,
        label='Applicable categories (deselect as needed)',
        widget=forms.CheckboxSelectMultiple(attrs={'checked': True}),
        choices=CAT_CHOICES,
    )
