from django import forms

class django_form(forms.Form):
    contents= forms.CharField(required=True)