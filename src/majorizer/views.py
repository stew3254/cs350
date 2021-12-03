from django.http import HttpResponse
from django.shortcuts import render
from majorizer.models import *
from majorizer.util import *
from django.contrib.auth import authenticate, login, logout

from .forms import ClassSearchForm, LoginForm

from datetime import time

# Sets up timeslots
times = [t for t in time_range(time(8), time(21, 30), 30)]

timeslots = []
for t in times:
    timeslots.append(TimeSlot(t))

# Test data
test_schedule = DBSchedule.objects.filter(name="Test Schedule")[0]


# Create your views here.
def home_view(request):
    login_form = LoginForm()
    class_search_form = ClassSearchForm()

    user = None

    name = ""
    class_search_term = ""
    class_search_results = []
    logged_in = False
    offerings = None
    selected_class = None
    active_schedule = test_schedule

    schedule_to_timeslots(active_schedule, timeslots)

    context_dict = {}
    

    # Handle forms
    if request.method == 'POST':
        if "login_button" in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                name = login_form.cleaned_data['username']
                pword = login_form.cleaned_data['password']
                user = authenticate(username=name, password=pword)
                if user is not None:
                    login(request, user)
                    logged_in = True

        elif "logout_button" in request.POST:
            logout(request)
            logged_in = False

        elif "class_search_button" in request.POST:
            class_search_form = ClassSearchForm(request.POST)
            if class_search_form.is_valid():
                class_search_term = class_search_form.cleaned_data['search_term']
                class_search_results = search_classes(class_search_term)

        elif "class_search_result_button" in request.POST:
            #print(request.POST['class_search_result_button'])
            selected_class = request.POST['class_search_result_button']
            offerings = get_course_offerings(selected_class)

        elif "course_offering_button" in request.POST:
            print(request.POST['course_offering_button'])
            
                
    context_dict['login_form'] = login_form
    context_dict['class_search_form'] = class_search_form
    context_dict['name'] = name
    context_dict['timeslots'] = timeslots
    context_dict['class_search_term'] = class_search_term
    context_dict['class_search_results'] = class_search_results
    context_dict['logged_in'] = logged_in
    context_dict['offerings'] = offerings
    context_dict['selected_class'] = selected_class
    context_dict['active_schedule'] = active_schedule

    return render(request, "home.html", context_dict)

