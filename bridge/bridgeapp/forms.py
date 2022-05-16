from django import forms
from bridgeapp.models import Category, Thread, Response

CATEGORIES = Category.objects.all()
CAT_CHOICES = [(f"{category.id}", f"{category.type}") for category in CATEGORIES]

RESPONSES = Response.objects.all()

class NewThreadForm(forms.Form):
  body = forms.CharField(label='Create New Thread', max_length=255, widget=forms.Textarea(attrs={'rows': '10', 'cols': '40'}), required=True)
  category_ids = forms.MultipleChoiceField(
    label='To which category or categories your question relates?',
    widget=forms.CheckboxSelectMultiple, choices=CAT_CHOICES,
    required=True
    )

class ResponseForm(forms.Form):
    body = forms.CharField(label='Add note', max_length=255)

# class ThreadForm(forms.ModelForm):
#     class Meta:
#         model = Thread
#         fields = ['body']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.fields['body'].label = 'Add Thread'

# class ResponseForm(forms.ModelForm):
#     class Meta:
#         model = Response
#         fields = ['body']

#     def __init__(self, *args, **kwargs):
#         thread_object = kwargs.pop('thread')
#         super().__init__(*args, **kwargs)

#         self.instance.thread = thread_object
#         self.fields['body'].label = ''