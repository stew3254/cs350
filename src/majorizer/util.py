from datetime import time, timedelta, datetime

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
        #This section calculates the correct rowspan for the html table elements
        # for index, timeslot in enumerate(timeslots):
        #     for day in days:
        #         j=1
        #         while (index + j < len(timeslots) and timeslots[index+j].classes[int(day)] == "up"):
        #             j += 1
        #             timeslot.rowspan += 1
        #     timeslot.rowspan = int(timeslot.rowspan / len(days))


class TimeSlot:
    def __init__(self, time) -> None:
        self.time = time
        self.classes = ["none"] * 5  # Indices 0-4 represent Mon-Fri
        #self.rowspan = 1