from django import forms


class create_tag_form(forms.Form):
    name=forms.CharField(required=True,widget=forms.TextInput(attrs={'class':"form-control"}))#(attrs={'class':"form-control"} 給html 的class or id
    description=forms.CharField(required=True,widget=forms.TextInput(attrs={'class':"form-control"}))