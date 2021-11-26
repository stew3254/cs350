from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm

# There must be a better way to do this
times = ["8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM", 
    "12:30 PM", "1:00 PM", "1:30 PM", "2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM", 
    "5:30 PM", "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM", "9:00 PM"]

class TimeSlot:
    def __init__(self, time) -> None:
        self.time = time
        self.classes = ["none"] * 5  # Indices 0-4 represent Mon-Fri

timeslots = []
for time in times:
    timeslots.append(TimeSlot(time))

# Create your views here.
def home_view(request):
    login_form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            form = LoginForm(request.POST)
            return render(request, "home.html", {'login_form' : login_form, 'name' : name, 'times' : times})

    return render(request, "home.html", {'login_form' : login_form, 'name' : "NONE", 'timeslots' : timeslots})

