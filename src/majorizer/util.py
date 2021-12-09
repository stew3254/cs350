from datetime import time, timedelta, datetime

from django.db.models.expressions import Case
from majorizer.models import *
import pandas as reader
import re

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

def schedule_to_timeslots(schedule, timeslots):
    for course in schedule.courses.all():
        days = course.days.split(",")
        start = course.start_time
        end = course.end_time
        # This section populates the timeslots with courses from the schedule
        for index, timeslot in enumerate(timeslots):
            for day in days:
                if (timeslot.time == start):
                    timeslot.classes[int(day)] = course.course_id.name
                elif ((timeslots[index-1].classes[int(day)] == course.course_id.name or timeslots[index-1].classes[int(day)] == "up") and timeslot.time <= end):
                    timeslot.classes[int(day)] = course.course_id.name
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
    results = DBCourse.objects.filter(course_number__contains=search_term).values()
    return results

def get_course_offerings(c_id):
    print(c_id)
    results = DBCourseOffering.objects.filter(course_id__pk = c_id).values()
    return results

def parse(file):
    df = reader.read_csv(file)
    program = df[0,0]
    df.drop(index=0, inplace=True)


    for item in df:
        time = str(item[2])
        if time == "N/A":
            time = -1
            end_time = begin_time = time
        elif time.startswith('L'):
            time = time[:2]
            time_array = filter(None, time.split(" "))
            days = filter(None, re.split("([A-Z][^A-Z]*)", time_array[0]))
            for day in days:
                switch = {
                    "M":0,
                    "T":1,
                    "Tu":1,
                    "w":2,
                    "Th":3,
                    "R":3,
                    "F":4
                }
                day = switch.get(day)

            time_array = filter(None, time.split("-"))
            begin_time = datetime.strptime(time_array[0], "%H:%M")
            end_time = datetime.strptime(time_array[1], "%H:%M")

        course = DBCourse(course_id=item[8], name=item[1], course_number=item[0])
        course.save()

        course_offering = DBCourseOffering(term=item[3], instructor=item[6], start_time=begin_time, end_time=end_time, days=days, room=item[6], section_num = 1, course_id=course)
        course_offering.save()
        program.save()
        program.courses.add(course_offering)
    


class TimeSlot:
    def __init__(self, time) -> None:
        self.time = time
        self.classes = ["none"] * 5  # Indices 0-4 represent Mon-Fri
        #self.rowspan = 1  # This probably doesn't work here. Classes should store their own rowspans maybe?