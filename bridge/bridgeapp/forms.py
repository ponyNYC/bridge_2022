from django import forms
from bridgeapp.models import Category
# from bridgeapp.models import Category, Thread, Response

CAT_CHOICES = [(f"{category.id}", f"{category.type}") for category in Category.objects.all()]

class InputForm(forms.Form):
    # body = forms.CharField(label='Add note', max_length=255)
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': '2', 'cols': '50'}), required=True)

class ThreadForm(InputForm):
  category_ids = forms.MultipleChoiceField(
    label='Check applicable categories',
    widget=forms.CheckboxSelectMultiple, choices=CAT_CHOICES,
    required=True
    )
