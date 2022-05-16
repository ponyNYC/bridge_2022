from django import forms
from .models import Category

CATEGORIES = Category.objects.all()
CAT_CHOICES = [(f"{category.id}", f"{category.type}") for category in CATEGORIES]

class NewThreadForm(forms.Form):
  body = forms.CharField(label='Create New Thread', max_length=255, widget=forms.Textarea(attrs={'rows': '10', 'cols': '40'}), required=True)
  category_ids = forms.MultipleChoiceField(
    label='To which category or categories your question relates?',
    widget=forms.CheckboxSelectMultiple, choices=CAT_CHOICES,
    required=True
    )
