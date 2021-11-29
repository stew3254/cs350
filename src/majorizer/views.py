from django.http import HttpResponse
from django.shortcuts import render
from majorizer.models import *

from .forms import LoginForm

from datetime import time, timedelta, datetime

# There must be a better way to do this
# Update: found a better way to do this
"""
times = ["8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM", 
    "12:30 PM", "1:00 PM", "1:30 PM", "2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM", 
    "5:30 PM", "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM", "9:00 PM"]
"""

def time_range(start, end, delta):
    # https://stackoverflow.com/questions/39298054/generating-15-minute-time-interval-array-in-python
    # https://stackoverflow.com/questions/656297/python-time-timedelta-equivalent
    # The following two lines are necessary because time objects do not support
    # addition with timedelta for some reason, but datetime objects do
    date_start = datetime(2001, 2, 28, start.hour, start.minute)  # Date is arbitrary, we only care about the time
    date_end = datetime(2001, 2, 28, end.hour, end.minute)
    current = date_start
    while current < date_end:
        yield current.time()
        current += timedelta(minutes=delta)

times = [t for t in time_range(time(8), time(21, 30), 30)]

class TimeSlot:
    def __init__(self, time) -> None:
        self.time = time
        self.classes = ["none"] * 5  # Indices 0-4 represent Mon-Fri

timeslots = []
for time in times:
    timeslots.append(TimeSlot(time))

test_schedule = DBSchedule.objects.get(name="Test Schedule")

def schedule_to_timeslots(schedule, time_slots):
    for course in schedule.courses.all():
        days = course.days.split(",")
        #days = map(int, days)
        start = course.start_time
        end = course.end_time
        for index, timeslot in enumerate(time_slots):
            for day in days:
                # print(index)
                # print(timeslot.time)
                if (timeslot.time == start):
                    timeslot.classes[int(day)] = course.course_id
                elif ((timeslots[index-1].classes[int(day)] == course.course_id or timeslots[index-1].classes[int(day)] == "up") and timeslot.time <= end):
                    timeslot.classes[int(day)] = course.course_id

schedule_to_timeslots(test_schedule, timeslots)


# Create your views here.
def home_view(request):
    login_form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            form = LoginForm(request.POST)
            return render(request, "home.html", {'login_form' : login_form, 'name' : name, 'timeslots' : timeslots})

    return render(request, "home.html", {'login_form' : login_form, 'name' : "NONE", 'timeslots' : timeslots})

