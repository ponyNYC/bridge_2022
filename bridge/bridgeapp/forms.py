from django import forms
from bridgeapp.models import Category

CAT_CHOICES = [(f"{category.id}", f"{category.type}")
               for category in Category.objects.all()]


class ResponseForm(forms.Form):
    body = forms.CharField(
        required=True,
        label='',
        widget=forms.Textarea(attrs={
            'rows': '2',
            'cols': '50',
            'placeholder': 'Write a response here.'
            }))


class ThreadForm(forms.Form):
    body = forms.CharField(
        required=True,
        label='',
        widget=forms.Textarea(attrs={
            'rows': '2',
            'cols': '50',
            'placeholder': 'Post a question here.'
            }))
    category_ids = forms.MultipleChoiceField(
        required=True,
        label='Check applicable categories',
        widget=forms.CheckboxSelectMultiple(attrs={'checked': True}),
        choices=CAT_CHOICES,
    )
