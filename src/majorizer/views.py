from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm

# Create your views here.
def home_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            form = LoginForm(request.POST)
            return render(request, "home.html", {'form' : form, 'name' : name})

    #return HttpResponse("<h1>Hello World</h1>")
    return render(request, "home.html", {'form' : form, 'name' : "NONE"})

