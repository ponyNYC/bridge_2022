from django import forms

class ResponseForm(forms.Form):
    """Form used for Responses to Threads"""
    # simple form with a single CharField
    body = forms.CharField(
        required=True,
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'cols': '50',
            # causes cursor to focus on text input area upon page load
            'autofocus': True,
            # inserts placeholder text into text input area as prompt for user
            'placeholder': 'Write a response here...'
        }))


class ThreadForm(forms.Form):
    """Form used for creation of Threads"""
    body = forms.CharField(
        # requires entry in this field before form can be submitted
        required=True,
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'cols': '50',
            # causes cursor to focus on text input area upon page load
            'autofocus': True,
            # inserts placeholder text into text input area as prompt for user
            'placeholder': 'Type a new question here then assign categories below...'
        }))
    # assigns a multiple choice field to category_ids variable, allowing user to select categories for newly created thread
    category_ids = forms.MultipleChoiceField(
        # requires entry in this field before form can be submitted
        required=True,
        # adds label adjacent to input area as prompt to user
        label='Applicable categories (deselect as needed)',
        # sets default value for check boxes to checked to prevent submission of form with no boxes checked
        widget=forms.CheckboxSelectMultiple(attrs={'checked': True}),
        # list of check boxes labeled with values from CAT_CHOICES global variable
        choices=[
            ('1', 'Pre-commitment'),
            ('2', 'Currently Incarcerated'),
            ('3', 'Post-release')
        ],
    )
