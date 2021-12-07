from datetime import time, timedelta, datetime
from majorizer.models import *



def time_range(start, end, delta):
    # https://stackoverflow.com/questions/39298054/generating-15-minute-time-interval-array-in-python
    # https://stackoverflow.com/questions/656297/python-time-timedelta-equivalent
    # The following two lines are necessary because time objects do not support
    # addition with timedelta, but datetime objects do
    date_start = datetime(2001, 2, 28, start.hour, start.minute)  # Date is arbitrary, we only care about the time
    date_end = datetime(2001, 2, 28, end.hour, end.minute)
    current = date_start
    while current < date_end:
        yield current.time()
        current += timedelta(minutes=delta)

times = [t for t in time_range(time(8), time(21, 30), 30)]

def init_timeslots(timeslots):
    timeslots.clear()
    for t in times:
        timeslots.append(TimeSlot(t))

def schedule_to_timeslots(schedule, timeslots):

    init_timeslots(timeslots)

    for course in schedule.courses.all():
        days = course.days.split(",")
        start = course.start_time
        end = course.end_time
        # This section populates the timeslots with courses from the schedule
        for index, timeslot in enumerate(timeslots):
            for day in days:
                if (timeslot.time == start):
                    timeslot.classes[int(day)] = (course.course_id.name, course.id)
                elif (timeslots[index-1].classes[int(day)][0] == course.course_id.name and timeslot.time <= end):
                    timeslot.classes[int(day)] = (course.course_id.name, course.id)
        #This section calculates the correct rowspan for the html table elements (Currently doesn't work for schedules with more than one class)
        # for index, timeslot in enumerate(timeslots):
        #     for day in days:
        #         j=1
        #         while (index + j < len(timeslots) and timeslots[index+j].classes[int(day)] == "up"):
        #             j += 1
        #             timeslot.rowspan += 1
        #     timeslot.rowspan = int(timeslot.rowspan / len(days))

def search_classes(search_term):
    search_term = search_term.upper()
    return DBCourse.objects.filter(course_number__contains=search_term).values()

def get_course_offerings(c_id, schedule):
    already_in_schedule = schedule.courses.all()
    return DBCourseOffering.objects.filter(course_id__pk = c_id).exclude(id__in=already_in_schedule).values()

def get_majors():
    return DBDegreeProgram.objects.filter(is_major=True).values()

def get_minors():
    return DBDegreeProgram.objects.filter(is_major=False).values()

def add_course_to_schedule(course_offering, schedule):
    schedule.courses.add(course_offering)

def remove_course_from_schedule(course_offering, schedule):
    schedule.courses.remove(course_offering)

class TimeSlot:
    def __init__(self, time) -> None:
        self.time = time
        self.classes = ["none"] * 5  # Indices 0-4 represent Mon-Fri
        #self.rowspan = 1  # This probably doesn't work here. Classes should store their own rowspans maybe?