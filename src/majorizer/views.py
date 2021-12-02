from django.http import HttpResponse
from django.shortcuts import render
from majorizer.models import *
from majorizer.util import *

from .forms import ClassSearchForm, LoginForm

from datetime import time

# Sets up timeslots
times = [t for t in time_range(time(8), time(21, 30), 30)]

timeslots = []
for t in times:
    timeslots.append(TimeSlot(t))

# Test data
test_schedule = DBSchedule.objects.filter(name="Test Schedule")[0]
schedule_to_timeslots(test_schedule, timeslots)

# Create your views here.
def home_view(request):
    login_form = LoginForm()
    class_search_form = ClassSearchForm()

    name = ""
    class_search_term = ""
    class_search_results = []

    context_dict = {}
    

    # Handle forms
    if request.method == 'POST':
        if "login_button" in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                name = login_form.cleaned_data['username']
                login_form = LoginForm(request.POST)
        elif "class_search_button" in request.POST:
            class_search_form = ClassSearchForm(request.POST)
            if class_search_form.is_valid():
                class_search_term = class_search_form.cleaned_data['search_term']
                class_search_results = search_classes(class_search_term)
                
    context_dict['login_form'] = login_form
    context_dict['class_search_form'] = class_search_form
    context_dict['name'] = name
    context_dict['timeslots'] = timeslots
    context_dict['class_search_term'] = class_search_term
    context_dict['class_search_results'] = class_search_results

    return render(request, "home.html", context_dict)

