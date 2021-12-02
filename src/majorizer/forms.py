from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='', max_length=100)

class ClassSearchForm(forms.Form):
    search_term = forms.CharField(label='', max_length=20)