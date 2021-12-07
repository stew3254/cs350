from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}))

class ClassSearchForm(forms.Form):
    search_term = forms.CharField(label='', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search classes'}))